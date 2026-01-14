# agents/orchestrator.py

"""
Campaign Orchestrator
---------------------
This module is the single entry point that coordinates all agents
to produce final, UI-ready campaign recommendations.

Pipeline order:
1. Segmentation
2. Strategy recommendation
3. Behavior insight (LLM explainability)
4. Message generation (LLM copy)
5. Parameter recommendation
6. Campaign economics & ROI estimation

This file should NOT contain business logic.
It only orchestrates agents and assembles outputs.
"""

from agents.strategy_agent import recommend_campaign_strategies
from agents.message_agent import generate_campaign_messages
from agents.parameter_agent import recommend_campaign_parameters
from agents.roi_agent import estimate_campaign_roi
from agents.behavior_insight_agent import generate_behavior_insights


def generate_campaign_recommendations() -> list[dict]:
    """
    Generate fully assembled campaign recommendations.
    Output is stable, explainable, and frontend-ready.
    """

    campaigns: list[dict] = []

    # --- Run upstream agents ---
    strategies = recommend_campaign_strategies()
    messages = generate_campaign_messages()
    insights = generate_behavior_insights()

    # Map (segment_id → message)
    message_map = {
        m["segment_id"]: m
        for m in messages
    }

    for strategy in strategies:
        segment_id = strategy["segment_id"]

        # ---- Message ----
        message_payload = message_map.get(segment_id)
        if not message_payload:
            # Skip if message generation failed
            continue

        # ---- Parameters ----
        parameters = recommend_campaign_parameters(strategy)

        # ---- ROI ----
        roi = estimate_campaign_roi(
            channel=strategy["channel"],
            target_size=parameters["target_size"],
            points=parameters["points"],
            expected_avg_order_value=parameters["expected_avg_order_value"],
            campaign_type=strategy["campaign_type"],
        )

        # ---- Assemble final campaign ----
        campaigns.append({
            "campaign_id": f"CMP_{segment_id}",
            "segment_id": segment_id,
            "segment": strategy["segment_name"],
            "target_customers": strategy["target_customers"],

            # Strategy
            "campaign_type": strategy["campaign_type"],
            "channel": strategy["channel"],
            "priority": strategy.get("priority", "medium"),
            "reason": strategy["reason"],

            # Insight (AI explanation)
            "insight": insights.get(
                segment_id,
                "Behavioral patterns indicate this segment may benefit from targeted engagement."
            ),

            # Message
            "message": message_payload["message"],

            # Parameters
            "parameters": parameters,

            # ROI & economics
            "roi_estimation": roi,

            # Lifecycle
            "status": "AI_RECOMMENDED",
        })

    return campaigns
