from app.products import get_current_price


print("PRICE LOOKUP TEST")
print("=" * 40)


# Test 1: Apple Purity 200ml during September promotion
print("\nTest 1: Apple Purity 200ml during promotion")

result = get_current_price(
    product_id="1002",
    store_id=1,
    check_date="2026-09-15"
)

print(result)


# Test 2: Apple Purity 200ml after promotion
print("\nTest 2: Apple Purity 200ml after promotion")

result = get_current_price(
    product_id="1002",
    store_id=1,
    check_date="2026-10-01"
)

print(result)


# Test 3: Apple Purity 125ml in Store 1
print("\nTest 3: Apple Purity 125ml in Store 1")

result = get_current_price(
    product_id="1001",
    store_id=1,
    check_date="2026-09-15"
)

print(result)


# Test 4: Apple Purity 125ml in Store 2
print("\nTest 4: Apple Purity 125ml in Store 2")

result = get_current_price(
    product_id="1001",
    store_id=2,
    check_date="2026-09-15"
)

print(result)