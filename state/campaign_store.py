# state/campaign_store.py

from typing import Dict, List

# In-memory campaign registry
CAMPAIGN_STORE: Dict[str, dict] = {}


def save_campaigns(campaigns: List[dict]):
    """
    Persist AI-generated campaigns in memory.
    Overwrites by campaign_id (idempotent).
    """
    for campaign in campaigns:
        CAMPAIGN_STORE[campaign["campaign_id"]] = campaign


def get_all_campaigns() -> List[dict]:
    return list(CAMPAIGN_STORE.values())


def get_campaign(campaign_id: str) -> dict | None:
    return CAMPAIGN_STORE.get(campaign_id)


def update_campaign_status(campaign_id: str, status: str):
    if campaign_id not in CAMPAIGN_STORE:
        raise ValueError("Campaign not found")

    CAMPAIGN_STORE[campaign_id]["status"] = status

def update_campaign(campaign_id: str, updated_campaign: dict):
    if campaign_id not in CAMPAIGN_STORE:
        raise ValueError("Campaign not found")

    CAMPAIGN_STORE[campaign_id] = updated_campaign
