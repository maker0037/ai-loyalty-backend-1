# api/routes/customers.py

from fastapi import APIRouter
from state.customer_store import get_all_customers

router = APIRouter(tags=["Customers"])




@router.get("/")
def list_members():
    customers = get_all_customers()
    items = []

    for c in customers:
        items.append({
            "id": c["customer_id"],
            "creation_date": c["created_at"],
            "firstname": c["first_name"],
            "lastname": c["last_name"],
            "mobile_number": c["mobile_number"],
            "tier": c["loyalty_tier"].upper(),
            "points_balance": c["points_balance"],
            "status": "active" if c["enabled"] else "inactive",
        })

    return {
        "count": len(items),
        "items": items
    }
