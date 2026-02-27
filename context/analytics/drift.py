import json

LOG_PATH = "logs/decisions.jsonl"


def compute_drift():
    total = 0
    mismatch = 0

    try:
        with open(LOG_PATH, "r") as f:
            for line in f:
                entry = json.loads(line)

                rule_risk = entry.get("rule_risk")
                ml_risk = entry.get("ml_risk")

                if rule_risk and ml_risk:
                    total += 1
                    if rule_risk != ml_risk:
                        mismatch += 1
    except FileNotFoundError:
        return {
            "drift_rate": 0,
            "total_samples": 0,
            "mismatch_count": 0
        }

    drift_rate = (mismatch / total) if total > 0 else 0

    return {
        "drift_rate": round(drift_rate, 3),
        "total_samples": total,
        "mismatch_count": mismatch
    }

