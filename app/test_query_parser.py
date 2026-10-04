from query_parser import parse_query


print("TEST: Query parser")

query = "How much is the 200ml Apple Purity?"

print("\nCashier query:")
print(query)

result = parse_query(query)

print("\nParsed query:")
print(result)