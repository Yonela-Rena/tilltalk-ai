from app.query_parser import parse_query
from app.product_resolution import resolve_product
from app.products import get_current_price


def answer_parsed_query(
    parsed_query,
    store_id=1,
    check_date=None
):
    """
    Process an already-parsed product request.

    This function does not call Gemini.
    It handles product resolution and verified price lookup.
    """

    product_name = parsed_query.get("product_name")
    brand = parsed_query.get("brand")
    size = parsed_query.get("size")

    if not product_name:
        return {
            "status": "needs_clarification",
            "message": "I need the product name to check the price."
        }

    resolution = resolve_product(
        product_name=product_name,
        brand=brand,
        size=size,
        store_id=store_id
    )

    if resolution["status"] == "not_found":
        return {
            "status": "not_found",
            "message": (
                f"I couldn't find {product_name} "
                "in the catalogue."
            ),
            "product_name": product_name,
            "brand": brand
        }

    if resolution["status"] == "ambiguous":
        available_sizes = [
            product["size"]
            for product in resolution["matches"]
        ]

        return {
            "status": "needs_clarification",
            "message": (
                f"I found {product_name} in multiple sizes. "
                "Which size do you need?"
            ),
            "product_name": product_name,
            "brand": brand,
            "available_sizes": available_sizes
        }

    if resolution["status"] == "size_not_found":
        available_sizes = [
            product["size"]
            for product in resolution["matches"]
        ]

        return {
            "status": "size_not_found",
            "message": (
                f"I couldn't find {product_name} "
                f"in {size}. Available sizes are: "
                f"{', '.join(available_sizes)}."
            ),
            "product_name": product_name,
            "brand": brand,
            "requested_size": size,
            "available_sizes": available_sizes
        }

    product = resolution["product"]

    price_info = get_current_price(
        product_id=product["product_id"],
        store_id=store_id,
        check_date=check_date
    )

    if not price_info:
        return {
            "status": "price_not_found",
            "message": (
                f"I found {product['product_name']} "
                f"({product['size']}), but there is no "
                "current price available."
            ),
            "product_name": product["product_name"],
            "brand": product["brand"],
            "size": product["size"]
        }

    return {
        "status": "success",
        "product_name": product["product_name"],
        "brand": product["brand"],
        "size": product["size"],
        "aisle": product["aisle"],
        "price": price_info["price"],
        "price_type": price_info["price_type"],
        "promotion_description": price_info["description"]
    }


def answer_price_query(
    query,
    store_id=1,
    check_date=None
):
    """
    Process a cashier's natural-language price query.

    Gemini understands the request.
    SQLite provides the verified price.
    """

    parsed_query = parse_query(query)

    return answer_parsed_query(
        parsed_query=parsed_query,
        store_id=store_id,
        check_date=check_date
    )