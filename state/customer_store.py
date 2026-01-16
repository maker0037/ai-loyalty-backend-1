from typing import Dict, List, Optional
import json
import os
from datetime import datetime

DATA_PATH = "data/snapshots/customers.json"

CUSTOMER_STORE: Dict[str, dict] = {}

# AI-required fields (DO NOT TOUCH)
REQUIRED_FIELDS = {
    "customer_id",
    "age",
    "city",
    "signup_channel",
    "preferred_channel",
    "loyalty_tier",
}


def load_customers() -> List[dict]:
    CUSTOMER_STORE.clear()

    if not os.path.exists(DATA_PATH):
        return []

    with open(DATA_PATH, "r") as f:
        data = json.load(f)

    for customer_id, customer in data.items():
        # ---- UI defaults (non-breaking) ----
        customer.setdefault("first_name", "")
        customer.setdefault("last_name", "")
        customer.setdefault("mobile_number", None)
        customer.setdefault("points_balance", 0)
        customer.setdefault("enabled", True)
        customer.setdefault("created_at", datetime.utcnow().date().isoformat())

        CUSTOMER_STORE[customer_id] = customer

    return list(CUSTOMER_STORE.values())


def persist_customers():
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w") as f:
        json.dump(CUSTOMER_STORE, f, indent=2)


def add_customer(customer: dict):
    missing = REQUIRED_FIELDS - customer.keys()
    if missing:
        raise ValueError(f"Missing fields: {missing}")

    customer.setdefault("created_at", datetime.utcnow().date().isoformat())
    customer.setdefault("enabled", True)
    customer.setdefault("points_balance", 0)

    CUSTOMER_STORE[customer["customer_id"]] = customer
    persist_customers()


def get_all_customers() -> List[dict]:
    return list(CUSTOMER_STORE.values())


def get_customer_by_id(customer_id: str) -> Optional[dict]:
    return CUSTOMER_STORE.get(customer_id)
