# agents/strategy_agent.py

from agents.segmentation_agent import segment_customers


def recommend_campaign_strategies() -> list[dict]:
    """
    Recommend campaign strategies per behavioral segment.
    Output is explainable, demo-safe, and ready for message/ROI agents.
    """

    segments = segment_customers()
    strategies: list[dict] = []

    for segment_id, segment_data in segments.items():
        customers = segment_data.get("customers", [])
        if not customers:
            continue

        segment_name = segment_data.get("name", "")
        base_payload = {
            "segment_id": segment_id,
            "segment_name": segment_name,
            "target_customers": customers,
        }

        # ---- High Value - Active ----
        if segment_id == "S1":
            strategies.append({
                **base_payload,
                "campaign_type": "exclusive_offer",
                "channel": "email",
                "priority": "medium",
                "reason": "Active high-value customers respond best to exclusivity and early access",
            })

        # ---- High Value - At Risk ----
        elif segment_id == "S2":
            strategies.append({
                **base_payload,
                "campaign_type": "bonus_points",
                "channel": "sms",
                "priority": "high",
                "reason": "High-value customers showing inactivity respond well to strong incentives",
            })

        # ---- Low Value - Active ----
        elif segment_id == "S3":
            strategies.append({
                **base_payload,
                "campaign_type": "informational",
                "channel": "push",
                "priority": "low",
                "reason": "Engaged low-spend customers can be nudged without monetary incentives",
            })

        # ---- Dormant ----
        elif segment_id == "S4":
            strategies.append({
                **base_payload,
                "campaign_type": "bonus_points",
                "channel": "sms",
                "priority": "high",
                "reason": "Dormant users require strong incentives to re-engage after long inactivity",
            })

        # ---- New Customers ----
        elif segment_id == "S5":
            strategies.append({
                **base_payload,
                "campaign_type": "welcome",
                "channel": "email",
                "priority": "medium",
                "reason": "New customers should be onboarded with a light welcome experience",
            })

    return strategies
