from fastapi import APIRouter
from state.purchase_store import get_all_purchases
from state.customer_store import get_customer_by_id

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("/")
def list_transactions():
    purchases = get_all_purchases()
    items = []

    for p in purchases:
        customer = get_customer_by_id(p["customer_id"])

        items.append({
            "transaction_id": p["transaction_id"],
            "date": p["date"],
            "member_card": p["card_number"],
            "member_mobile": customer["mobile_number"] if customer else None,
            "member_tier": customer["loyalty_tier"].upper() if customer else "UNKNOWN",
            "point_of_sale": p["store_name"],
            "pos_type": p["pos_type"],
            "amount": p["order_value"],
        })

    return {
        "count": len(items),
        "items": items
    }
