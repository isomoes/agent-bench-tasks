#!/usr/bin/env python3
"""Verification script for TOOLS-002: Fetch a webpage and extract the page title."""
import os
import sys


# The known title of https://example.com — stable since the page is maintained by IANA
EXPECTED_TITLE = "Example Domain"


def verify() -> bool:
    output_file = "results/page_title.txt"

    if not os.path.exists(output_file):
        print(f"FAIL: '{output_file}' does not exist")
        return False

    content = open(output_file).read().strip()

    if not content:
        print(f"FAIL: '{output_file}' is empty")
        return False

    lines = [line.strip() for line in content.splitlines() if line.strip()]

    if len(lines) != 1:
        print(f"FAIL: Expected exactly 1 line, got {len(lines)}")
        return False

    title = lines[0]

    if title.lower() != EXPECTED_TITLE.lower():
        print(f"FAIL: Expected title '{EXPECTED_TITLE}', got '{title}'")
        return False

    print(f"PASS: Page title correctly extracted: '{title}'")
    return True


if __name__ == "__main__":
    sys.exit(0 if verify() else 1)
