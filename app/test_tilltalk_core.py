from tilltalk import answer_price_query


print("TILLTALK CORE TEST")
print("=" * 40)


queries = [
    "How much is the 200ml Apple Purity?",
    "What's the price of the 2kg Maize Meal?",
    "How much is the 400g Peanut Butter?",
    "What does the 1L Full Cream Milk cost?"
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