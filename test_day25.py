#!/usr/bin/env python3
"""Test the day25 algorithm with the examples"""

from day25 import get_position_for_coordinates, generate_code
import sys
sys.path.append('/workspaces/aoc-2015/src')


# Test the position calculation with examples from the problem
test_cases = [
    (1, 1, 1),   # first position
    (2, 1, 2),   # second position
    (1, 2, 3),   # third position
    (3, 1, 4),   # fourth position
    (2, 2, 5),   # fifth position
    (1, 3, 6),   # sixth position
    (4, 2, 12),  # mentioned in problem: "the 12th code would be written to row 4, column 2"
    (1, 5, 15),  # mentioned in problem: "the 15th code would be written to row 1, column 5"
]

print("Testing position calculation:")
for row, col, expected_pos in test_cases:
    actual_pos = get_position_for_coordinates(row, col)
    print(f"({row}, {col}) -> position {actual_pos} (expected {expected_pos}) {'✓' if actual_pos == expected_pos else '✗'}")

print("\nTesting code generation:")
# Test with known values from the problem
known_codes = {
    1: 20151125,   # Given as first code
    2: 31916031,   # Given as second code (calculated in problem description)
    # Let's verify a few more from the table
    3: 18749137,   # (1,2)
    4: 16080970,   # (3,1)
    5: 21629792,   # (2,2)
    6: 17289845,   # (1,3)
}

for pos, expected_code in known_codes.items():
    actual_code = generate_code(pos)
    print(
        f"Position {pos}: {actual_code} (expected {expected_code}) {'✓' if actual_code == expected_code else '✗'}")
