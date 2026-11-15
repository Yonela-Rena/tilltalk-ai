
import re
import sqlite3
from datetime import date

from app.database import get_connection


def normalize_text(text):
    """
    Normalize text to make product matching more reliable.

    Examples:
    'Apple-Purity' -> 'apple purity'
    '200 ML' -> '200ml'
    '1 KG' -> '1kg'
    """

    if not text:
        return ""

    text = text.lower().strip()

    # Replace punctuation with spaces.
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Normalize spaces between numbers and units.
    text = re.sub(
        r"(\d+)\s+(ml|kg|g|l)\b",
        r"\1\2",
        text
    )

    # Remove extra spaces.
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def find_products_by_name(product_name, store_id=1):
    """
    Find products by matching the requested name.

    Supports exact names and flexible keyword matching.
    Only returns products available at the requested store.
    """

    normalized_query = normalize_text(product_name)

    if not normalized_query:
        return []

    connection = get_connection()
    connection.row_factory = sqlite3.Row

    try:
        rows = connection.execute(
            """
            SELECT
                p.product_id,
                p.product_name,
                p.brand,
                p.category,
                p.size,
                p.barcode,
                p.aisle
            FROM products p
            JOIN store_products sp
                ON sp.product_id = p.product_id
            WHERE sp.store_id = ?
            ORDER BY p.product_name, p.size
            """,
            (store_id,)
        ).fetchall()

        products = []

        query_words = normalized_query.split()

        for row in rows:
            product = dict(row)

            searchable_text = normalize_text(
                " ".join([
                    product["product_name"] or "",
                    product["brand"] or "",
                    product["category"] or ""
                ])
            )

            # Exact product-name match.
            exact_match = (
                normalize_text(product["product_name"])
                == normalized_query
            )

            # Flexible keyword match.
            keyword_match = all(
                word in searchable_text
                for word in query_words
            )

            if exact_match or keyword_match:
                products.append(product)

        return products

    finally:
        connection.close()


def get_current_price(product_id, store_id=1, check_date=None):
    """
    Return the active promotional price if one exists.
    Otherwise, return the regular price effective on the date.

    Uses the actual column names in the TillTalk database.
    """

    if check_date is None:
        check_date = date.today().isoformat()

    connection = get_connection()
    connection.row_factory = sqlite3.Row

    try:
        # Confirm that the product belongs to this store.
        available = connection.execute(
            """
            SELECT 1
            FROM store_products
            WHERE product_id = ?
              AND store_id = ?
            """,
            (str(product_id), store_id)
        ).fetchone()

        if not available:
            return None

        # Check for an active promotion first.
        promotion = connection.execute(
            """
            SELECT promo_price, description
            FROM promotions
            WHERE product_id = ?
              AND store_id = ?
              AND start_date <= ?
              AND end_date >= ?
            ORDER BY start_date DESC
            LIMIT 1
            """,
            (str(product_id), store_id, check_date, check_date)
        ).fetchone()

        if promotion:
            return {
                "price": float(promotion["promo_price"]),
                "price_type": "promotion",
                "description": promotion["description"]
            }

        # Check the regular price.
        regular_price = connection.execute(
            """
            SELECT regular_price
            FROM prices
            WHERE product_id = ?
              AND store_id = ?
              AND effective_from <= ?
              AND (
                  effective_until IS NULL
                  OR effective_until >= ?
              )
            ORDER BY effective_from DESC
            LIMIT 1
            """,
            (str(product_id), store_id, check_date, check_date)
        ).fetchone()

        if not regular_price:
            return None

        return {
            "price": float(regular_price["regular_price"]),
            "price_type": "regular",
            "description": None
        }

    finally:
        connection.close()

