from products import search_products


print("TEST: Product search")

results = search_products("Apple Purity")

print(f"\nFound {len(results)} products:\n")

for product in results:
    print(
        f"{product['product_name']} | "
        f"{product['size']} | "
        f"{product['brand']} | "
        f"{product['aisle']} | "
        f"ID: {product['product_id']}"
    )