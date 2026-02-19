#!/usr/bin/env python3
"""Verification script for WRITING-001: haiku about technology."""
import os
import re
import sys


VOWEL_GROUPS_RE = re.compile(r"[aeiouy]+", re.IGNORECASE)


def count_syllables_in_word(word: str) -> int:
    """Estimate syllable count for an English word using simple heuristics."""
    cleaned = re.sub(r"[^a-z]", "", word.lower())
    if not cleaned:
        return 0
    groups = len(VOWEL_GROUPS_RE.findall(cleaned))
    syllables = groups
    if cleaned.endswith("e") and not cleaned.endswith(("le", "ye")) and syllables > 1:
        syllables -= 1
    return max(1, syllables)


def count_line_syllables(line: str) -> int:
    words = [w for w in re.split(r"\s+", line.strip()) if w]
    return sum(count_syllables_in_word(word) for word in words)


def verify() -> bool:
    output_file = "results/haiku.txt"

    if not os.path.exists(output_file):
        print(f"FAIL: '{output_file}' does not exist")
        return False

    content = open(output_file).read().strip()
    if not content:
        print(f"FAIL: '{output_file}' is empty")
        return False

    lines = [line.strip() for line in content.splitlines() if line.strip()]

    if len(lines) != 3:
        print(f"FAIL: A haiku must have exactly 3 lines, got {len(lines)}")
        return False

    expected_pattern = [5, 7, 5]
    for i, (line, expected) in enumerate(zip(lines, expected_pattern), start=1):
        syllables = count_line_syllables(line)
        if syllables != expected:
            print(f"FAIL: Line {i} must have {expected} syllables, found {syllables}: '{line}'")
            return False

    tech_keywords = [
        "code", "data", "digital", "software", "hardware", "computer",
        "internet", "network", "algorithm", "ai", "robot", "machine",
        "silicon", "circuit", "byte", "pixel", "screen", "server",
        "cloud", "tech", "program", "electric", "signal", "binary",
    ]
    if not any(kw in content.lower() for kw in tech_keywords):
        print("FAIL: Haiku does not appear to be about technology")
        return False

    print("PASS: Haiku uses 5-7-5 syllable pattern and technology theme")
    return True


if __name__ == "__main__":
    sys.exit(0 if verify() else 1)
