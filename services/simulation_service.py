# services/simulation_service.py

from datetime import datetime
from state.engagement_store import record_engagement


def simulate_engagement_once(campaign: dict) -> dict:
    """
    Simulate one round of engagement events.
    Safe to call multiple times.
    """

    audience = campaign["audience_size"]

    # Tunable demo heuristics
    open_rate = 0.5
    click_rate = 0.3
    conversion_rate = 0.2
    avg_order_value = 1200

    opens = max(1, int(audience * open_rate))
    clicks = max(1, int(opens * click_rate))
    conversions = max(1, int(clicks * conversion_rate))

    for _ in range(opens):
        record_engagement(campaign["campaign_id"], "open")

    for _ in range(clicks):
        record_engagement(campaign["campaign_id"], "click")

    revenue = 0
    for _ in range(conversions):
        record_engagement(
            campaign["campaign_id"],
            "conversion",
            value=avg_order_value,
        )
        revenue += avg_order_value

    return {
        "simulated_at": datetime.utcnow().isoformat(),
        "opens": opens,
        "clicks": clicks,
        "conversions": conversions,
        "revenue": revenue,
    }
