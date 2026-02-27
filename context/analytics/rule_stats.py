import json
from collections import Counter

LOG_PATH = "logs/decisions.jsonl"


def get_rule_frequency():
    counter = Counter()

    try:
        with open(LOG_PATH, "r") as f:
            for line in f:
                entry = json.loads(line)
                for rule in entry.get("rules_triggered", []):
                    counter[rule] += 1
    except FileNotFoundError:
        return {}

    return dict(counter)

