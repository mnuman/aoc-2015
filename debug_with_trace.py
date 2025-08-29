#!/usr/bin/env python3

"""
Debug version of Day 22 to trace the winning sequence
"""

from day22 import GameState, apply_effects, cast_spell, is_game_over, get_possible_spells
import sys
import os
from typing import Optional, List, Tuple
from dataclasses import dataclass
from heapq import heappush, heappop

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def solve_combat_with_trace(initial_hp: int, initial_mana: int, boss_hp: int, boss_damage: int, hard_mode: bool = False) -> Optional[Tuple[int, List[str]]]:
    """
    Solve the wizard combat and return the minimum mana cost plus the sequence of spells cast.
    """
    @dataclass
    class TrackedState:
        state: GameState
        spell_sequence: List[str]

        def __lt__(self, other):
            return self.state.mana_spent < other.state.mana_spent

    initial_state = GameState(
        player_hp=initial_hp,
        player_mana=initial_mana,
        player_armor=0,
        boss_hp=boss_hp,
        boss_damage=boss_damage,
        effects={},
        mana_spent=0,
        is_player_turn=True
    )

    initial_tracked = TrackedState(initial_state, [])

    # Priority queue: (mana_spent, TrackedState)
    pq = [(0, initial_tracked)]
    visited = set()

    iterations = 0

    while pq:
        current_mana, tracked = heappop(pq)
        state = tracked.state
        spell_sequence = tracked.spell_sequence

        iterations += 1
        if iterations % 10000 == 0:
            print(
                f"Iterations: {iterations}, Current mana: {current_mana}, Queue size: {len(pq)}")

        # Skip if we've seen this state with less mana
        state_key = hash(state)
        if state_key in visited:
            continue
        visited.add(state_key)

        # Apply hard mode penalty at start of player turn
        if hard_mode and state.is_player_turn:
            state = state.copy()
            state.player_hp -= 1
            if state.player_hp <= 0:
                continue  # Player dies, skip this path

        # Apply effects at start of turn
        state = apply_effects(state)

        # Check if game is over after effects
        game_over, player_won = is_game_over(state)
        if game_over:
            if player_won:
                print(f"Found solution after {iterations} iterations!")
                print(f"Spell sequence: {' -> '.join(spell_sequence)}")
                return current_mana, spell_sequence
            else:
                continue  # Player lost, skip this path

        if state.is_player_turn:
            # Player's turn - try casting each possible spell
            possible_spells = get_possible_spells(state)

            if not possible_spells:
                continue  # No spells available, player loses

            for spell in possible_spells:
                new_state = cast_spell(state, spell)
                new_sequence = spell_sequence + [spell.name]

                # Check if boss dies immediately from spell
                game_over, player_won = is_game_over(new_state)
                if game_over:
                    if player_won:
                        print(
                            f"Found immediate solution after {iterations} iterations!")
                        print(f"Spell sequence: {' -> '.join(new_sequence)}")
                        return new_state.mana_spent, new_sequence
                    else:
                        continue

                # Switch to boss turn
                new_state.is_player_turn = False
                new_tracked = TrackedState(new_state, new_sequence)
                heappush(pq, (new_state.mana_spent, new_tracked))

        else:
            # Boss's turn - attack player
            new_state = state.copy()

            # Calculate damage (minimum 1)
            damage = max(1, state.boss_damage - state.player_armor)
            new_state.player_hp -= damage

            # Check if player dies
            if new_state.player_hp <= 0:
                continue  # Player lost, skip this path

            # Switch to player turn
            new_state.is_player_turn = True
            new_tracked = TrackedState(new_state, spell_sequence)
            heappush(pq, (new_state.mana_spent, new_tracked))

    print(f"No solution found after {iterations} iterations")
    return None


def main():
    print("=== Testing Example 1 ===")
    result = solve_combat_with_trace(10, 250, 13, 8, hard_mode=False)
    if result:
        mana, sequence = result
        print(f"Mana cost: {mana}")
        print(f"Sequence: {' -> '.join(sequence)}")
    else:
        print("No solution found")

    print("\n=== Testing Part 1 ===")
    result = solve_combat_with_trace(50, 500, 51, 9, hard_mode=False)
    if result:
        mana, sequence = result
        print(f"Part 1 - Mana cost: {mana}")
        print(f"Sequence: {' -> '.join(sequence)}")
    else:
        print("No solution found")


if __name__ == "__main__":
    main()
