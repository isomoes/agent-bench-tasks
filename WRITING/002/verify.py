#!/usr/bin/env python3
"""Verification script for WRITING-002: one-sentence paragraph summary."""
import os
import sys


def verify() -> bool:
    output_file = "results/summary.txt"

    if not os.path.exists(output_file):
        print(f"FAIL: '{output_file}' does not exist")
        return False

    content = open(output_file).read().strip()
    if not content:
        print(f"FAIL: '{output_file}' is empty")
        return False

    sentences = [s.strip() for s in content.split(".") if s.strip()]
    if len(sentences) > 1:
        print(f"FAIL: Expected a single sentence, found {len(sentences)} sentences")
        return False

    word_count = len(content.split())
    if word_count >= 50:
        print(f"FAIL: Summary is too long ({word_count} words); it must be under 50 words")
        return False

    if word_count < 8:
        print(f"FAIL: Summary is too short ({word_count} words)")
        return False

    if not content.endswith("."):
        print("FAIL: Summary must end with a period")
        return False

    benefit_keywords = ["benefit", "transform", "assist", "improve", "advance",
                        "promise", "opportunit", "revolutioniz", "enhance", "help"]
    challenge_keywords = ["challenge", "concern", "ethical", "bias", "privacy",
                          "risk", "question", "problem", "issue", "employment"]

    text_lower = content.lower()
    if not any(kw in text_lower for kw in benefit_keywords):
        print("FAIL: Summary does not mention benefits/advances of AI")
        return False

    if not any(kw in text_lower for kw in challenge_keywords):
        print("FAIL: Summary does not mention challenges/concerns of AI")
        return False

    print(f"PASS: One-sentence summary covers both benefits and challenges ({word_count} words)")
    return True


if __name__ == "__main__":
    sys.exit(0 if verify() else 1)
