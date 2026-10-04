from app.product_resolution import resolve_product
from app.products import get_current_price
from app.tilltalk import answer_parsed_query


def test_product_with_valid_size():
    result = resolve_product(
        product_name="Apple Purity",
        size="200ml",
        store_id=1
    )

    assert result["status"] == "success"
    assert result["product"]["product_id"] == "1002"
    assert result["product"]["size"] == "200ml"


def test_product_without_size_is_ambiguous():
    result = resolve_product(
        product_name="Apple Purity",
        store_id=1
    )

    assert result["status"] == "ambiguous"
    assert len(result["matches"]) == 3


def test_invalid_size():
    result = resolve_product(
        product_name="Apple Purity",
        size="300ml",
        store_id=1
    )

    assert result["status"] == "size_not_found"
    assert len(result["matches"]) == 3


def test_unknown_product():
    result = resolve_product(
        product_name="Chocolate",
        store_id=1
    )

    assert result["status"] == "not_found"


def test_active_promotion():
    result = get_current_price(
        product_id="1002",
        store_id=1,
        check_date="2026-09-15"
    )

    assert result["price"] == 13.99
    assert result["price_type"] == "promotion"


def test_expired_promotion():
    result = get_current_price(
        product_id="1002",
        store_id=1,
        check_date="2026-10-01"
    )

    assert result["price"] == 16.99
    assert result["price_type"] == "regular"


def test_store_specific_price():
    result = get_current_price(
        product_id="1001",
        store_id=2,
        check_date="2026-09-15"
    )

    assert result["price"] == 15.49
    assert result["price_type"] == "regular"


def test_complete_successful_query():
    result = answer_parsed_query(
        parsed_query={
            "product_name": "Apple Purity",
            "brand": "Purity",
            "size": "200ml"
        },
        store_id=1,
        check_date="2026-09-15"
    )

    assert result["status"] == "success"
    assert result["price"] == 13.99
    assert result["aisle"] == "Baby Aisle"


def test_missing_size_requests_clarification():
    result = answer_parsed_query(
        parsed_query={
            "product_name": "Apple Purity",
            "brand": "Purity",
            "size": None
        },
        store_id=1,
        check_date="2026-09-15"
    )

    assert result["status"] == "needs_clarification"
    assert result["available_sizes"] == [
        "125ml",
        "200ml",
        "400ml"
    ]