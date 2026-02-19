#!/usr/bin/env python3
"""Verification script for CODING-003: Aggregate a CSV file and output JSON.

Fixture: data/sales.csv
"""
import csv
import json
import os
import sys


def compute_expected(csv_file: str) -> dict:
    """Compute expected aggregation from the source CSV."""
    summary = {}
    with open(csv_file, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            product = row["product"].strip()
            quantity = int(row["quantity"].strip())
            price = float(row["price"].strip())
            if product not in summary:
                summary[product] = {"total_quantity": 0, "total_revenue": 0.0}
            summary[product]["total_quantity"] += quantity
            summary[product]["total_revenue"] += quantity * price

    for product in summary:
        summary[product]["total_revenue"] = round(summary[product]["total_revenue"], 2)

    return summary


def verify() -> bool:
    output_file = "results/sales_summary.json"
    source_csv = "data/sales.csv"

    if not os.path.exists(source_csv):
        print(f"FAIL: Source CSV '{source_csv}' does not exist")
        return False

    if not os.path.exists(output_file):
        print(f"FAIL: '{output_file}' does not exist")
        return False

    content = open(output_file).read().strip()
    if not content:
        print(f"FAIL: '{output_file}' is empty")
        return False

    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"FAIL: '{output_file}' is not valid JSON: {e}")
        return False

    if not isinstance(data, dict):
        print(f"FAIL: JSON root must be an object, got {type(data).__name__}")
        return False

    expected = compute_expected(source_csv)

    if set(data.keys()) != set(expected.keys()):
        missing = set(expected.keys()) - set(data.keys())
        extra = set(data.keys()) - set(expected.keys())
        print(f"FAIL: Product keys mismatch — missing: {missing}, extra: {extra}")
        return False

    actual_keys = list(data.keys())
    if actual_keys != sorted(actual_keys):
        print(f"FAIL: Keys are not sorted alphabetically: {actual_keys}")
        return False

    for product, exp_vals in expected.items():
        got = data[product]
        if not isinstance(got, dict):
            print(f"FAIL: Value for '{product}' must be an object, got {type(got).__name__}")
            return False
        if got.get("total_quantity") != exp_vals["total_quantity"]:
            print(f"FAIL: '{product}' total_quantity: expected {exp_vals['total_quantity']}, got {got.get('total_quantity')}")
            return False
        got_rev = round(float(got.get("total_revenue", 0)), 2)
        if got_rev != exp_vals["total_revenue"]:
            print(f"FAIL: '{product}' total_revenue: expected {exp_vals['total_revenue']}, got {got_rev}")
            return False

    print(f"PASS: sales_summary.json is correct for {len(expected)} products")
    return True


if __name__ == "__main__":
    sys.exit(0 if verify() else 1)
