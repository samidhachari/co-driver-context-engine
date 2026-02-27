import joblib
import numpy as np
import os

print("ML MODEL FILE LOADED")


class RiskModelService:
    def __init__(self):
        BASE_DIR = os.getcwd()
        model_path = os.path.join(BASE_DIR, "src", "risk_model.pkl")

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}")

        print(f"[INFO] Loading model from: {model_path}")

        self.model = joblib.load(model_path)

    def predict(self, features: dict):
        feature_order = [
            "fatigue_level",
            "stress_level",
            "battery_level",
            "speed",
            "location_type",
            "traffic_level",
            "time_of_day"
        ]

        input_vector = np.array([features[f] for f in feature_order]).reshape(1, -1)

        prediction = self.model.predict(input_vector)[0]

        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(input_vector)[0]
            confidence = float(np.max(probs))
        else:
            confidence = 0.5

        return prediction, confidence