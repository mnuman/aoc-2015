#!/usr/bin/env python3
"""Tests for Day 25: Let It Snow"""

from day25 import get_position_for_coordinates, generate_code, solve_part1
import unittest
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestDay25(unittest.TestCase):
    """Test cases for Day 25 solution"""

    def test_position_calculation(self):
        """Test the position calculation for various coordinates"""
        test_cases = [
            (1, 1, 1),   # first position
            (2, 1, 2),   # second position
            (1, 2, 3),   # third position
            (3, 1, 4),   # fourth position
            (2, 2, 5),   # fifth position
            (1, 3, 6),   # sixth position
            # mentioned in problem: "the 12th code would be written to row 4, column 2"
            (4, 2, 12),
            # mentioned in problem: "the 15th code would be written to row 1, column 5"
            (1, 5, 15),
        ]

        for row, col, expected_pos in test_cases:
            with self.subTest(row=row, col=col):
                actual_pos = get_position_for_coordinates(row, col)
                self.assertEqual(actual_pos, expected_pos)

    def test_code_generation(self):
        """Test code generation for known values"""
        known_codes = {
            1: 20151125,   # Given as first code
            # Given as second code (calculated in problem description)
            2: 31916031,
            3: 18749137,   # (1,2)
            4: 16080970,   # (3,1)
            5: 21629792,   # (2,2)
            6: 17289845,   # (1,3)
        }

        for pos, expected_code in known_codes.items():
            with self.subTest(position=pos):
                actual_code = generate_code(pos)
                self.assertEqual(actual_code, expected_code)

    def test_solve_part1_with_example(self):
        """Test the full solution with a mock input"""
        test_input = "To continue, please consult the code grid in the manual.  Enter the code at row 4, column 2."
        result = solve_part1(test_input)
        # Position (4,2) is position 12, which should have code 32451966
        self.assertEqual(result, 32451966)


if __name__ == '__main__':
    unittest.main()
