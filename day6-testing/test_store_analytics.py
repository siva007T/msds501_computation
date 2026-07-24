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


# --- Your tests go below here ----------------------------------------------
def test_parse_order_row_invalid():
    bad_row_missing_field = ["101", "Coffee Mug", "2", "12.50"]
    with pytest.raises(ValueError, match="expected 5 fields"):
        parse_order_row(bad_row_missing_field)
    bad_row_zero_qty = ["101", "Mug", "0", "9.99", "sivag@.com"]
    with pytest.raises(ValueError, match="quantity must be positive"):
        parse_order_row(bad_row_zero_qty)


def test_compute_line_total():
    order = {"quantity": 3, "unit_price": 10.333}
    total = compute_line_total(order)
    assert total == 31.00


def test_summarize_by_product():
    orders = [
        {"product": "cattoy", "quantity": 2, "unit_price": 10.00},
        {"product": "cattoy", "quantity": 1, "unit_price": 10.00},
        {"product": "dogtoy", "quantity": 5, "unit_price": 4.00},
    ]

    # When: We summarize the orders
    summary = summarize_by_product(orders)

    # Then: Mugs combine (3 total units, $30 revenue) and notebooks stand alone
    assert summary == {
        "cattoy": {"total_quantity": 3, "total_revenue": 30.00, "order_count": 2},
        "dogtoy": {"total_quantity": 5, "total_revenue": 20.00, "order_count": 1},
    }


def test_top_n_products_ranking_and_tiebreak():
    summary = {
        "apple": {"total_revenue": 50.0},
        "android": {"total_revenue": 100.0},
        "google": {"total_revenue": 50.0},
    }
    top_2 = top_n_products(summary, n=2)
    assert top_2 == [
        ("android", {"total_revenue": 100.0}),
        ("apple", {"total_revenue": 50.0}),
    ]


def test_apply_bulk_discount_immutability():
    # Given: An order with qty 10 (qualifies) and an order with qty 2 (does not)
    original_orders = [
        {"product": "mug", "quantity": 10, "unit_price": 10.00},
        {"product": "pen", "quantity": 2, "unit_price": 2.00},
    ]
    discounted = apply_bulk_discount(original_orders, min_quantity=5, discount_rate=0.10)
    assert discounted[0]["unit_price"] == 9.00
    assert discounted[1]["unit_price"] == 2


@pytest.mark.parametrize(
    "spend, expected_tier",
    [
        (0, "none"),
        (100, "silver"),
        (999.9999999, "gold"),
        (1000, "platinum"),
    ],
)
def test_loyalty_tier_boundaries(spend, expected_tier):
    assert loyalty_tier(spend) == expected_tier


def test_load_orders_from_csv(tmp_path):
    # Given: A mock CSV file with 1 header, 1 good row, and 1 bad row (negative qty)
    csv_file = tmp_path / "orders.csv"
    csv_file.write_text(
        "order_id,product,quantity,unit_price,customer_email\n"
        "420,cattoy,2,11.00,siva@acingtests.com\n"
        "67,dogttoy,-1,7.00,good@bad.com\n"
    )
    orders, errors = load_orders_from_csv(csv_file)
    assert len(orders) == 1
    assert orders[0]["order_id"] == "101"

    assert len(errors) == 1
    assert "row 3: quantity must be positive" in errors[0]


def test_write_top_products_report(tmp_path):
    # Given: A summary dict and a target file path
    summary = {
        "coffee mug": {"total_quantity": 5, "total_revenue": 50.0},
        "notebook": {"total_quantity": 2, "total_revenue": 20.0},
    }
    report_file = tmp_path / "report.txt"

    # When: We write the top 1 product to the report
    write_top_products_report(summary, report_file, n=1)

    # Then: The file is created on disk with exact expected string formatting
    content = report_file.read_text()
    assert content == "coffee mug: $50.0 (5 units)\n"