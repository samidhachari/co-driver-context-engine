"""
Context Fusion Engine with Explainability and Rule Tracing.
"""

from typing import Dict, List
class DriverStateExtractor:

    @staticmethod
    def extract(text: str):
        text = text.lower()

        if any(word in text for word in ["sleepy", "tired", "drowsy"]):
            return {"driver_state": "fatigued"}

        if any(word in text for word in ["stress", "angry", "frustrated"]):
            return {"driver_state": "stressed"}

        return {"driver_state": "normal"}
    
class ContextFusionEngine:
    """
    Combines multiple context signals into a final decision
    with explainability and rule tracing.
    """

    @staticmethod
    def compute_risk(
        driver_state: str,
        battery_status: str,
        time_of_day: str,
        location: str,
        trace: Dict
    ) -> str:

        explanations: List[str] = trace["explanations"]
        rules: List[str] = trace["rules"]

        # Rule 1: Fatigue + Night
        if driver_state == "fatigued" and time_of_day == "night":
            rules.append("RULE_FATIGUE_NIGHT_HIGH_RISK")
            explanations.append("Driver is fatigued during night time")
            return "high"

        # Rule 2: Fatigue + Highway
        if driver_state == "fatigued" and location == "highway":
            rules.append("RULE_FATIGUE_HIGHWAY_HIGH_RISK")
            explanations.append("Fatigue detected while driving on highway")
            return "high"

        # Rule 3: Critical Battery
        if battery_status == "critical":
            rules.append("RULE_BATTERY_CRITICAL")
            explanations.append("Battery level is critically low")
            return "high"

        # Rule 4: Stress + City
        if driver_state == "stressed" and location == "city":
            rules.append("RULE_STRESS_CITY_MEDIUM_RISK")
            explanations.append("Driver stress detected in city conditions")
            return "medium"

        # Rule 5: Low Battery
        if battery_status == "low":
            rules.append("RULE_BATTERY_LOW")
            explanations.append("Battery level is low")
            return "medium"

        # Default Rule
        rules.append("RULE_DEFAULT_LOW_RISK")
        explanations.append("No significant risk factors detected")
        return "low"

    @staticmethod
    def determine_priority(risk_level: str) -> str:
        if risk_level == "high":
            return "safety_critical"
        if risk_level == "medium":
            return "attention_needed"
        return "normal"

    @staticmethod
    def recommend_action(
        driver_state: str,
        battery_status: str,
        risk_level: str,
        trace: Dict
    ) -> str:

        explanations: List[str] = trace["explanations"]
        rules: List[str] = trace["rules"]

        # Safety actions
        if driver_state == "fatigued" and risk_level == "high":
            rules.append("ACTION_REST_BREAK")
            explanations.append("System recommends taking a rest break")
            return "suggest_rest_break"

        if driver_state == "stressed":
            rules.append("ACTION_REDUCE_DISTRACTION")
            explanations.append("Reducing distractions for stressed driver")
            return "reduce_distractions"

        # Battery actions
        if battery_status == "critical":
            rules.append("ACTION_NAVIGATE_CHARGING")
            explanations.append("Navigating to nearest charging station")
            return "navigate_to_nearest_charging"

        if battery_status == "low":
            rules.append("ACTION_SUGGEST_CHARGING")
            explanations.append("Suggesting nearby charging station")
            return "suggest_charging"

        rules.append("ACTION_NONE")
        explanations.append("No action required")
        return "no_action"

    @staticmethod
    def fuse(context: Dict[str, str]) -> Dict:
        """
        Main fusion with explainability.
        """

        trace = {
            "rules": [],
            "explanations": []
        }

        driver_state = context.get("driver_state", "unknown")
        battery_status = context.get("battery_status", "unknown")
        time_of_day = context.get("time_of_day", "unknown")
        location = context.get("location", "unknown")

        risk_level = ContextFusionEngine.compute_risk(
            driver_state, battery_status, time_of_day, location, trace
        )

        priority = ContextFusionEngine.determine_priority(risk_level)

        action = ContextFusionEngine.recommend_action(
            driver_state, battery_status, risk_level, trace
        )

        return {
            "driver_state": driver_state,
            "battery_status": battery_status,
            "time_of_day": time_of_day,
            "location": location,
            "risk_level": risk_level,
            "priority": priority,
            "recommended_action": action,
            "rules_triggered": trace["rules"],
            "explanation": trace["explanations"]
        }