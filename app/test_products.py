from products import find_product, find_products_by_name


print("TEST 1: Exact product lookup")

product = find_product("Apple Purity", "200ml")

if product:
    print(f"Product: {product['product_name']}")
    print(f"Size: {product['size']}")
    print(f"Price: R{product['price']}")
    print(f"Aisle: {product['aisle']}")
else:
    print("Product not found.")


print("\nTEST 2: Find all Apple Purity sizes")

products = find_products_by_name("Apple Purity")

for product in products:
    print(
        f"{product['size']} - "
        f"R{product['price']} - "
        f"{product['aisle']}"
    )