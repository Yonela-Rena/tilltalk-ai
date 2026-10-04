from database import get_connection


def check_database():
    connection = get_connection()
    cursor = connection.cursor()

    # Count stores
    cursor.execute("SELECT COUNT(*) FROM stores")
    store_count = cursor.fetchone()[0]

    # Count products
    cursor.execute("SELECT COUNT(*) FROM products")
    product_count = cursor.fetchone()[0]

    # Count prices
    cursor.execute("SELECT COUNT(*) FROM prices")
    price_count = cursor.fetchone()[0]

    print(f"Stores: {store_count}")
    print(f"Products: {product_count}")
    print(f"Prices: {price_count}")

    print("\nFirst 3 products:")

    cursor.execute("""
        SELECT
            product_id,
            product_name,
            size,
            barcode,
            aisle
        FROM products
        LIMIT 3
    """)

    for product in cursor.fetchall():
        print(product)

    print("\nFirst 3 prices:")

    cursor.execute("""
        SELECT
            product_id,
            store_id,
            regular_price,
            effective_from
        FROM prices
        LIMIT 3
    """)

    for price in cursor.fetchall():
        print(price)

    connection.close()


if __name__ == "__main__":
    check_database()