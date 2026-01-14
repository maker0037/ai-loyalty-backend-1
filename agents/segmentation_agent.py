# agents/segmentation_agent.py

from state.customer_store import get_all_customers
from agents.behavior_features import extract_customer_features


# --- Tunable, explainable thresholds ---
HIGH_VALUE_AOV = 800
VERY_HIGH_VALUE_SPEND = 3000
ACTIVE_PURCHASES_30D = 2
DORMANT_DAYS = 45
AT_RISK_DAYS = 20


def segment_customers() -> dict:
    """
    Segment customers into homogeneous, actionable behavioral groups.
    Segmentation is rule-based, explainable, and demo-safe.
    """

    segments = {
        "S1": {
            "name": "High Value - Active",
            "customers": [],
            "description": "High spenders with recent and frequent purchases",
        },
        "S2": {
            "name": "High Value - At Risk",
            "customers": [],
            "description": "High spenders showing declining or no recent activity",
        },
        "S3": {
            "name": "Low Value - Active",
            "customers": [],
            "description": "Recently active customers with low average spend",
        },
        "S4": {
            "name": "Dormant",
            "customers": [],
            "description": "Customers with long inactivity or no meaningful engagement",
        },
        "S5": {
            "name": "New Customers",
            "customers": [],
            "description": "Recently acquired customers with very limited history",
        },
    }

    customers = get_all_customers()
    if not customers:
        return segments

    for customer in customers:
        customer_id = customer.get("customer_id")
        if not customer_id:
            continue

        features = extract_customer_features(customer_id)

        total_spend = features.get("total_spend", 0)
        avg_order = features.get("avg_order_value", 0)
        purchase_count_30d = features.get("purchase_count_30d", 0)
        total_purchase_count = features.get("total_purchase_count", 0)
        days_since_last = features.get("days_since_last_purchase", 9999)

        # ---- Segment: New Customers ----
        if total_purchase_count <= 1 and days_since_last <= 14:
            segments["S5"]["customers"].append(customer_id)
            continue

        # ---- Segment: Dormant ----
        if days_since_last > DORMANT_DAYS:
            segments["S4"]["customers"].append(customer_id)
            continue

        # ---- High-value determination (robust) ----
        is_high_value = (
            avg_order >= HIGH_VALUE_AOV
            or total_spend >= VERY_HIGH_VALUE_SPEND
        )

        # ---- Activity determination ----
        is_active = purchase_count_30d >= ACTIVE_PURCHASES_30D

        # ---- High Value - Active ----
        if is_high_value and is_active:
            segments["S1"]["customers"].append(customer_id)

        # ---- High Value - At Risk ----
        elif is_high_value and not is_active and days_since_last >= AT_RISK_DAYS:
            segments["S2"]["customers"].append(customer_id)

        # ---- Low Value - Active ----
        elif not is_high_value and is_active:
            segments["S3"]["customers"].append(customer_id)

        # ---- Fallback ----
        else:
            segments["S4"]["customers"].append(customer_id)

    return segments
