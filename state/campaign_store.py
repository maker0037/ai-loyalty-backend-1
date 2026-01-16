# state/campaign_store.py

import json
import os

DATA_PATH = "data/snapshots/campaigns.json"
CAMPAIGN_STORE = {}


def load_campaigns():
    CAMPAIGN_STORE.clear()
    if not os.path.exists(DATA_PATH):
        return []

    with open(DATA_PATH, "r") as f:
        data = json.load(f)

    CAMPAIGN_STORE.update(data)
    return list(CAMPAIGN_STORE.values())


def save_campaign(campaign: dict):
    CAMPAIGN_STORE[campaign["campaign_id"]] = campaign
    persist()


def persist():
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w") as f:
        json.dump(CAMPAIGN_STORE, f, indent=2)


def get_campaign(campaign_id: str):
    return CAMPAIGN_STORE.get(campaign_id)


def get_all_campaigns():
    return list(CAMPAIGN_STORE.values())
