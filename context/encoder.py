import joblib
import os


def safe_transform(encoder, value):
    try:
        return encoder.transform([value])[0]
    except ValueError:
        return 0


class EncoderService:
    def __init__(self):
        BASE_DIR = os.getcwd()
        MODEL_DIR = os.path.join(BASE_DIR, "src")

        print(f"[DEBUG] Encoder loading from: {MODEL_DIR}")

        self.location_encoder = joblib.load(os.path.join(MODEL_DIR, "location_encoder.pkl"))
        self.traffic_encoder = joblib.load(os.path.join(MODEL_DIR, "traffic_encoder.pkl"))
        self.time_encoder = joblib.load(os.path.join(MODEL_DIR, "time_encoder.pkl"))
        self.target_encoder = joblib.load(os.path.join(MODEL_DIR, "target_encoder.pkl"))

    def encode_features(self, data: dict):
        return {
            "fatigue_level": data["fatigue_level"],
            "stress_level": data["stress_level"],
            "battery_level": data["battery_level"],
            "speed": data["speed"],
            "location_type": safe_transform(self.location_encoder, data["location_type"]),
            "traffic_level": safe_transform(self.traffic_encoder, data["traffic_level"]),
            "time_of_day": safe_transform(self.time_encoder, data["time_of_day"]),
        }

    def decode_target(self, value: int):
        return self.target_encoder.inverse_transform([int(value)])[0]