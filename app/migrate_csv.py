import csv

from database import get_connection


CSV_PATH = "data/products.csv"


def migrate_products():
    """Load products from CSV into the SQLite database."""

    connection = get_connection()
    cursor = connection.cursor()

    # Add our demo supermarket store.
    cursor.execute("""
        INSERT OR IGNORE INTO stores (
            store_id,
            store_name,
            location
        )
        VALUES (?, ?, ?)
    """, (
        1,
        "TillTalk Demo Store",
        "Richards Bay"
    ))

    # Read products from the CSV file.
    with open(CSV_PATH, "r", encoding="utf-8") as file:

        products = csv.DictReader(file)

        for product in products:

            # Add the product to the catalogue.
            cursor.execute("""
                INSERT OR IGNORE INTO products (
                    product_id,
                    product_name,
                    brand,
                    category,
                    size,
                    barcode,
                    aisle
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                product["product_id"],
                product["product_name"],
                product["brand"],
                product["category"],
                product["size"],
                product["barcode"],
                product["aisle"]
            ))

            # Make the product available at our demo store.
            cursor.execute("""
                INSERT OR IGNORE INTO store_products (
                    store_id,
                    product_id
                )
                VALUES (?, ?)
            """, (
                1,
                product["product_id"]
            ))

            # Add the current regular price.
            cursor.execute("""
                INSERT OR IGNORE INTO prices (
                    product_id,
                    store_id,
                    regular_price,
                    effective_from,
                    effective_until
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                product["product_id"],
                1,
                float(product["price"]),
                "2026-01-01",
                None
            ))

    connection.commit()
    connection.close()

    print("CSV data migrated to SQLite successfully.")


if __name__ == "__main__":
    migrate_products()