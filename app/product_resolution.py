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

    products = find_products_by_name(
        product_name,
        store_id=store_id
    )

    # Apply brand filtering when a brand is provided.
    if brand:
        brand_matches = [
            product
            for product in products
            if normalize_text(product["brand"]) == normalize_text(brand)
        ]

        if brand_matches:
            products = brand_matches

    # No matching products.
    if not products:
        return {
            "status": "not_found",
            "matches": []
        }

    # If a size was provided, resolve it before
    # checking whether the product name is ambiguous.
    if size:
        normalized_size = normalize_text(size)

        for product in products:

            if normalize_text(product["size"]) == normalized_size:

                return {
                    "status": "success",
                    "product": product
                }

        # Product exists, but requested size does not.
        return {
            "status": "size_not_found",
            "matches": products
        }

    # No size was provided and multiple sizes exist.
    if len(products) > 1:
        return {
            "status": "ambiguous",
            "matches": products
        }

    # Exactly one product exists.
    return {
        "status": "success",
        "product": products[0]
    }