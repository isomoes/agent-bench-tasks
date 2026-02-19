#!/usr/bin/env python3
"""Verification script for TOOLS-003: Read config, run command, write combined report.

Fixture: TOOLS/003/data/settings.json
         TOOLS/003/data/input/
"""
import json
import os
import re
import sys


def count_nonempty_lines(filepath: str) -> int:
    with open(filepath) as f:
        return sum(1 for line in f if line.strip())


def verify() -> bool:
    config_file = "TOOLS/003/data/settings.json"
    output_file = "results/report.txt"

    if not os.path.exists(config_file):
        print(f"FAIL: Config file '{config_file}' does not exist in workspace")
        return False

    try:
        config = json.loads(open(config_file).read())
    except json.JSONDecodeError as e:
        print(f"FAIL: '{config_file}' is not valid JSON: {e}")
        return False

    target_dir = config.get("target_dir", "").strip()
    if not target_dir:
        print(f"FAIL: 'target_dir' key missing or empty in '{config_file}'")
        return False

    if not os.path.isdir(target_dir):
        print(f"FAIL: target_dir '{target_dir}' does not exist in workspace")
        return False

    # Compute expected values
    files_in_dir = sorted(
        f for f in os.listdir(target_dir)
        if os.path.isfile(os.path.join(target_dir, f))
    )
    expected_counts = {
        fname: count_nonempty_lines(os.path.join(target_dir, fname))
        for fname in files_in_dir
    }

    if not os.path.exists(output_file):
        print(f"FAIL: '{output_file}' does not exist")
        return False

    content = open(output_file).read()
    non_blank = [l for l in content.splitlines() if l.strip()]

    if not non_blank:
        print(f"FAIL: '{output_file}' is empty")
        return False

    # First line: target_dir
    m = re.match(r'^target_dir:\s*(.+)$', non_blank[0].strip())
    if not m:
        print(f"FAIL: First line must be 'target_dir: <value>', got: '{non_blank[0]}'")
        return False
    reported_dir = m.group(1).strip()
    if reported_dir != target_dir:
        print(f"FAIL: target_dir: expected '{target_dir}', got '{reported_dir}'")
        return False

    # Second line: "files:"
    if len(non_blank) < 2 or non_blank[1].strip() != "files:":
        got = non_blank[1] if len(non_blank) > 1 else ""
        print(f"FAIL: Second non-blank line must be 'files:', got: '{got}'")
        return False

    file_lines = non_blank[2:]

    if len(file_lines) != len(expected_counts):
        print(f"FAIL: Expected {len(expected_counts)} file entries, got {len(file_lines)}")
        return False

    parsed_files = {}
    for i, line in enumerate(file_lines, start=1):
        m2 = re.match(r'^\s*(.+):\s*(\d+)\s+lines$', line)
        if not m2:
            print(f"FAIL: File entry {i} does not match '<name>: <n> lines': '{line}'")
            return False
        parsed_files[m2.group(1).strip()] = int(m2.group(2))

    reported_names = list(parsed_files.keys())
    if reported_names != sorted(reported_names):
        print(f"FAIL: Files are not listed in alphabetical order: {reported_names}")
        return False

    for fname, exp_count in expected_counts.items():
        if fname not in parsed_files:
            print(f"FAIL: File '{fname}' is missing from the report")
            return False
        if parsed_files[fname] != exp_count:
            print(f"FAIL: '{fname}' line count: expected {exp_count}, got {parsed_files[fname]}")
            return False

    print(f"PASS: Report correct — target_dir='{target_dir}', {len(expected_counts)} files reported")
    return True


if __name__ == "__main__":
    sys.exit(0 if verify() else 1)
