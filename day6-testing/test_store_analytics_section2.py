"""
test_store_analytics.py

Starter file for the "write your own tests" exercise.

pytest and the module under test are already imported below, and there's
one fully-worked example test to show you the pattern. Everything after
that is up to you: add your own test functions (name them test_something)
that check store_analytics.py against its docstrings.

Run your tests from this folder with:
    pytest -v
"""

import pytest
from store_analytics import (
    parse_order_row,
    compute_line_total,
    summarize_by_product,
    top_n_products,
    apply_bulk_discount,
    loyalty_tier,
    load_orders_from_csv,
    write_top_products_report,
)


# --- Example test (already written for you) -------------------------------

def test_parse_order_row_valid_row():
    row = ["1001", "Widget", "4", "9.99", "alice@example.com"]
    order = parse_order_row(row)
    assert order == {
        "order_id": "1001",
        "product": "widget",
        "quantity": 4,
        "unit_price": 9.99,
        "customer_email": "alice@example.com",
    }


def test_parse_order_row_missing_order_id():
    row = ["", "Widget", "4", "9.99", "alice@example.com"]
    with pytest.raises(ValueError):
        parse_order_row(row)

def test_parse_order_row_wrong_number_of_fields():
    row = ["Widget", "4", "9.99", "alice@example.com"]
    with pytest.raises(ValueError):
        parse_order_row(row)

def test_compute_line_total():
    order = {
        "order_id": "1001",
        "product": "widget",
        "quantity": 3,
        "unit_price": 9.99,
        "customer_email": "alice@example.com",
    }
    assert compute_line_total(order) == 29.97


def test_loyalty_tier_platinum():
    total_spent = 10001
    assert loyalty_tier(total_spent) == "platinum"

def test_loyalty_tier_silver():
    total_spent = 150
    assert loyalty_tier(total_spent) == "silver"