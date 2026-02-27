from fastapi import APIRouter
from app.models import ContextRequest, ContextResponse
from context.extractor import DriverStateExtractor

from context.classifier import BatteryClassifier, TimeClassifier, LocationClassifier
from context.fusion import ContextFusionEngine

from context.ml_model import RiskModelService
from context.encoder import EncoderService
from context.utils.decision_logger import log_decision

from context.analytics.rule_stats import get_rule_frequency
from context.analytics.drift import compute_drift



import traceback

router = APIRouter()

# Lazy loading
ml_service = None
encoder_service = None


def get_services():
    global ml_service, encoder_service

    if ml_service is None:
        ml_service = RiskModelService()

    if encoder_service is None:
        encoder_service = EncoderService()

    return ml_service, encoder_service


@router.post("/analyze", response_model=ContextResponse)
def analyze_context(request: ContextRequest):

    try:
        ml_service, encoder_service = get_services()

        # Step 1: Extract
        extracted = DriverStateExtractor.extract(request.user_text)

        # Step 2: Classify
        battery_status = BatteryClassifier.classify(request.battery)
        time_of_day = TimeClassifier.classify(request.time)
        location = LocationClassifier.classify(request.location)

        # Step 3: Build Context
        context = {
            "driver_state": extracted["driver_state"],
            "battery_status": battery_status,
            "time_of_day": time_of_day,
            "location": location,
        }

        # Step 4: ML Features
        raw_features = {
            "fatigue_level": 8 if extracted["driver_state"] == "fatigued" else 2,
            "stress_level": 6 if extracted["driver_state"] == "stressed" else 2,
            "battery_level": request.battery,
            "speed": 60,
            "location_type": location,
            "traffic_level": "medium",
            "time_of_day": time_of_day,
        }

        encoded_features = encoder_service.encode_features(raw_features)

        # Step 5: ML Prediction
        ml_pred_encoded, confidence = ml_service.predict(encoded_features)
        ml_risk = encoder_service.decode_target(ml_pred_encoded)

        # Step 6: Rule-based output
        rule_output = ContextFusionEngine.fuse(context)
        rule_risk = rule_output["risk_level"]

        rule_output.setdefault("rules_triggered", [])
        rule_output.setdefault("explanation", [])

        # Step 7: Decision Logic
        final_risk = rule_risk

        if rule_risk == "high":
            decision_source = "rules_override"

        elif rule_risk == "low" and confidence > 0.75:
            final_risk = ml_risk
            decision_source = "ml_override"

        elif rule_risk != ml_risk:
            decision_source = "conflict_rules_preferred"

        else:
            decision_source = "rules"

        # Step 8: Update Output
        rule_output["risk_level"] = final_risk
        rule_output["ml_prediction"] = ml_risk
        rule_output["confidence_score"] = round(confidence, 3)
        rule_output["decision_source"] = decision_source

        # Explainability (improved)
        rule_output["rules_triggered"].append(f"DECISION_{decision_source.upper()}")
        rule_output["explanation"].append(
            f"Rule risk: {rule_risk}, ML risk: {ml_risk}, "
            f"Confidence: {confidence:.2f}, Decision: {decision_source}"
        )

        # Logging
        log_decision({
            "input": {
                "text": request.user_text,
                "battery": request.battery,
                "time": request.time,
                "location": request.location
            },
            "rule_risk": rule_risk,
            "ml_risk": ml_risk,
            "final_risk": final_risk,
            "confidence": confidence,
            "decision_source": decision_source,
            "rules_triggered": rule_output["rules_triggered"]
        })

        return rule_output

    except Exception as e:
        print("[ERROR]", str(e))
        traceback.print_exc()

        return {
            "driver_state": "unknown",
            "battery_status": "unknown",
            "time_of_day": "unknown",
            "location": "unknown",
            "priority": "unknown",
            "recommended_action": "error",
            "risk_level": "error",
            "ml_prediction": "error",
            "confidence_score": 0,
            "decision_source": "error",
            "rules_triggered": [],
            "explanation": [str(e)]
        }
    

# -------------------------------
# ANALYTICS ENDPOINTS
# -------------------------------

@router.get("/analytics/rules")
def rule_analytics():
    try:
        return {
            "rule_frequency": get_rule_frequency()
        }
    except Exception as e:
        return {
            "rule_frequency": {},
            "error": str(e)
        }


@router.get("/analytics/drift")
def drift_analytics():
    try:
        return compute_drift()
    except Exception as e:
        return {
            "drift_rate": 0,
            "total_samples": 0,
            "mismatch_count": 0,
            "error": str(e)
        }