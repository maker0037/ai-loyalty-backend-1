# agents/roi_agent.py

from agents.campaign_economics import estimate_campaign_cost


def estimate_campaign_roi(
    *,
    channel: str,
    target_size: int,
    points: int,
    expected_avg_order_value: float,
    campaign_type: str,
) -> dict:
    """
    Estimate participation, revenue, cost, and ROI for a campaign.
    """

    # ---- Participation heuristics (simple & explainable) ----
    if campaign_type == "bonus_points":
        participation_rate = 0.30
    elif campaign_type == "exclusive_offer":
        participation_rate = 0.25
    elif campaign_type == "welcome":
        participation_rate = 0.35
    elif campaign_type == "informational":
        participation_rate = 0.15
    else:
        participation_rate = 0.10

    estimated_participants = int(target_size * participation_rate)

    # ---- Revenue estimation ----
    estimated_incremental_revenue = round(
        estimated_participants * expected_avg_order_value,
        2,
    )

    # ---- Cost estimation ----
    estimated_campaign_cost = estimate_campaign_cost(
        channel=channel,
        target_size=target_size,
        points=points,
    )

    # ---- ROI calculation ----
    if estimated_campaign_cost > 0:
        estimated_roi = round(
            (estimated_incremental_revenue - estimated_campaign_cost)
            / estimated_campaign_cost,
            2,
        )
    else:
        estimated_roi = 0.0

    return {
        "estimated_participation_rate": participation_rate,
        "estimated_participants": estimated_participants,
        "estimated_campaign_cost": estimated_campaign_cost,
        "estimated_incremental_revenue": estimated_incremental_revenue,
        "estimated_roi": estimated_roi,
    }
