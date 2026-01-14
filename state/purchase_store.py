# state/purchase_store.py

from typing import List
import json
import os

DATA_PATH = "data/snapshots/purchases.json"

# In-memory store
PURCHASE_STORE: List[dict] = []

REQUIRED_FIELDS = {
    "customer_id",
    "date",
    "order_value",
    "product_category",
}


def load_purchases() -> List[dict]:
    """
    Load purchases from snapshot file into memory.
    """
    PURCHASE_STORE.clear()

    if not os.path.exists(DATA_PATH):
        return []

    with open(DATA_PATH, "r") as f:
        data = json.load(f)

    for purchase in data:
        PURCHASE_STORE.append(purchase)

    return PURCHASE_STORE


def persist_purchases():
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w") as f:
        json.dump(PURCHASE_STORE, f, indent=2)


def add_purchase(purchase: dict):
    missing = REQUIRED_FIELDS - purchase.keys()
    if missing:
        raise ValueError(f"Missing fields: {missing}")

    PURCHASE_STORE.append(purchase)
    persist_purchases()


def get_all_purchases() -> List[dict]:
    return PURCHASE_STORE
