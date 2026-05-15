"""Generate synthetic e-commerce source data for ingestion."""
import json
import random
from pathlib import Path
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

OUT = Path(__file__).parent.parent / "source_data"
OUT.mkdir(exist_ok=True)

N_CUSTOMERS = 50
N_ORDERS = 200
PRODUCTS = [
    {"sku": "SKU-001", "name": "Wireless Mouse",      "price": 24.99},
    {"sku": "SKU-002", "name": "Mechanical Keyboard", "price": 89.99},
    {"sku": "SKU-003", "name": "USB-C Hub",           "price": 39.99},
    {"sku": "SKU-004", "name": "Monitor Stand",       "price": 49.99},
    {"sku": "SKU-005", "name": "Desk Lamp",           "price": 34.99},
]

customers = [{
    "customer_id":  i,
    "email":        fake.email(),
    "first_name":   fake.first_name(),
    "last_name":    fake.last_name(),
    "country":      fake.country_code(),
    "signed_up_at": fake.date_time_between(start_date="-2y", end_date="-1d").isoformat(),
} for i in range(1, N_CUSTOMERS + 1)]

orders, order_items, oi_id = [], [], 1
for o in range(1, N_ORDERS + 1):
    customer = random.choice(customers)
    orders.append({
        "order_id":    o,
        "customer_id": customer["customer_id"],
        "ordered_at":  fake.date_time_between(start_date="-1y", end_date="now").isoformat(),
        "status":      random.choices(["completed", "pending", "cancelled"],
                                      weights=[0.8, 0.15, 0.05])[0],
    })
    for _ in range(random.randint(1, 4)):
        p = random.choice(PRODUCTS)
        order_items.append({
            "order_item_id": oi_id,
            "order_id":      o,
            "sku":           p["sku"],
            "product_name":  p["name"],
            "unit_price":    p["price"],
            "quantity":      random.randint(1, 3),
        })
        oi_id += 1

(OUT / "customers.json").write_text(json.dumps(customers, indent=2))
(OUT / "orders.json").write_text(json.dumps(orders, indent=2))
(OUT / "order_items.json").write_text(json.dumps(order_items, indent=2))
print(f"Wrote {len(customers)} customers, {len(orders)} orders, {len(order_items)} order items")