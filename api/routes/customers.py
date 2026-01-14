# api/routes/customers.py

from fastapi import APIRouter, HTTPException
from state.customer_store import add_customer, get_all_customers

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("/")
def list_customers():
    """
    Return all customers currently loaded in memory.
    Used by UI & AI pipeline.
    """
    return {
        "count": len(get_all_customers()),
        "customers": get_all_customers(),
    }


@router.post("/")
def create_customer(customer: dict):
    """
    Add a new customer (manual UI entry or demo).
    """
    try:
        add_customer(customer)
        return {
            "status": "success",
            "customer_id": customer["customer_id"],
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
