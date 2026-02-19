#!/usr/bin/env python3
"""Verification script for CODING-001: Fix a broken temperature converter.

Fixture: CODING/001/data/temperature.py
"""
import os
import sys


EXPECTED = [32.0, 212.0, -40.0, 98.6, 71.6]


def verify() -> bool:
    output_file = "results/temperatures.txt"

    if not os.path.exists(output_file):
        print(f"FAIL: '{output_file}' does not exist")
        return False

    content = open(output_file).read().strip()

    if not content:
        print(f"FAIL: '{output_file}' is empty")
        return False

    lines = [line.strip() for line in content.splitlines() if line.strip()]

    if len(lines) != len(EXPECTED):
        print(f"FAIL: Expected {len(EXPECTED)} lines, got {len(lines)}")
        return False

    for i, (line, exp) in enumerate(zip(lines, EXPECTED), start=1):
        try:
            val = round(float(line), 1)
        except ValueError:
            print(f"FAIL: Line {i} is not a number: '{line}'")
            return False
        if val != exp:
            print(f"FAIL: Line {i}: expected {exp}, got {val}")
            return False

    print("PASS: All 5 Celsius→Fahrenheit conversions are correct")
    return True


if __name__ == "__main__":
    sys.exit(0 if verify() else 1)
