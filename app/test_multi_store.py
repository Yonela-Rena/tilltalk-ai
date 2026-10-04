from database import get_connection
from product_resolution import resolve_product


print("MULTI-STORE TEST")
print("=" * 40)


def create_second_store():
    """Create a second demo store for testing."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO stores (
            store_id,
            store_name,
            location
        )
        VALUES (?, ?, ?)
        """,
        (
            2,
            "TillTalk Second Store",
            "Empangeni"
        )
    )

    # Add only one product to Store 2.
    cursor.execute(
        """
        INSERT OR IGNORE INTO store_products (
            store_id,
            product_id
        )
        VALUES (?, ?)
        """,
        (
            2,
            "1001"
        )
    )

    connection.commit()
    connection.close()


create_second_store()


# Test Store 1.
print("\nStore 1:")
result = resolve_product(
    product_name="Apple Purity",
    size="200ml",
    store_id=1
)

print(result)


# Test Store 2.
print("\nStore 2:")
result = resolve_product(
    product_name="Apple Purity",
    size="200ml",
    store_id=2
)

print(result)


# Test a product that exists in Store 2.
print("\nStore 2 - 125ml Apple Purity:")
result = resolve_product(
    product_name="Apple Purity",
    size="125ml",
    store_id=2
)

print(result)