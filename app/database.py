import sqlite3


DATABASE_PATH = "data/tilltalk.db"


def get_connection():
    """Create a connection to the TillTalk SQLite database."""

    connection = sqlite3.connect(DATABASE_PATH)

    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def create_tables():
    """Create the TillTalk SQLite database tables."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stores (
            store_id INTEGER PRIMARY KEY,
            store_name TEXT NOT NULL,
            location TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id TEXT PRIMARY KEY,
            product_name TEXT NOT NULL,
            brand TEXT NOT NULL,
            category TEXT NOT NULL,
            size TEXT NOT NULL,
            barcode TEXT UNIQUE NOT NULL,
            aisle TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS store_products (
            store_id INTEGER NOT NULL,
            product_id TEXT NOT NULL,

            PRIMARY KEY (store_id, product_id),

            FOREIGN KEY (store_id)
                REFERENCES stores(store_id),

            FOREIGN KEY (product_id)
                REFERENCES products(product_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            price_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT NOT NULL,
            store_id INTEGER NOT NULL,
            regular_price REAL NOT NULL,
            effective_from TEXT NOT NULL,
            effective_until TEXT,

            UNIQUE (
                product_id,
                store_id,
                effective_from
            ),

            FOREIGN KEY (product_id)
                REFERENCES products(product_id),

            FOREIGN KEY (store_id)
                REFERENCES stores(store_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS promotions (
            promotion_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT NOT NULL,
            store_id INTEGER NOT NULL,
            promo_price REAL NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            description TEXT,

            UNIQUE (
                product_id,
                store_id,
                start_date,
                end_date
            ),

            FOREIGN KEY (product_id)
                REFERENCES products(product_id),

            FOREIGN KEY (store_id)
                REFERENCES stores(store_id)
        )
    """)

    connection.commit()
    connection.close()

    print("Database tables created successfully.")


if __name__ == "__main__":
    create_tables()