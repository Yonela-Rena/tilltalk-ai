from products import lookup_product_price

print("TEST: Product price lookup")

result = lookup_product_price(
    product_name="Apple Purity",
    size="200ml",
    store_id=1,
    check_date="2026-09-20"
)

if result:
    print("\nProduct found:")
    print(f"Product: {result['product_name']}")
    print(f"Brand: {result['brand']}")
    print(f"Size: {result['size']}")
    print(f"Product ID: {result['product_id']}")
    print(f"Aisle: {result['aisle']}")
    print(f"Price: R{result['price']:.2f}")
    print(f"Price type: {result['price_type']}")

    if result["promotion_description"]:
        print(f"Promotion: {result['promotion_description']}")
else:
    print("\nProduct or price not found.")