import csv

from app.database import get_connection


CSV_PATH = "data/products.csv"


def seed_database():
    """Create predictable demo data for TillTalk."""

    connection = get_connection()
    cursor = connection.cursor()

    # ---------------------------------------------------------
    # 1. Create demo stores
    # ---------------------------------------------------------

    stores = [
        (
            1,
            "TillTalk Demo Store",
            "Richards Bay"
        ),
        (
            2,
            "TillTalk Second Store",
            "Empangeni"
        )
    ]

    cursor.executemany(
        """
        INSERT OR IGNORE INTO stores (
            store_id,
            store_name,
            location
        )
        VALUES (?, ?, ?)
        """,
        stores
    )

    # ---------------------------------------------------------
    # 2. Load products from CSV
    # ---------------------------------------------------------

    with open(
        CSV_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        products = csv.DictReader(file)

        for product in products:

            cursor.execute(
                """
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
                """,
                (
                    product["product_id"],
                    product["product_name"],
                    product["brand"],
                    product["category"],
                    product["size"],
                    product["barcode"],
                    product["aisle"]
                )
            )

            # -------------------------------------------------
            # Store 1 has all catalogue products.
            # -------------------------------------------------

            cursor.execute(
                """
                INSERT OR IGNORE INTO store_products (
                    store_id,
                    product_id
                )
                VALUES (?, ?)
                """,
                (
                    1,
                    product["product_id"]
                )
            )

            # -------------------------------------------------
            # Store 1 regular price.
            # -------------------------------------------------

            cursor.execute(
                """
                INSERT OR IGNORE INTO prices (
                    product_id,
                    store_id,
                    regular_price,
                    effective_from,
                    effective_until
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    product["product_id"],
                    1,
                    float(product["price"]),
                    "2026-01-01",
                    None
                )
            )

    # ---------------------------------------------------------
    # 3. Store 2 deliberately carries only one product.
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # 4. Store 2 has its own price.
    # ---------------------------------------------------------

    cursor.execute(
        """
        INSERT OR IGNORE INTO prices (
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

    # ---------------------------------------------------------
    # 5. Add demo promotion.
    # ---------------------------------------------------------

    cursor.execute(
        """
        INSERT OR IGNORE INTO promotions (
            product_id,
            store_id,
            promo_price,
            start_date,
            end_date,
            description
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            "1002",
            1,
            13.99,
            "2026-09-01",
            "2026-09-30",
            "September Baby Food Special"
        )
    )

    connection.commit()
    connection.close()

    print("TillTalk demo database seeded successfully.")


if __name__ == "__main__":
    seed_database()
    