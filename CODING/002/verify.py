#!/usr/bin/env python3
"""Verification script for CODING-002: Parse a log file and extract error counts.

Fixture: data/server.log
"""
import os
import re
import sys


def count_log_levels(log_file: str) -> dict:
    """Count log levels in the source log file to derive expected values."""
    counts = {"INFO": 0, "WARN": 0, "ERROR": 0}
    with open(log_file) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            m = re.match(r'^\[(INFO|WARN|ERROR)\]', line)
            if m:
                counts[m.group(1)] += 1
    return counts


def verify() -> bool:
    output_file = "results/log_summary.txt"
    source_log = "data/server.log"

    if not os.path.exists(source_log):
        print(f"FAIL: Source log '{source_log}' does not exist")
        return False

    if not os.path.exists(output_file):
        print(f"FAIL: '{output_file}' does not exist")
        return False

    content = open(output_file).read().strip()
    if not content:
        print(f"FAIL: '{output_file}' is empty")
        return False

    lines = [line.strip() for line in content.splitlines() if line.strip()]

    if len(lines) != 3:
        print(f"FAIL: Expected exactly 3 lines (INFO/WARN/ERROR), got {len(lines)}")
        return False

    parsed = {}
    for line in lines:
        m = re.match(r'^(INFO|WARN|ERROR):\s*(\d+)$', line)
        if not m:
            print(f"FAIL: Line does not match 'LEVEL: count' format: '{line}'")
            return False
        parsed[m.group(1)] = int(m.group(2))

    order = [re.match(r'^(INFO|WARN|ERROR)', l).group(1) for l in lines]  # type: ignore[union-attr]
    if order != ["INFO", "WARN", "ERROR"]:
        print(f"FAIL: Lines must be in order INFO, WARN, ERROR — got {order}")
        return False

    expected = count_log_levels(source_log)
    for level in ("INFO", "WARN", "ERROR"):
        if parsed.get(level) != expected[level]:
            print(f"FAIL: {level} count: expected {expected[level]}, got {parsed.get(level)}")
            return False

    total = sum(expected.values())
    print(f"PASS: Log summary correct — INFO:{expected['INFO']} WARN:{expected['WARN']} ERROR:{expected['ERROR']} (total {total} lines)")
    return True


if __name__ == "__main__":
    sys.exit(0 if verify() else 1)
