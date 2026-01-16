# services/learning_service.py

from agents.learning_agent import derive_learning_signal
from agents.policy_guard_agent import validate_autonomous_adjustment
from state.learning_store import update_learning


def process_campaign_learning(campaign: dict):
    """
    Apply safe learning updates based on performance.
    """

    signal = derive_learning_signal(campaign)

    if signal["status"] == "insufficient_data":
        return {"status": "skipped"}

    if not validate_autonomous_adjustment(signal):
        return {"status": "rejected", "reason": "policy_guard"}

    update_learning(
        segment_id=campaign["segment_id"],
        adjustment=signal,
    )

    return {"status": "applied", "signal": signal}
