# state/override_store.py

import json
import os
from typing import List

DATA_PATH = "data/snapshots/override_store.json"
OVERRIDES: List[dict] = []


def log_override(override: dict):
    OVERRIDES.append(override)
    persist()


def persist():
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w") as f:
        json.dump(OVERRIDES, f, indent=2)


def get_overrides():
    return OVERRIDES
