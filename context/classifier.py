class BatteryClassifier:

    @staticmethod
    def classify(battery: int) -> str:
        if battery < 10:
            return "critical"
        elif battery < 30:
            return "low"
        else:
            return "normal"


class TimeClassifier:

    @staticmethod
    def classify(time_str: str) -> str:
        hour = int(time_str.split(":")[0])

        if 22 <= hour or hour < 5:
            return "night"
        elif 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        else:
            return "evening"


class LocationClassifier:

    @staticmethod
    def classify(location: str) -> str:
        location = location.lower()

        if "highway" in location:
            return "highway"
        elif "city" in location:
            return "city"
        else:
            return "unknown"