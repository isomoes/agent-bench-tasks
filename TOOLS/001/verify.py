#!/usr/bin/env python3
"""Verification script for TOOLS-001: Find all Python files and report their sizes."""
import os
import re
import sys


def find_py_files(root: str) -> list:
    """Find all .py files under root, return sorted list of (rel_path, size)."""
    found = []
    for dirpath, _dirs, files in os.walk(root):
        for fname in files:
            if fname.endswith(".py"):
                full = os.path.join(dirpath, fname)
                rel = os.path.relpath(full, root)
                size = os.path.getsize(full)
                found.append((rel, size))
    return sorted(found, key=lambda x: x[0])


def verify() -> bool:
    output_file = "results/py_files.txt"

    if not os.path.exists(output_file):
        print(f"FAIL: '{output_file}' does not exist")
        return False

    content = open(output_file).read().strip()
    if not content:
        print(f"FAIL: '{output_file}' is empty")
        return False

    lines = [line.strip() for line in content.splitlines() if line.strip()]

    # Parse each line
    parsed = []
    for i, line in enumerate(lines, start=1):
        m = re.match(r'^(.+):\s*(\d+)\s+bytes$', line)
        if not m:
            print(f"FAIL: Line {i} does not match '<path>: <n> bytes' format: '{line}'")
            return False
        parsed.append((m.group(1).strip(), int(m.group(2))))

    # Compute expected from workspace.
    # Exclude task infrastructure dirs (CODING/, TOOLS/, WRITING/) and results/.
    workspace = os.getcwd()
    expected = find_py_files(workspace)

    EXCLUDE_PREFIXES = {"CODING", "TOOLS", "WRITING", "results"}
    expected = [
        (p, s) for p, s in expected
        if p.split(os.sep)[0] not in EXCLUDE_PREFIXES
    ]

    if len(parsed) != len(expected):
        print(f"FAIL: Expected {len(expected)} Python files, got {len(parsed)}")
        return False

    # Check paths and sizes
    for i, ((got_path, got_size), (exp_path, exp_size)) in enumerate(zip(parsed, expected), start=1):
        got_norm = got_path.replace("\\", "/")
        exp_norm = exp_path.replace("\\", "/")
        if got_norm != exp_norm:
            print(f"FAIL: Line {i} path: expected '{exp_norm}', got '{got_norm}'")
            return False
        if got_size != exp_size:
            print(f"FAIL: '{exp_path}' size: expected {exp_size} bytes, got {got_size}")
            return False

    print(f"PASS: Found and reported {len(expected)} Python files correctly")
    return True


if __name__ == "__main__":
    sys.exit(0 if verify() else 1)
