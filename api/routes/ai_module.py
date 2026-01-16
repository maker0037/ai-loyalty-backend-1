# api/routes/ai_module.py

from fastapi import APIRouter

from agents.orchestrator import generate_campaign_recommendations

router = APIRouter(prefix="/ai", tags=["AI"])


@router.get("/suggestions")
def ai_suggestions():
    """
    UI-facing AI Intelligence Hub endpoint.
    """
    campaigns = generate_campaign_recommendations()
    items = []

    for c in campaigns:
        items.append({
            "segment_id": c["segment_id"],
            "detected_behavior": {
                "label": c["campaign_type"].replace("_", " ").title(),
                "type": c["campaign_type"],
            },
            "suggested_campaign": {
                "name": c["segment"],
                "channel": c["channel"],
            },
            "estimated_roi": c["roi_estimation"]["estimated_roi"],
        })

    return {
        "items": items
    }
