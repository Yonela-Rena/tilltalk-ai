from app.product_resolution import resolve_product


print("PRODUCT RESOLUTION TEST")
print("=" * 40)


tests = [
    ("Apple Purity", None),
    ("Apple Purity", "200ml"),
    ("Apple Purity", "200 ml"),
    ("Apple Purity", "200ML"),
    ("Apple Purity", "300ml"),
    ("Chocolate", None),
]


for product_name, size in tests:

    print(f"\nProduct: {product_name}")
    print(f"Size: {size}")

    result = resolve_product(
        product_name=product_name,
        size=size
    )

    print("Result:")
    print(result)