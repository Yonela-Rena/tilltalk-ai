import csv

with open("data/products.csv", "r", encoding="utf-8") as file:
    products = list(csv.DictReader(file))

print(f"Loaded {len(products)} products.")

for product in products[:3]:
    print(product)