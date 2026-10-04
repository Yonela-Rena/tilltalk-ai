from database import get_connection


def add_test_promotion():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO promotions (
            product_id,
            store_id,
            promo_price,
            start_date,
            end_date,
            description
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        "1002",
        1,
        13.99,
        "2026-09-15",
        "2026-09-30",
        "September Baby Food Special"
    ))

    connection.commit()
    connection.close()

    print("Test promotion added successfully.")


if __name__ == "__main__":
    add_test_promotion()