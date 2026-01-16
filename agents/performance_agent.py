# agents/performance_agent.py

from state.purchase_store import get_all_purchases
from agents.roi_agent import estimate_campaign_roi


def evaluate_campaign_performance(campaign: dict) -> dict:
    """
    Compare actual outcomes vs AI estimates for a campaign.
    """

    segment_id = campaign["segment_id"]
    purchases = get_all_purchases()

    # ---- Simulated attribution (Phase 3-safe) ----
    attributed_purchases = [
        p for p in purchases
        if p["customer_id"] in campaign.get("segment_customers", [])
    ]

    participants = len(set(p["customer_id"] for p in attributed_purchases))
    revenue = sum(p["order_value"] for p in attributed_purchases)

    # ---- Actual ROI ----
    cost = campaign["estimated_cost"]
    if cost > 0:
        actual_roi = round((revenue - cost) / cost, 2)
    else:
        actual_roi = 0.0

    # ---- Explanation (no LLM yet) ----
    explanation = (
        "Performance aligned with expectations."
        if actual_roi >= campaign["projected_roi"]
        else "Lower participation than expected reduced ROI."
    )

    return {
        "participants": participants,
        "revenue": revenue,
        "actual_roi": actual_roi,
        "explanation": explanation,
    }
