import re
from datetime import date

from app.database import get_connection


def normalize_text(text):
    """
    Normalize text for safer product matching.

    Examples:
    '  Apple   Purity  ' -> 'apple purity'
    '200 ML' -> '200ml'
    '1 KG' -> '1kg'
    '400 G' -> '400g'
    'Apple-Purity' -> 'apple purity'
    """

    if not text:
        return ""

    text = text.lower().strip()

    # Replace punctuation with spaces.
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Normalize spaces between numbers and common units.
    # Longer units must come before shorter units.
    # Examples:
    # '200 ml' -> '200ml'
    # '1 kg' -> '1kg'
    # '400 g' -> '400g'
    text = re.sub(
        r"(\d+)\s+(ml|kg|g|l)\b",
        r"\1\2",
        text
    )

    # Collapse repeated spaces.
    text = re.sub(r"\s+", " ", text)

    return text


def get_current_price(product_id, store_id=1, check_date=None):
    """
    Return the current price for a product.

    An active promotion takes priority over the regular price.
    """

    if check_date is None:
        check_date = date.today().isoformat()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            promo_price,
            description
        FROM promotions
        WHERE product_id = ?
          AND store_id = ?
          AND start_date <= ?
          AND end_date >= ?
        ORDER BY promo_price ASC
        LIMIT 1
        """,
        (
            product_id,
            store_id,
            check_date,
            check_date
        )
    )

    promotion = cursor.fetchone()

    if promotion:
        connection.close()

        return {
            "price": promotion[0],
            "price_type": "promotion",
            "description": promotion[1]
        }

    cursor.execute(
        """
        SELECT
            regular_price
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
        (
            product_id,
            store_id,
            check_date,
            check_date
        )
    )

    regular_price = cursor.fetchone()

    connection.close()

    if regular_price:
        return {
            "price": regular_price[0],
            "price_type": "regular",
            "description": None
        }

    return None


def get_product(product_id, store_id=1):
    """
    Get product information for a specific store.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            p.product_id,
            p.product_name,
            p.brand,
            p.category,
            p.size,
            p.barcode,
            p.aisle,
            s.store_name,
            s.location
        FROM products p
        JOIN store_products sp
            ON sp.product_id = p.product_id
        JOIN stores s
            ON s.store_id = sp.store_id
        WHERE p.product_id = ?
          AND sp.store_id = ?
        """,
        (
            product_id,
            store_id
        )
    )

    product = cursor.fetchone()

    connection.close()

    if product:
        return {
            "product_id": product[0],
            "product_name": product[1],
            "brand": product[2],
            "category": product[3],
            "size": product[4],
            "barcode": product[5],
            "aisle": product[6],
            "store_name": product[7],
            "location": product[8]
        }

    return None


def search_products(search_term, store_id=1):
    """
    Search products using normalized text.

    Searches:
    - product name
    - brand
    - category
    - size
    """

    connection = get_connection()
    cursor = connection.cursor()

    search_pattern = f"%{search_term}%"

    cursor.execute(
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
          AND (
              p.product_name LIKE ?
              OR p.brand LIKE ?
              OR p.category LIKE ?
              OR p.size LIKE ?
          )
        ORDER BY
            p.product_name,
            p.size
        """,
        (
            store_id,
            search_pattern,
            search_pattern,
            search_pattern,
            search_pattern
        )
    )

    rows = cursor.fetchall()

    connection.close()

    products = []

    for row in rows:
        products.append(
            {
                "product_id": row[0],
                "product_name": row[1],
                "brand": row[2],
                "category": row[3],
                "size": row[4],
                "barcode": row[5],
                "aisle": row[6]
            }
        )

    return products


def find_products_by_name(product_name, store_id=1):
    """
    Find products using normalized product-name matching.
    """

    normalized_name = normalize_text(product_name)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
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
    )

    rows = cursor.fetchall()

    connection.close()

    products = []

    for row in rows:

        database_name = normalize_text(row[1])

        if database_name == normalized_name:

            products.append(
                {
                    "product_id": row[0],
                    "product_name": row[1],
                    "brand": row[2],
                    "category": row[3],
                    "size": row[4],
                    "barcode": row[5],
                    "aisle": row[6]
                }
            )

    return products


def find_product_by_name_and_size(
    product_name,
    size,
    store_id=1
):
    """
    Find exactly one product using normalized
    product name and size.
    """

    products = find_products_by_name(
        product_name,
        store_id=store_id
    )

    normalized_size = normalize_text(size)

    for product in products:

        if normalize_text(product["size"]) == normalized_size:

            return product

    return None


def lookup_product_price(
    product_name,
    size,
    store_id=1,
    check_date=None
):
    """
    Find a product at a specific store and return
    its verified current price.
    """

    product = find_product_by_name_and_size(
        product_name,
        size,
        store_id
    )

    if not product:
        return None

    price_info = get_current_price(
        product_id=product["product_id"],
        store_id=store_id,
        check_date=check_date
    )

    if not price_info:
        return None

    return {
        "product_id": product["product_id"],
        "product_name": product["product_name"],
        "brand": product["brand"],
        "size": product["size"],
        "category": product["category"],
        "aisle": product["aisle"],
        "price": price_info["price"],
        "price_type": price_info["price_type"],
        "promotion_description": price_info["description"]
    }