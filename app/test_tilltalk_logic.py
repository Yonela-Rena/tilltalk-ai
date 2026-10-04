from app.tilltalk import answer_parsed_query


print("TILLTALK BUSINESS LOGIC TEST")
print("=" * 50)


# Test 1: Valid product and size
print("\nTest 1: Valid product and size")

result = answer_parsed_query(
    parsed_query={
        "product_name": "Apple Purity",
        "brand": "Purity",
        "size": "200ml"
    },
    store_id=1,
    check_date="2026-09-15"
)

print(result)


# Test 2: Missing size
print("\nTest 2: Missing size")

result = answer_parsed_query(
    parsed_query={
        "product_name": "Apple Purity",
        "brand": "Purity",
        "size": None
    },
    store_id=1,
    check_date="2026-09-15"
)

print(result)


# Test 3: Invalid size
print("\nTest 3: Invalid size")

result = answer_parsed_query(
    parsed_query={
        "product_name": "Apple Purity",
        "brand": "Purity",
        "size": "300ml"
    },
    store_id=1,
    check_date="2026-09-15"
)

print(result)


# Test 4: Product does not exist
print("\nTest 4: Product does not exist")

result = answer_parsed_query(
    parsed_query={
        "product_name": "Chocolate",
        "brand": None,
        "size": None
    },
    store_id=1,
    check_date="2026-09-15"
)

print(result)


# Test 5: Different store
print("\nTest 5: Store-specific price")

result = answer_parsed_query(
    parsed_query={
        "product_name": "Apple Purity",
        "brand": "Purity",
        "size": "125ml"
    },
    store_id=2,
    check_date="2026-09-15"
)

print(result)