from database import get_connection
from products import get_current_price


print("STORE PRICE TEST")
print("=" * 40)


connection = get_connection()
cursor = connection.cursor()


# Add a Store 2 price for Apple Purity 125ml.
cursor.execute(
    """
    INSERT INTO prices (
        product_id,
        store_id,
        regular_price,
        effective_from,
        effective_until
    )
    VALUES (?, ?, ?, ?, ?)
    """,
    (
        "1001",
        2,
        15.49,
        "2026-01-01",
        None
    )
)


connection.commit()
connection.close()


# Check Store 1 price.
print("\nStore 1:")
store_1_price = get_current_price(
    product_id="1001",
    store_id=1,
    check_date="2026-09-24"
)

print(store_1_price)


# Check Store 2 price.
print("\nStore 2:")
store_2_price = get_current_price(
    product_id="1001",
    store_id=2,
    check_date="2026-09-24"
)

print(store_2_price)