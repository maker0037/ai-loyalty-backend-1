# agents/behavior_change_agent.py

from agents.behavior_features import extract_customer_features
from state.customer_store import get_all_customers

INACTIVITY_DAYS_THRESHOLD = 14
LOW_ACTIVITY_THRESHOLD = 1


def detect_behavior_changes() -> list[dict]:
    """
    Detect meaningful behavioral changes for customers based on
    extracted behavioral features.
    """
    signals: list[dict] = []

    customers = get_all_customers()
    if not customers:
        return signals

    for customer in customers:
        customer_id = customer.get("customer_id")
        if not customer_id:
            continue

        features = extract_customer_features(customer_id)

        days_since_last = features.get("days_since_last_purchase", 9999)
        purchase_count_30d = features.get("purchase_count_30d", 0)

        # Rule 1: Inactivity
        if days_since_last > INACTIVITY_DAYS_THRESHOLD:
            signals.append({
                "customer_id": customer_id,
                "signal": "inactivity",
                "severity": "high",
                "features": features,
            })

        # Rule 2: Low recent activity (but not completely inactive)
        if purchase_count_30d <= LOW_ACTIVITY_THRESHOLD and days_since_last <= INACTIVITY_DAYS_THRESHOLD:
            signals.append({
                "customer_id": customer_id,
                "signal": "low_activity",
                "severity": "medium",
                "features": features,
            })

    return signals
