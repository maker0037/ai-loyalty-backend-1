# services/engagement_simulator.py

import random
from state.engagement_store import record_engagement


def simulate_engagement(campaign: dict):
    """
    Fake engagement for demo purposes.
    Deterministic enough to look realistic.
    """

    audience = campaign["audience_size"]

    # Simple heuristics
    open_rate = 0.6
    click_rate = 0.3
    conversion_rate = 0.15

    opens = int(audience * open_rate)
    clicks = int(opens * click_rate)
    conversions = int(clicks * conversion_rate)

    for _ in range(opens):
        record_engagement(campaign["campaign_id"], "open")

    for _ in range(clicks):
        record_engagement(campaign["campaign_id"], "click")

    avg_order_value = 1200

    for _ in range(conversions):
        record_engagement(
            campaign["campaign_id"],
            "conversion",
            value=avg_order_value,
        )

    return {
        "opens": opens,
        "clicks": clicks,
        "conversions": conversions,
        "revenue": conversions * avg_order_value,
    }
