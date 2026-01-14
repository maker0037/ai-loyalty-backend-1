# agents/campaign_economics.py

# --- Assumptions (demo-safe, explainable) ---
SMS_COST = 0.5
EMAIL_COST = 0.1
PUSH_COST = 0.05

POINT_VALUE = 0.01  # 1 point = ₹0.01
AVG_ORDER_VALUE_DEFAULT = 800


def estimate_campaign_cost(
    channel: str,
    target_size: int,
    points: int,
) -> float:
    """
    Estimate total campaign cost based on channel and incentives.
    """

    # Channel cost
    if channel == "sms":
        channel_cost = SMS_COST * target_size
    elif channel == "email":
        channel_cost = EMAIL_COST * target_size
    elif channel == "push":
        channel_cost = PUSH_COST * target_size
    else:
        channel_cost = 0

    # Incentive cost
    incentive_cost = target_size * points * POINT_VALUE

    total_cost = channel_cost + incentive_cost
    return round(total_cost, 2)
