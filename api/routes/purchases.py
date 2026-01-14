# api/routes/purchases.py

from fastapi import APIRouter, HTTPException
from state.purchase_store import add_purchase, get_all_purchases

router = APIRouter(prefix="/purchases", tags=["Purchases"])


@router.get("/")
def list_purchases():
    """
    Return all purchase events.
    """
    return {
        "count": len(get_all_purchases()),
        "purchases": get_all_purchases(),
    }


@router.post("/")
def create_purchase(purchase: dict):
    """
    Add a new purchase event.
    Used for demo ingestion & testing AI reactions.
    """
    try:
        add_purchase(purchase)
        return {"status": "success"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
