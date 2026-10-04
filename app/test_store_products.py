from database import get_connection


connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
    SELECT
        s.store_name,
        p.product_id,
        p.product_name,
        p.size
    FROM store_products sp
    JOIN stores s
        ON s.store_id = sp.store_id
    JOIN products p
        ON p.product_id = sp.product_id
    ORDER BY p.product_id
""")

rows = cursor.fetchall()

connection.close()


print("STORE PRODUCT TEST")
print("=" * 40)

print(f"Store-product relationships: {len(rows)}")

for row in rows[:5]:
    print(row)