#!/usr/bin/env python3
"""Convert Celsius temperatures to Fahrenheit and save to a file.

BUG 1: The formula uses subtraction instead of addition for the offset.
BUG 2: The multiplier 9/5 is written as 9/50 (extra zero).
BUG 3: round() is called with 2 decimal places instead of 1.
"""
import os

CELSIUS_TEMPS = [0, 100, -40, 37, 22]


def celsius_to_fahrenheit(c):
    # BUG 1: should be + 32, not - 32
    # BUG 2: should be 9/5, not 9/50
    return (c * 9 / 50) - 32


def main():
    os.makedirs("results", exist_ok=True)
    with open("results/temperatures.txt", "w") as f:
        for c in CELSIUS_TEMPS:
            # BUG 3: should round to 1 decimal place, not 2
            f.write(f"{round(celsius_to_fahrenheit(c), 2)}\n")


if __name__ == "__main__":
    main()
