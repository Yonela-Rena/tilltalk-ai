from products import get_current_price


print("TEST 1: Active promotion")

result = get_current_price(
    product_id="1002",
    store_id=1,
    check_date="2026-09-20"
)

print(result)


print("\nTEST 2: Promotion expired")

result = get_current_price(
    product_id="1002",
    store_id=1,
    check_date="2026-10-05"
)

print(result)