# agents/policy_guard_agent.py

def validate_autonomous_adjustment(adjustment: dict) -> bool:
    """
    Ensure AI does not exceed safe boundaries.
    """

    if adjustment.get("confidence", 0) < 0.2:
        return False

    if abs(adjustment.get("delta_roi", 0)) > 2.0:
        return False

    return True
