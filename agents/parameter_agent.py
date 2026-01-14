# agents/parameter_agent.py

from agents.campaign_economics import AVG_ORDER_VALUE_DEFAULT


def recommend_campaign_parameters(strategy: dict) -> dict:
    """
    Recommend concrete campaign parameters in a simple, explainable way.
    Parameters are conservative, segment-aware, and demo-safe.
    """

    target_customers = strategy.get("target_customers", [])
    segment_size = len(target_customers)
    campaign_type = strategy.get("campaign_type", "")

    # ---- Defaults ----
    points = 0
    duration_days = 5
    expected_avg_order_value = AVG_ORDER_VALUE_DEFAULT

    # ---- Bonus Points Campaign ----
    if campaign_type == "bonus_points":
        # Smaller segments → stronger incentive
        if segment_size <= 10:
            points = 150
            duration_days = 7
        elif segment_size <= 50:
            points = 100
            duration_days = 7
        else:
            points = 50
            duration_days = 10

    # ---- Exclusive / Welcome Campaigns ----
    elif campaign_type in {"exclusive_offer", "welcome"}:
        points = 0
        duration_days = 10

    # ---- Informational Campaign ----
    elif campaign_type == "informational":
        points = 0
        duration_days = 5

    return {
        "points": points,
        "duration_days": duration_days,
        "target_size": segment_size,
        "expected_avg_order_value": expected_avg_order_value,
    }
