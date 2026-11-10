
import json
from pathlib import Path

from agent_framework import tool


DATA_FILE = Path(__file__).parent / "products.json"


def load_products():
    """Load products from the JSON file."""
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# Tool 1: Inventory Agent - Search Products
@tool(approval_mode="never_require")
def search_products(topic: str) -> str:
    """Find products matching a topic, category, or title."""

    print(f"[TOOL CALLED] search_products: {topic}")

    products = load_products()

    matches = [
        product for product in products
        if topic.lower() in product.get("name", "").lower()
        or topic.lower() in product.get("category", "").lower()
        or topic.lower() in product.get("description", "").lower()
    ]

    if not matches:
        return json.dumps({
            "status": "not_found",
            "message": f"No products found for {topic}."
        })

    return json.dumps(matches, ensure_ascii=False)


# Tool 2: Pricing Agent - Calculate Order Total
@tool(approval_mode="never_require")
def calculate_order_total(product_id: str, quantity: int) -> str:
    """Calculate total order price after validating stock availability."""

    print(
        f"[TOOL CALLED] calculate_order_total: "
        f"{product_id}, {quantity}"
    )

    if quantity < 1:
        return json.dumps({
            "status": "invalid_quantity",
            "message": "Quantity must be at least 1."
        })

    products = load_products()

    for product in products:

        if product.get("id", "").upper() == product_id.upper():

            stock = product.get("stock", 0)
            price = product.get("price_inr", 0)

            if quantity > stock:
                return json.dumps({
                    "status": "insufficient_stock",
                    "product_id": product_id,
                    "available_stock": stock,
                    "requested_quantity": quantity,
                    "message": "Requested quantity exceeds available stock."
                })

            total = price * quantity

            return json.dumps({
                "status": "success",
                "product_id": product["id"],
                "name": product.get("name", "Unknown"),
                "quantity": quantity,
                "available_stock": stock,
                "price_per_item": price,
                "total_price": total,
                "currency": "INR"
            }, ensure_ascii=False)

    return json.dumps({
        "status": "not_found",
        "message": f"Product ID {product_id} not found."
    })
