from datetime import datetime, timedelta
from state.engagement_store import get_engagements
from services.simulation_service import simulate_engagement_once


def refresh_campaign_metrics(campaign: dict) -> dict:
    """
    Refresh metrics dynamically.
    Adds time-based engagement growth.
    """

    engagements = get_engagements(campaign["campaign_id"])

    # Time-based growth: simulate once every 60 seconds
    last_updated = campaign["metrics"].get("last_updated")

    should_grow = False
    if not engagements:
        should_grow = True
    elif last_updated:
        last_time = datetime.fromisoformat(last_updated)
        if datetime.utcnow() - last_time > timedelta(seconds=60):
            should_grow = True

    if should_grow:
        simulate_engagement_once(campaign)
        engagements = get_engagements(campaign["campaign_id"])

    participants = 0
    revenue = 0.0

    for e in engagements:
        if e["event_type"] == "conversion":
            participants += 1
            revenue += e["value"]

    cost = campaign["estimated_cost"]
    actual_roi = round((revenue - cost) / cost, 2) if cost > 0 else 0.0

    campaign["metrics"] = {
        "participants": participants,
        "revenue": round(revenue, 2),
        "actual_roi": actual_roi,
        "last_updated": datetime.utcnow().isoformat(),
        "explanation": "Metrics updated via simulated engagement growth.",
    }

    return campaign
