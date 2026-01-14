# api/routes/ai_module.py

from fastapi import APIRouter

from services.campaign_service import get_ai_campaign_recommendations
from agents.behavior_change_agent import detect_behavior_changes
from agents.segmentation_agent import segment_customers

router = APIRouter(prefix="/ai", tags=["AI"])


@router.get("/campaign-recommendations")
def campaign_recommendations():
    """
    Main AI endpoint.
    Returns fully assembled, UI-ready campaigns.
    """
    return get_ai_campaign_recommendations()


@router.get("/behavior-signals")
def behavior_signals():
    """
    Explainability endpoint.
    Shows raw detected behavior changes per customer.
    """
    return {
        "signals": detect_behavior_changes()
    }


@router.get("/segments")
def segmentation_summary():
    """
    Returns customer segmentation summary.
    Useful for analytics & drill-downs.
    """
    return segment_customers()
