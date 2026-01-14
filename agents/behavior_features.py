from datetime import datetime, timedelta
from collections import Counter
from state.purchase_store import get_all_purchases


def _parse_date(date_str: str) -> datetime | None:
    """
    Safely parse ISO date strings.
    Returns None if parsing fails.
    """
    try:
        return datetime.fromisoformat(date_str)
    except Exception:
        return None


def extract_customer_features(customer_id: str) -> dict:
    """
    Convert raw purchase data into numerical behavioral signals
    used by downstream agents.
    """

    all_purchases = get_all_purchases()

    purchases = [
        p for p in all_purchases
        if p.get("customer_id") == customer_id
    ]

    # ---- No purchase case (cold start) ----
    if not purchases:
        return {
            "total_purchase_count": 0,
            "total_spend": 0,
            "purchase_count_30d": 0,
            "avg_order_value": 0,
            "days_since_last_purchase": 9999,  # sentinel for "never purchased"
            "dominant_category": None,
        }

    now = datetime.utcnow()
    last_30_days = now - timedelta(days=30)

    parsed_purchases = []

    for p in purchases:
        parsed_date = _parse_date(p.get("date"))
        if not parsed_date:
            continue  # skip bad records safely

        parsed_purchases.append({
            **p,
            "_parsed_date": parsed_date
        })

    if not parsed_purchases:
        # All purchases had invalid dates
        return {
            "total_purchase_count": len(purchases),
            "total_spend": sum(p.get("order_value", 0) for p in purchases),
            "purchase_count_30d": 0,
            "avg_order_value": 0,
            "days_since_last_purchase": 9999,
            "dominant_category": None,
        }

    # ---- Core metrics ----
    total_purchase_count = len(parsed_purchases)
    total_spend = sum(p.get("order_value", 0) for p in parsed_purchases)

    avg_order_value = total_spend / total_purchase_count

    recent_purchases = [
        p for p in parsed_purchases
        if p["_parsed_date"] >= last_30_days
    ]

    purchase_count_30d = len(recent_purchases)

    last_purchase_date = max(
        p["_parsed_date"] for p in parsed_purchases
    )

    days_since_last_purchase = (now - last_purchase_date).days

    dominant_category = Counter(
        p.get("product_category") for p in parsed_purchases
        if p.get("product_category")
    ).most_common(1)[0][0]

    return {
        "total_purchase_count": total_purchase_count,
        "total_spend": round(total_spend, 2),
        "purchase_count_30d": purchase_count_30d,
        "avg_order_value": round(avg_order_value, 2),
        "days_since_last_purchase": days_since_last_purchase,
        "dominant_category": dominant_category,
    }
