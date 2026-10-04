from tilltalk import answer_price_query


print("TILLTALK RESOLUTION TEST")
print("=" * 40)


queries = [
    "How much is the 200ml Apple Purity?",
    "How much is the Apple Purity?",
    "How much is the 300ml Apple Purity?",
    "How much is the Chocolate?"
]


for query in queries:

    print(f"\nCashier: {query}")

    result = answer_price_query(
        query,
        store_id=1,
        check_date="2026-09-20"
    )

    print("TillTalk:")
    print(result)