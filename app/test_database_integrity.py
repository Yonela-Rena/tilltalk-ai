from database import get_connection


connection = get_connection()
cursor = connection.cursor()


print("DATABASE INTEGRITY TEST")
print("=" * 40)


# Check number of stores.
cursor.execute("""
    SELECT COUNT(*)
    FROM stores
""")

store_count = cursor.fetchone()[0]

print(f"\nStores: {store_count}")


# Check number of products.
cursor.execute("""
    SELECT COUNT(*)
    FROM products
""")

product_count = cursor.fetchone()[0]

print(f"Products: {product_count}")


# Check store-product relationships.
cursor.execute("""
    SELECT COUNT(*)
    FROM store_products
""")

relationship_count = cursor.fetchone()[0]

print(f"Store-product relationships: {relationship_count}")


# Check price records.
cursor.execute("""
    SELECT COUNT(*)
    FROM prices
""")

price_count = cursor.fetchone()[0]

print(f"Price records: {price_count}")


# Check promotions.
cursor.execute("""
    SELECT COUNT(*)
    FROM promotions
""")

promotion_count = cursor.fetchone()[0]

print(f"Promotion records: {promotion_count}")


# Find duplicate price records.
cursor.execute("""
    SELECT
        product_id,
        store_id,
        effective_from,
        COUNT(*)
    FROM prices
    GROUP BY
        product_id,
        store_id,
        effective_from
    HAVING COUNT(*) > 1
""")

duplicate_prices = cursor.fetchall()

print("\nDuplicate price records:")

if duplicate_prices:
    for row in duplicate_prices:
        print(row)
else:
    print("None")


# Find duplicate promotions.
cursor.execute("""
    SELECT
        product_id,
        store_id,
        start_date,
        end_date,
        COUNT(*)
    FROM promotions
    GROUP BY
        product_id,
        store_id,
        start_date,
        end_date
    HAVING COUNT(*) > 1
""")

duplicate_promotions = cursor.fetchall()

print("\nDuplicate promotion records:")

if duplicate_promotions:
    for row in duplicate_promotions:
        print(row)
else:
    print("None")


connection.close()