# agents/autonomy_agent.py

from agents.policy_guard_agent import validate_autonomous_adjustment


def should_auto_launch(campaign_preview: dict, learning_signal: dict | None) -> bool:
    """
    Decide if AI can autonomously launch this campaign.
    """

    if campaign_preview["estimated_cost"] > 0:
        return False

    if campaign_preview["channel"] not in {"push", "email"}:
        return False

    if learning_signal and not validate_autonomous_adjustment(learning_signal):
        return False

    return True
