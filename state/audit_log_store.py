# state/audit_log_store.py

import json
import os
from datetime import datetime
from typing import List

DATA_PATH = "data/snapshots/audit_logs.json"
AUDIT_LOGS: List[dict] = []


def log_event(event_type: str, payload: dict):
    AUDIT_LOGS.append({
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "payload": payload,
    })
    persist_logs()


def persist_logs():
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w") as f:
        json.dump(AUDIT_LOGS, f, indent=2)


def get_audit_logs() -> List[dict]:
    return AUDIT_LOGS
