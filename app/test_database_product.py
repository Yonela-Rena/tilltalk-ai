from products import get_product


print("TEST: SQLite product lookup")

product = get_product("1002")

if product:
    print(f"Product: {product['product_name']}")
    print(f"Brand: {product['brand']}")
    print(f"Size: {product['size']}")
    print(f"Category: {product['category']}")
    print(f"Barcode: {product['barcode']}")
    print(f"Aisle: {product['aisle']}")
    print(f"Store: {product['store_name']}")
    print(f"Location: {product['location']}")
else:
    print("Product not found.")