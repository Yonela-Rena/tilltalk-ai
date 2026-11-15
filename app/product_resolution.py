
from app.products import (
    find_products_by_name,
    normalize_text
)


def resolve_product(
    product_name,
    brand=None,
    size=None,
    store_id=1
):
    """
    Resolve a product using product name,
    optional brand, and optional size.
    """

    # Find products matching the requested name.
    products = find_products_by_name(
        product_name,
        store_id=store_id
    )

    # If a brand was provided, keep only products
    # that match that brand.
    if brand:
        products = [
            product for product in products
            if normalize_text(product["brand"])
            == normalize_text(brand)
        ]

    # No matching products.
    if not products:
        return {
            "status": "not_found",
            "matches": []
        }

    # If a size was provided, find the exact size.
    if size:
        normalized_size = normalize_text(size)

        for product in products:
            if normalize_text(product["size"]) == normalized_size:
                return {
                    "status": "success",
                    "product": product
                }

        # The product exists, but not in the requested size.
        return {
            "status": "size_not_found",
            "matches": products
        }

    # No size was provided and multiple products match.
    if len(products) > 1:
        return {
            "status": "ambiguous",
            "matches": products
        }

    # Exactly one product matches.
    return {
        "status": "success",
        "product": products[0]
    }
