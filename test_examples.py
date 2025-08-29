#!/usr/bin/env python3

"""
Quick test of the examples provided in the problem description
"""

from src.day22 import solve_combat
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_example_1():
    """
    First example: Player has 10 HP, 250 mana; Boss has 13 HP, 8 damage
    Expected sequence: Poison (173 mana) -> Magic Missile (53 mana) = 226 total
    """
    print("Testing Example 1:")
    print("Player: 10 HP, 250 mana")
    print("Boss: 13 HP, 8 damage")

    result = solve_combat(10, 250, 13, 8, hard_mode=False)
    print(f"Minimum mana cost: {result}")

    # The example shows this sequence:
    # 1. Cast Poison (173 mana) - boss takes 3 damage per turn for 6 turns
    # 2. Boss attacks for 8 damage (player down to 2 HP)
    # 3. Cast Magic Missile (53 mana) - deals 4 damage
    # 4. Boss dies from poison (3 damage)
    # Total: 173 + 53 = 226 mana

    assert result == 226, f"Expected 226 mana, got {result}"
    print("✓ Example 1 passed!")
    print()


def test_example_2():
    """
    Second example: Player has 10 HP, 250 mana; Boss has 14 HP, 8 damage
    This is a longer combat that should have a solution
    """
    print("Testing Example 2:")
    print("Player: 10 HP, 250 mana")
    print("Boss: 14 HP, 8 damage")

    result = solve_combat(10, 250, 14, 8, hard_mode=False)
    print(f"Minimum mana cost: {result}")

    # The example shows this sequence with total costs:
    # Recharge (229) + Shield (113) + Drain (73) + Poison (173) + Magic Missile (53)
    # Total: 641 mana (but this might not be optimal)

    assert result is not None, "Should have found a solution"
    assert result > 0, f"Expected positive mana cost, got {result}"
    print(f"✓ Example 2 found solution with {result} mana")
    print()


if __name__ == "__main__":
    test_example_1()
    test_example_2()
    print("All example tests passed!")
