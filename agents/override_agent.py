# agents/override_agent.py

def record_override(original: dict, overridden: dict) -> dict:
    """
    Capture how humans modify AI recommendations.
    """

    changes = {}

    for key in overridden:
        if original.get(key) != overridden.get(key):
            changes[key] = {
                "ai": original.get(key),
                "human": overridden.get(key),
            }

    return {
        "campaign_id": original["campaign_id"],
        "changes": changes,
        "override_strength": len(changes),
    }
