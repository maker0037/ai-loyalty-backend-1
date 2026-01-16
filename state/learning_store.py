# state/learning_store.py

import json
import os
from typing import Dict

DATA_PATH = "data/snapshots/learning_store.json"

LEARNING_STATE: Dict[str, dict] = {}


def load_learning_state():
    global LEARNING_STATE
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            LEARNING_STATE = json.load(f)
    return LEARNING_STATE


def persist_learning_state():
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w") as f:
        json.dump(LEARNING_STATE, f, indent=2)


def update_learning(segment_id: str, adjustment: dict):
    LEARNING_STATE[segment_id] = adjustment
    persist_learning_state()


def get_learning(segment_id: str):
    return LEARNING_STATE.get(segment_id)
