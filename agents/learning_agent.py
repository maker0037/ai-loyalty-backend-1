# agents/learning_agent.py

def derive_learning_signal(campaign: dict) -> dict:
    """
    Derive adjustment signals from campaign performance.
    No direct mutation happens here.
    """

    projected = campaign["projected_roi"]
    actual = campaign["metrics"]["actual_roi"]

    if actual is None:
        return {"status": "insufficient_data"}

    delta = round(actual - projected, 2)

    signal = {
        "campaign_id": campaign["campaign_id"],
        "delta_roi": delta,
        "direction": "positive" if delta > 0 else "negative",
        "confidence": abs(delta),
    }

    return signal
