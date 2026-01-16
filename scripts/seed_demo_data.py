# scripts/seed_demo_data.py

import json
import os
import random
from datetime import datetime, timedelta

CUSTOMER_PATH = "data/snapshots/customers.json"
PURCHASE_PATH = "data/snapshots/purchases.json"

FIRST_NAMES = [
    "Aarav", "Riya", "Kunal", "Ananya", "Vikram", "Neha",
    "Rahul", "Pooja", "Arjun", "Sneha", "Aditya", "Kavya"
]

LAST_NAMES = [
    "Mehta", "Sharma", "Verma", "Gupta", "Malhotra",
    "Singh", "Kaur", "Bansal", "Chopra"
]

CITIES = ["Delhi", "Bangalore", "Mumbai", "Pune", "Chandigarh"]
SIGNUP_CHANNELS = ["website", "mobile_app"]
PREFERRED_CHANNELS = ["email", "sms", "push"]
PRODUCT_CATEGORIES = ["electronics", "fashion", "groceries", "home", "beauty"]


def random_date(days_back: int):
    return (datetime.utcnow() - timedelta(days=random.randint(0, days_back))).date().isoformat()


def generate_customers(count=30):
    customers = {}

    for i in range(1, count + 1):
        cust_id = f"CUST_{i:03d}"

        tier = random.choices(
            ["gold", "silver", "bronze"],
            weights=[0.3, 0.4, 0.3],
        )[0]

        points = {
            "gold": random.randint(2500, 5000),
            "silver": random.randint(500, 2000),
            "bronze": random.randint(0, 500),
        }[tier]

        customers[cust_id] = {
            "customer_id": cust_id,
            "age": random.randint(22, 55),
            "city": random.choice(CITIES),
            "signup_channel": random.choice(SIGNUP_CHANNELS),
            "preferred_channel": random.choice(PREFERRED_CHANNELS),
            "loyalty_tier": tier,

            "first_name": random.choice(FIRST_NAMES),
            "last_name": random.choice(LAST_NAMES),
            "mobile_number": f"+91XXXXXXXX{i:02d}",
            "points_balance": points,
            "enabled": True,
            "created_at": random_date(120),
        }

    return customers


def generate_purchases(customers, target_count=100):
    purchases = []
    txn_id = 1

    customer_ids = list(customers.keys())

    while len(purchases) < target_count:
        cust_id = random.choice(customer_ids)
        tier = customers[cust_id]["loyalty_tier"]

        # Spend behavior by tier
        order_value = {
            "gold": random.randint(1500, 3500),
            "silver": random.randint(500, 1500),
            "bronze": random.randint(200, 700),
        }[tier]

        # Dormant behavior
        days_back = random.choices(
            [10, 30, 90, 180],
            weights=[0.4, 0.3, 0.2, 0.1],
        )[0]

        purchases.append({
            "transaction_id": f"TXN_{txn_id:04d}",
            "customer_id": cust_id,
            "date": random_date(days_back),
            "order_value": order_value,
            "product_category": random.choice(PRODUCT_CATEGORIES),
            "card_number": f"{random.randint(4000,4999)}-XXXX-{random.randint(1000,9999)}",
            "store_name": f"{customers[cust_id]['city']} Store",
            "pos_type": "Retail",
        })

        txn_id += 1

    return purchases


def persist(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    customers = generate_customers(30)
    purchases = generate_purchases(customers, 100)

    persist(CUSTOMER_PATH, customers)
    persist(PURCHASE_PATH, purchases)

    print("✅ Demo data generated successfully")
    print(f"👤 Customers: {len(customers)}")
    print(f"🧾 Purchases: {len(purchases)}")
