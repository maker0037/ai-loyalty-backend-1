from typing import List
import json
import os
from uuid import uuid4

DATA_PATH = "data/snapshots/purchases.json"

PURCHASE_STORE: List[dict] = []

REQUIRED_FIELDS = {
    "customer_id",
    "date",
    "order_value",
    "product_category",
}


def load_purchases() -> List[dict]:
    PURCHASE_STORE.clear()

    if not os.path.exists(DATA_PATH):
        return []

    with open(DATA_PATH, "r") as f:
        data = json.load(f)

    for purchase in data:
        # ---- UI defaults ----
        purchase.setdefault("transaction_id", f"TXN_{uuid4().hex[:6].upper()}")
        purchase.setdefault("store_name", "Unknown Store")
        purchase.setdefault("pos_type", "Retail")
        purchase.setdefault("card_number", "XXXX-XXXX-XXXX")

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

    purchase.setdefault("transaction_id", f"TXN_{uuid4().hex[:6].upper()}")
    purchase.setdefault("store_name", "Unknown Store")
    purchase.setdefault("pos_type", "Retail")
    purchase.setdefault("card_number", "XXXX-XXXX-XXXX")

    PURCHASE_STORE.append(purchase)
    persist_purchases()


def get_all_purchases() -> List[dict]:
    return PURCHASE_STORE
