from day21 import (
    Character,
    simulate_combat,
    get_equipment_combinations,
    calculate_stats,
    part1,
    part2,
    WEAPONS,
    ARMOR,
    RINGS,
)


def test_character_creation():
    """Test character creation and copying."""
    char = Character(100, 5, 3)
    assert char.hp == 100
    assert char.damage == 5
    assert char.armor == 3

    char_copy = char.copy()
    assert char_copy.hp == char.hp
    assert char_copy.damage == char.damage
    assert char_copy.armor == char.armor


def test_simulate_combat_example():
    """Test the example combat scenario from the problem."""
    player = Character(8, 5, 5)
    boss = Character(12, 7, 2)

    result = simulate_combat(player, boss)
    assert result is True  # Player should win


def test_simulate_combat_player_loses():
    """Test a scenario where the player loses."""
    player = Character(8, 1, 0)  # Very weak player
    boss = Character(12, 7, 2)

    result = simulate_combat(player, boss)
    assert result is False  # Player should lose


def test_equipment_combinations():
    """Test that equipment combinations are generated correctly."""
    combinations = get_equipment_combinations()

    # Should have many combinations
    assert len(combinations) > 0

    # Each combination should have exactly one weapon
    for combo in combinations:
        weapons_in_combo = [item for item in combo if item in WEAPONS]
        assert len(weapons_in_combo) == 1

        # Should have 0 or 1 armor pieces
        armor_in_combo = [item for item in combo if item in ARMOR]
        assert len(armor_in_combo) <= 1

        # Should have 0, 1, or 2 rings
        rings_in_combo = [item for item in combo if item in RINGS]
        assert len(rings_in_combo) <= 2


def test_calculate_stats():
    """Test stat calculation from equipment."""
    # Test with just a weapon
    equipment = [WEAPONS[0]]  # Dagger: cost=8, damage=4, armor=0
    cost, damage, armor = calculate_stats(equipment)
    assert cost == 8
    assert damage == 4
    assert armor == 0

    # Test with weapon + armor + ring
    equipment = [
        WEAPONS[0],  # Dagger: cost=8, damage=4, armor=0
        ARMOR[0],  # Leather: cost=13, damage=0, armor=1
        RINGS[0],  # Damage +1: cost=25, damage=1, armor=0
    ]
    cost, damage, armor = calculate_stats(equipment)
    assert cost == 46  # 8 + 13 + 25
    assert damage == 5  # 4 + 0 + 1
    assert armor == 1  # 0 + 1 + 0


def test_part1_with_weak_boss():
    """Test part 1 with a very weak boss."""
    # Boss that can be defeated with minimal equipment
    min_cost = part1(1, 1, 0)  # HP=1, Damage=1, Armor=0

    # Should be able to win with just the cheapest weapon
    assert min_cost == 8  # Cost of Dagger


def test_part2_with_strong_boss():
    """Test part 2 with a very strong boss."""
    # Boss that's hard to lose against
    max_cost = part2(1000, 1000, 1000)  # Very strong boss

    # Should be able to lose with the most expensive equipment
    assert max_cost > 0
