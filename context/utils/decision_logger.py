import json
import os

LOG_FILE = os.path.join(os.getcwd(), "logs", "decisions.jsonl")


def log_decision(data: dict):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")

    print(f"LOGGING TRIGGERED: {LOG_FILE}")


def compute_drift():
    if not os.path.exists(LOG_FILE):
        return {
            "drift_rate": 0,
            "total_samples": 0,
            "mismatch_count": 0
        }

    total = 0
    mismatch = 0

    with open(LOG_FILE, "r") as f:
        for line in f:
            try:
                entry = json.loads(line)

                rule_risk = entry.get("rule_risk")
                ml_risk = entry.get("ml_risk")

                if rule_risk and ml_risk:
                    total += 1
                    if rule_risk != ml_risk:
                        mismatch += 1

            except:
                continue

    drift_rate = mismatch / total if total > 0 else 0

    return {
        "drift_rate": round(drift_rate, 3),
        "total_samples": total,
        "mismatch_count": mismatch
    }