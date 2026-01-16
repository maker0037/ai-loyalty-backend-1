# api/routes/campaigns.py

from fastapi import APIRouter, HTTPException
from services.campaign_service import (
    preview_campaign,
    launch_campaign,
    get_campaign_details,
)

router = APIRouter(prefix="/campaigns", tags=["Campaigns"])

@router.get("/")
def list_all_campaigns():
    """
    List all launched campaigns.
    """
    from services.campaign_service import list_campaigns
    return {
        "items": list_campaigns()
    }


@router.post("/preview")
def preview(payload: dict):
    try:
        return preview_campaign(payload["segment_id"])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/launch")
def launch(payload: dict):
    try:
        return launch_campaign(payload["segment_id"])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{campaign_id}")
def details(campaign_id: str):
    try:
        return get_campaign_details(campaign_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@router.post("/{campaign_id}/simulate")
def simulate_campaign(campaign_id: str):
    """
    Manually trigger engagement simulation (demo / testing).
    """

    from state.campaign_store import get_campaign, save_campaign
    from services.simulation_service import simulate_engagement_once
    from services.metrics_service import refresh_campaign_metrics

    campaign = get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    simulation_result = simulate_engagement_once(campaign)

    # Refresh metrics after simulation
    campaign = refresh_campaign_metrics(campaign)
    save_campaign(campaign)

    return {
        "status": "simulated",
        "simulation": simulation_result,
        "metrics": campaign["metrics"],
    }
