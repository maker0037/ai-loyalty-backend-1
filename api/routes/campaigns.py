# api/routes/campaigns.py

from fastapi import APIRouter, HTTPException
from state.campaign_store import (
    get_all_campaigns,
    get_campaign,
    update_campaign_status,
)

router = APIRouter(prefix="/campaigns", tags=["Campaigns"])


@router.get("/")
def list_campaigns():
    """
    List all campaigns currently in memory.
    """
    return {
        "count": len(get_all_campaigns()),
        "campaigns": get_all_campaigns(),
    }


@router.post("/approve")
def approve_campaign(campaign: dict):
    """
    Human approves AI recommendation.
    """
    campaign_id = campaign.get("campaign_id")
    if not campaign_id:
        raise HTTPException(status_code=400, detail="campaign_id missing")

    try:
        update_campaign_status(campaign_id, "DRAFT")
        return get_campaign(campaign_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/launch/{campaign_id}")
def launch_campaign(campaign_id: str):
    """
    Launch approved campaign.
    """
    try:
        update_campaign_status(campaign_id, "LAUNCHED")
        return get_campaign(campaign_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/update/{campaign_id}")
def update_campaign(campaign_id: str, campaign: dict):
    try:
        from state.campaign_store import update_campaign
        update_campaign(campaign_id, campaign)
        return campaign
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
