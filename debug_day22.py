#!/usr/bin/env python3

"""
Detailed debugging of Day 22 solution
"""

from day22 import GameState, SPELLS, apply_effects, cast_spell, solve_combat
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import with the correct path structure
sys.path.append('/workspaces/aoc-2015/src')


def trace_example_1():
    """
    Trace through the first example step by step to verify logic

    Expected sequence from problem:
    -- Player turn --
    - Player has 10 hit points, 0 armor, 250 mana
    - Boss has 13 hit points
    Player casts Poison.

    -- Boss turn --
    - Player has 10 hit points, 0 armor, 77 mana
    - Boss has 13 hit points
    Poison deals 3 damage; its timer is now 5.
    Boss attacks for 8 damage.

    -- Player turn --
    - Player has 2 hit points, 0 armor, 77 mana
    - Boss has 10 hit points
    Poison deals 3 damage; its timer is now 4.
    Player casts Magic Missile, dealing 4 damage.

    -- Boss turn --
    - Player has 2 hit points, 0 armor, 24 mana
    - Boss has 3 hit points
    Poison deals 3 damage. This kills the boss, and the player wins.
    """
    print("=== Tracing Example 1 ===")

    # Initial state
    state = GameState(
        player_hp=10,
        player_mana=250,
        player_armor=0,
        boss_hp=13,
        boss_damage=8,
        effects={},
        mana_spent=0,
        is_player_turn=True
    )

    print(
        f"Initial: Player {state.player_hp} HP, {state.player_mana} mana; Boss {state.boss_hp} HP")

    # Player turn 1: Cast Poison
    poison = next(s for s in SPELLS if s.name == "Poison")
    state = cast_spell(state, poison)
    print(
        f"After Poison cast: Player {state.player_hp} HP, {state.player_mana} mana (spent {state.mana_spent}); Boss {state.boss_hp} HP")
    print(f"Effects: {state.effects}")

    # Switch to boss turn
    state.is_player_turn = False

    # Boss turn 1: Apply effects, then attack
    state = apply_effects(state)
    print(
        f"After effects: Player {state.player_hp} HP, {state.player_mana} mana; Boss {state.boss_hp} HP")
    print(f"Effects: {state.effects}")

    # Boss attacks
    damage = max(1, state.boss_damage - state.player_armor)
    state.player_hp -= damage
    print(
        f"Boss attacks for {damage} damage: Player {state.player_hp} HP, {state.player_mana} mana; Boss {state.boss_hp} HP")

    # Switch to player turn
    state.is_player_turn = True

    # Player turn 2: Apply effects, then cast Magic Missile
    state = apply_effects(state)
    print(
        f"After effects: Player {state.player_hp} HP, {state.player_mana} mana; Boss {state.boss_hp} HP")
    print(f"Effects: {state.effects}")

    magic_missile = next(s for s in SPELLS if s.name == "Magic Missile")
    state = cast_spell(state, magic_missile)
    print(
        f"After Magic Missile: Player {state.player_hp} HP, {state.player_mana} mana (spent {state.mana_spent}); Boss {state.boss_hp} HP")

    # Switch to boss turn
    state.is_player_turn = False

    # Boss turn 2: Apply effects
    state = apply_effects(state)
    print(
        f"After effects: Player {state.player_hp} HP, {state.player_mana} mana; Boss {state.boss_hp} HP")
    print(f"Effects: {state.effects}")

    if state.boss_hp <= 0:
        print(f"Boss dies! Total mana spent: {state.mana_spent}")
        return state.mana_spent
    else:
        print("Boss still alive, example continues...")
        return None


def test_solve_combat():
    """Test the solve_combat function directly"""
    print("\n=== Testing solve_combat function ===")

    # Test example 1
    result = solve_combat(10, 250, 13, 8, hard_mode=False)
    print(f"Example 1 result: {result}")

    # The manual trace should match
    manual_result = trace_example_1()
    if manual_result and result:
        if manual_result == result:
            print("✓ Manual trace matches solve_combat result")
        else:
            print(
                f"✗ Manual trace ({manual_result}) != solve_combat ({result})")

    # Test example 2
    result2 = solve_combat(10, 250, 14, 8, hard_mode=False)
    print(f"Example 2 result: {result2}")


if __name__ == "__main__":
    manual_cost = trace_example_1()
    test_solve_combat()
