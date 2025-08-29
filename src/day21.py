from itertools import combinations
from typing import NamedTuple, List
import os


class Item(NamedTuple):
    name: str
    cost: int
    damage: int
    armor: int


class Character:
    def __init__(self, hp: int, damage: int, armor: int):
        self.hp = hp
        self.damage = damage
        self.armor = armor

    def copy(self):
        return Character(self.hp, self.damage, self.armor)


# Shop inventory
WEAPONS = [
    Item("Dagger", 8, 4, 0),
    Item("Shortsword", 10, 5, 0),
    Item("Warhammer", 25, 6, 0),
    Item("Longsword", 40, 7, 0),
    Item("Greataxe", 74, 8, 0),
]

ARMOR = [
    Item("Leather", 13, 0, 1),
    Item("Chainmail", 31, 0, 2),
    Item("Splintmail", 53, 0, 3),
    Item("Bandedmail", 75, 0, 4),
    Item("Platemail", 102, 0, 5),
]

RINGS = [
    Item("Damage +1", 25, 1, 0),
    Item("Damage +2", 50, 2, 0),
    Item("Damage +3", 100, 3, 0),
    Item("Defense +1", 20, 0, 1),
    Item("Defense +2", 40, 0, 2),
    Item("Defense +3", 80, 0, 3),
]


def simulate_combat(player: Character, boss: Character) -> bool:
    """Simulate combat between player and boss. Returns True if player wins."""
    player_copy = player.copy()
    boss_copy = boss.copy()

    while player_copy.hp > 0 and boss_copy.hp > 0:
        # Player attacks first
        damage_to_boss = max(1, player_copy.damage - boss_copy.armor)
        boss_copy.hp -= damage_to_boss

        if boss_copy.hp <= 0:
            return True

        # Boss attacks
        damage_to_player = max(1, boss_copy.damage - player_copy.armor)
        player_copy.hp -= damage_to_player

    return False


def get_equipment_combinations():
    """Generate all valid equipment combinations."""
    combinations_list = []

    # Must buy exactly one weapon
    for weapon in WEAPONS:
        # Armor is optional (0 or 1)
        for armor_count in range(2):
            armor_choices = [None] if armor_count == 0 else ARMOR

            for armor in armor_choices:
                # Rings: 0, 1, or 2 rings
                for ring_count in range(3):
                    if ring_count == 0:
                        ring_combinations = [()]
                    elif ring_count == 1:
                        ring_combinations = [(ring,) for ring in RINGS]
                    else:  # ring_count == 2
                        ring_combinations = list(combinations(RINGS, 2))

                    for rings in ring_combinations:
                        equipment = [weapon]
                        if armor:
                            equipment.append(armor)
                        equipment.extend(rings)
                        combinations_list.append(equipment)

    return combinations_list


def calculate_stats(equipment: List[Item]) -> tuple[int, int, int]:
    """Calculate total cost, damage, and armor from equipment."""
    total_cost = sum(item.cost for item in equipment)
    total_damage = sum(item.damage for item in equipment)
    total_armor = sum(item.armor for item in equipment)
    return total_cost, total_damage, total_armor


def part1(boss_hp: int, boss_damage: int, boss_armor: int) -> int:
    """Find minimum gold to spend and still win the fight."""
    min_cost = None

    for equipment in get_equipment_combinations():
        cost, damage, armor = calculate_stats(equipment)

        player = Character(100, damage, armor)
        boss = Character(boss_hp, boss_damage, boss_armor)

        if simulate_combat(player, boss):
            min_cost = cost if min_cost is None else min(min_cost, cost)

    return min_cost or 0


def part2(boss_hp: int, boss_damage: int, boss_armor: int) -> int:
    """Find maximum gold to spend and still lose the fight."""
    max_cost = 0

    for equipment in get_equipment_combinations():
        cost, damage, armor = calculate_stats(equipment)

        player = Character(100, damage, armor)
        boss = Character(boss_hp, boss_damage, boss_armor)

        if not simulate_combat(player, boss):
            max_cost = max(max_cost, cost)

    return max_cost


def parse_boss_stats(filename: str = "day21.txt") -> tuple[int, int, int]:
    """Parse boss stats from input file."""
    filepath = os.path.join("/workspaces/aoc-2015/data", filename)
    with open(filepath) as f:
        lines = f.read().strip().split("\n")

    stats = {}
    for line in lines:
        key, value = line.split(": ")
        stats[key] = int(value)

    return stats["Hit Points"], stats["Damage"], stats["Armor"]


def main():
    # Example from problem description
    print("Testing with example:")
    player = Character(8, 5, 5)
    boss = Character(12, 7, 2)
    result = simulate_combat(player, boss)
    print(f"Player wins: {result}")

    # Parse boss stats from input file
    boss_hp, boss_damage, boss_armor = parse_boss_stats()
    print(f"\nBoss stats: HP={boss_hp}, Damage={boss_damage}, Armor={boss_armor}")

    print(f"Part 1 - Minimum gold to win: {part1(boss_hp, boss_damage, boss_armor)}")
    print(f"Part 2 - Maximum gold to lose: {part2(boss_hp, boss_damage, boss_armor)}")


if __name__ == "__main__":
    main()
