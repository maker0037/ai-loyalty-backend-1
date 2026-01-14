# state/customer_store.py

from typing import Dict, List
import json
import os

DATA_PATH = "data/snapshots/customers.json"

# In-memory store
CUSTOMER_STORE: Dict[str, dict] = {}

REQUIRED_FIELDS = {
    "customer_id",
    "age",
    "city",
    "signup_channel",
    "preferred_channel",
    "loyalty_tier",
}


def load_customers() -> List[dict]:
    """
    Load customers from snapshot file into memory.
    Safe to call multiple times.
    """
    CUSTOMER_STORE.clear()

    if not os.path.exists(DATA_PATH):
        return []

    with open(DATA_PATH, "r") as f:
        data = json.load(f)

    for customer_id, customer in data.items():
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

    CUSTOMER_STORE[customer["customer_id"]] = customer
    persist_customers()


def get_all_customers() -> List[dict]:
    return list(CUSTOMER_STORE.values())
