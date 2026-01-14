# services/campaign_service.py

from datetime import datetime

from agents.orchestrator import generate_campaign_recommendations
from state.campaign_store import save_campaigns, get_all_campaigns


def get_ai_campaign_recommendations(force_refresh: bool = False) -> dict:
    """
    Entry point for AI-generated campaign recommendations.

    - Runs full AI pipeline via orchestrator
    - Persists campaigns in state
    - Returns UI-ready response with metadata
    """

    # Optional cache behavior (useful later)
    if not force_refresh:
        existing = get_all_campaigns()
        if existing:
            return {
                "meta": {
                    "total_campaigns": len(existing),
                    "generated_at": None,
                    "source": "cached",
                },
                "campaigns": existing,
            }

    # Run AI orchestration
    campaigns = generate_campaign_recommendations()

    # Persist results
    save_campaigns(campaigns)

    # Aggregate economics for UI KPIs
    total_cost = sum(
        c["roi_estimation"]["estimated_campaign_cost"]
        for c in campaigns
    )

    avg_roi = (
        round(
            sum(c["roi_estimation"]["estimated_roi"] for c in campaigns)
            / len(campaigns),
            2,
        )
        if campaigns
        else 0
    )

    return {
        "meta": {
            "total_campaigns": len(campaigns),
            "estimated_total_cost": round(total_cost, 2),
            "average_estimated_roi": avg_roi,
            "generated_at": datetime.utcnow().isoformat(),
            "source": "ai_orchestrator_v1",
        },
        "campaigns": campaigns,
    }
