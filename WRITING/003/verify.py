#!/usr/bin/env python3
"""Verification script for WRITING-003: pros/cons list about remote work."""
import os
import re
import sys


def verify() -> bool:
    output_file = "results/pros_cons.txt"

    if not os.path.exists(output_file):
        print(f"FAIL: '{output_file}' does not exist")
        return False

    content = open(output_file).read().strip()
    if not content:
        print(f"FAIL: '{output_file}' is empty")
        return False

    pros_match = re.search(r'Pros\s*:\s*\n((?:\s*-[^\n]+\n?){1,})', content, re.IGNORECASE)
    cons_match = re.search(r'Cons\s*:\s*\n((?:\s*-[^\n]+\n?){1,})', content, re.IGNORECASE)

    if not pros_match:
        print("FAIL: Could not find a 'Pros:' section with bullet points")
        return False

    if not cons_match:
        print("FAIL: Could not find a 'Cons:' section with bullet points")
        return False

    def extract_bullets(section_text):
        return [line.strip().lstrip("-").strip()
                for line in section_text.splitlines()
                if line.strip().startswith("-")]

    pros = extract_bullets(pros_match.group(1))
    cons = extract_bullets(cons_match.group(1))

    if len(pros) != 5:
        print(f"FAIL: Expected 5 pros, found {len(pros)}")
        return False

    if len(cons) != 5:
        print(f"FAIL: Expected 5 cons, found {len(cons)}")
        return False

    for i, point in enumerate(pros + cons, start=1):
        word_count = len(point.split())
        if word_count < 10 or word_count > 30:
            print(f"FAIL: Point {i} must be 10-30 words, found {word_count}: '{point}'")
            return False

    print("PASS: Pros/cons list has 5 pros and 5 cons about remote work")
    return True


if __name__ == "__main__":
    sys.exit(0 if verify() else 1)
