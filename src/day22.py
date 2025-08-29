try:
    # when running as script with src on PYTHONPATH
    from utils.file_utils import read_file
except ModuleNotFoundError:  # pragma: no cover
    # Fallback when tests import via 'from src.day22 import ...'
    from src.utils.file_utils import read_file
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from heapq import heappush, heappop
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@dataclass
class Spell:
    name: str
    cost: int
    damage: int = 0
    heal: int = 0
    armor: int = 0
    mana: int = 0
    duration: int = 0


@dataclass
class GameState:
    player_hp: int
    player_mana: int
    player_armor: int
    boss_hp: int
    boss_damage: int
    effects: Dict[str, int]  # effect_name -> turns_remaining
    mana_spent: int
    is_player_turn: bool

    def copy(self):
        return GameState(
            self.player_hp,
            self.player_mana,
            self.player_armor,
            self.boss_hp,
            self.boss_damage,
            self.effects.copy(),
            self.mana_spent,
            self.is_player_turn,
        )

    def __hash__(self):
        return hash(
            (
                self.player_hp,
                self.player_mana,
                self.player_armor,
                self.boss_hp,
                tuple(sorted(self.effects.items())),
                self.is_player_turn,
            )
        )

    def __eq__(self, other):
        return (
            self.player_hp == other.player_hp
            and self.player_mana == other.player_mana
            and self.player_armor == other.player_armor
            and self.boss_hp == other.boss_hp
            and self.effects == other.effects
            and self.is_player_turn == other.is_player_turn
        )

    def __lt__(self, other):
        # For priority queue - compare by mana spent first
        return self.mana_spent < other.mana_spent


# Available spells
# NOTE:
# For effect spells (Shield, Poison, Recharge) we do NOT encode their per-turn
# behavior in the Spell fields (except duration). Their ongoing impact is
# handled explicitly inside apply_effects based on the effect name. In the
# original implementation Poison incorrectly applied its 3 damage immediately
# upon casting because its damage value was set in the Spell definition.
# According to the puzzle description, Poison only deals damage at the start
# of each turn while active – not immediately when cast. Likewise Recharge
# only grants mana at the start of turns. Shield's armor bonus is applied at
# the start of each turn while active (which includes the very next boss turn
# right after being cast).
SPELLS = [
    Spell("Magic Missile", 53, damage=4),  # Instant 4 damage
    Spell("Drain", 73, damage=2, heal=2),  # Instant 2 damage + 2 heal
    # Effect: +7 armor during apply_effects
    Spell("Shield", 113, duration=6),
    # Effect: deal 3 damage each apply_effects
    Spell("Poison", 173, duration=6),
    # Effect: +101 mana each apply_effects
    Spell("Recharge", 229, duration=5),
]


def apply_effects(state: GameState) -> GameState:
    """Apply all active effects and decrement their timers"""
    state = state.copy()

    # Reset armor to 0 (shield effect will reapply if active)
    state.player_armor = 0

    # Apply effects
    for effect_name in list(state.effects.keys()):
        if effect_name == "Shield":
            state.player_armor = 7
        elif effect_name == "Poison":
            state.boss_hp -= 3
        elif effect_name == "Recharge":
            state.player_mana += 101

        # Decrement timer
        state.effects[effect_name] -= 1
        if state.effects[effect_name] <= 0:
            del state.effects[effect_name]

    return state


def can_cast_spell(state: GameState, spell: Spell) -> bool:
    """Check if a spell can be cast"""
    # Must have enough mana
    if state.player_mana < spell.cost:
        return False

    # Cannot cast effect spells that are already active
    if spell.duration > 0 and spell.name in state.effects:
        return False

    return True


def cast_spell(state: GameState, spell: Spell) -> GameState:
    """Cast a spell and return the new state"""
    state = state.copy()

    # Deduct mana cost
    state.player_mana -= spell.cost
    state.mana_spent += spell.cost

    # Apply immediate effects
    if spell.damage > 0:
        state.boss_hp -= spell.damage

    if spell.heal > 0:
        state.player_hp += spell.heal

    # Start effect spells
    if spell.duration > 0:
        state.effects[spell.name] = spell.duration

    return state


def is_game_over(state: GameState) -> Tuple[bool, bool]:
    """Check if game is over. Returns (is_over, player_won)"""
    if state.boss_hp <= 0:
        return True, True
    if state.player_hp <= 0:
        return True, False
    return False, False


def get_possible_spells(state: GameState) -> List[Spell]:
    """Get all spells that can be cast in the current state"""
    return [spell for spell in SPELLS if can_cast_spell(state, spell)]


def solve_combat(
    initial_hp: int,
    initial_mana: int,
    boss_hp: int,
    boss_damage: int,
    hard_mode: bool = False,
) -> Optional[int]:
    """
    Solve the wizard combat using Dijkstra's algorithm.
    Returns the minimum mana cost to win, or None if impossible.
    """
    initial_state = GameState(
        player_hp=initial_hp,
        player_mana=initial_mana,
        player_armor=0,
        boss_hp=boss_hp,
        boss_damage=boss_damage,
        effects={},
        mana_spent=0,
        is_player_turn=True,
    )

    # Priority queue: (mana_spent, state)
    pq = [(0, initial_state)]
    visited = set()

    while pq:
        current_mana, state = heappop(pq)

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
                return current_mana
            else:
                continue  # Player lost, skip this path

        if state.is_player_turn:
            # Player's turn - try casting each possible spell
            possible_spells = get_possible_spells(state)

            if not possible_spells:
                continue  # No spells available, player loses

            for spell in possible_spells:
                new_state = cast_spell(state, spell)

                # Check if boss dies immediately from spell
                game_over, player_won = is_game_over(new_state)
                if game_over:
                    if player_won:
                        return new_state.mana_spent
                    else:
                        continue

                # Switch to boss turn
                new_state.is_player_turn = False
                heappush(pq, (new_state.mana_spent, new_state))

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
            heappush(pq, (new_state.mana_spent, new_state))

    return None  # No solution found


# ---- Recursive DFS solver (authoritative minimal search) ---- #


def _apply_effects_for_dfs(
    player_hp: int, player_mana: int, boss_hp: int, effects: Dict[str, int]
) -> tuple[int, int, int, Dict[str, int], int]:
    """Apply effects (for DFS path). Returns updated (player_hp, player_mana, boss_hp, new_effects, armor)."""
    armor = 0
    new_effects: Dict[str, int] = {}
    for name, timer in effects.items():
        if name == "Shield":
            armor = 7  # active this turn
        if name == "Poison":
            boss_hp -= 3
        if name == "Recharge":
            player_mana += 101
        if timer - 1 > 0:
            new_effects[name] = timer - 1
    return player_hp, player_mana, boss_hp, new_effects, armor


def solve_combat_dfs(
    initial_hp: int,
    initial_mana: int,
    boss_hp: int,
    boss_damage: int,
    hard_mode: bool = False,
) -> Optional[int]:
    """Depth-first exhaustive search with pruning to guarantee minimal mana."""
    best: Optional[int] = None
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def dfs(
        player_hp: int,
        player_mana: int,
        boss_hp: int,
        effects_key: Tuple[Tuple[str, int], ...],
        player_turn: bool,
        mana_spent: int,
    ) -> Optional[int]:
        nonlocal best
        # Prune if already worse than known best
        if best is not None and mana_spent >= best:
            return None

        # Reconstruct effects dict from key
        effects = {k: v for k, v in effects_key}

        if player_turn:
            # Hard mode penalty FIRST
            if hard_mode:
                player_hp -= 1
                if player_hp <= 0:
                    return None

        # Apply effects
        player_hp, player_mana, boss_hp, effects, armor = _apply_effects_for_dfs(
            player_hp, player_mana, boss_hp, effects
        )

        # Boss dead after effects?
        if boss_hp <= 0:
            if best is None or mana_spent < best:
                best = mana_spent
            return mana_spent

        if player_turn:
            # Try each castable spell
            result_any = None
            for spell in SPELLS:
                # Can't afford
                if player_mana < spell.cost:
                    continue
                # Effect already active
                if spell.duration > 0 and spell.name in effects:
                    continue
                # Spend cost
                new_player_mana = player_mana - spell.cost
                new_mana_spent = mana_spent + spell.cost
                new_player_hp = player_hp
                new_boss_hp = boss_hp
                new_effects = effects.copy()

                # Immediate effects
                if spell.damage:
                    new_boss_hp -= spell.damage
                if spell.heal:
                    new_player_hp += spell.heal
                if spell.duration:
                    new_effects[spell.name] = spell.duration

                # Win check
                if new_boss_hp <= 0:
                    if best is None or new_mana_spent < best:
                        best = new_mana_spent
                    result_any = (
                        new_mana_spent
                        if (result_any is None or new_mana_spent < result_any)
                        else result_any
                    )
                    continue

                dfs(
                    new_player_hp,
                    new_player_mana,
                    new_boss_hp,
                    tuple(sorted(new_effects.items())),
                    False,
                    new_mana_spent,
                )
            return result_any
        else:
            # Boss turn: boss attacks (after effects already applied above).
            damage = max(1, boss_damage - armor)
            player_hp -= damage
            if player_hp <= 0:
                return None
            return dfs(
                player_hp,
                player_mana,
                boss_hp,
                tuple(sorted(effects.items())),
                True,
                mana_spent,
            )

    dfs(initial_hp, initial_mana, boss_hp, tuple(), True, 0)
    return best


def parse_boss_stats(filename: str) -> Tuple[int, int]:
    """Parse boss stats from input file"""
    lines = read_file(filename)
    hp = int(lines[0].split(": ")[1])
    damage = int(lines[1].split(": ")[1])
    return hp, damage


def part1(filename: str) -> int:
    """Solve part 1: minimum mana to win (DFS authoritative)."""
    boss_hp, boss_damage = parse_boss_stats(filename)
    result = solve_combat_dfs(50, 500, boss_hp, boss_damage, hard_mode=False)
    return result if result is not None else -1


def part2(filename: str) -> int:
    """Solve part 2: minimum mana to win in hard mode (DFS authoritative)."""
    boss_hp, boss_damage = parse_boss_stats(filename)
    result = solve_combat_dfs(50, 500, boss_hp, boss_damage, hard_mode=True)
    return result if result is not None else -1


def main():
    """Main function to run both parts"""
    filename = "day22.txt"

    print("Day 22: Wizard Simulator 20XX")
    print("=" * 40)

    result1 = part1(filename)
    print(f"Part 1 - Minimum mana to win: {result1}")

    result2 = part2(filename)
    print(f"Part 2 - Minimum mana to win (hard mode): {result2}")


if __name__ == "__main__":
    main()
