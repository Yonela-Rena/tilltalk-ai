from products import find_product_by_name_and_size

print("TEST: Exact product lookup")

product = find_product_by_name_and_size(
    "Apple Purity",
    "200ml"
)

if product:
    print("\nProduct found:")
    print(f"Product: {product['product_name']}")
    print(f"Size: {product['size']}")
    print(f"Brand: {product['brand']}")
    print(f"Product ID: {product['product_id']}")
    print(f"Aisle: {product['aisle']}")
else:
    print("\nProduct not found.")