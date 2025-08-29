#!/usr/bin/env python3

"""
Simple test for Day 22 examples
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from day22 import solve_combat

    print("Testing Example 1:")
    print("Player: 10 HP, 250 mana")
    print("Boss: 13 HP, 8 damage")

    result1 = solve_combat(10, 250, 13, 8, hard_mode=False)
    print(f"Result: {result1}")
    print(f"Expected: 226 (Poison 173 + Magic Missile 53)")

    if result1 == 226:
        print("✓ Example 1 PASSED")
    else:
        print("✗ Example 1 FAILED")

    print("\nTesting Example 2:")
    print("Player: 10 HP, 250 mana")
    print("Boss: 14 HP, 8 damage")

    result2 = solve_combat(10, 250, 14, 8, hard_mode=False)
    print(f"Result: {result2}")

    if result2 is not None and result2 > 0:
        print("✓ Example 2 found a solution")
    else:
        print("✗ Example 2 FAILED")

    print("\nTesting actual puzzle:")
    result3 = solve_combat(50, 500, 51, 9, hard_mode=False)
    print(f"Part 1 Result: {result3}")

    result4 = solve_combat(50, 500, 51, 9, hard_mode=True)
    print(f"Part 2 Result: {result4}")

except ImportError as e:
    print(f"Import error: {e}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
