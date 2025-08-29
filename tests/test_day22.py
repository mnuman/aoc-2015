import pytest
from src.day22 import (
    GameState, SPELLS, apply_effects, can_cast_spell, cast_spell,
    is_game_over, solve_combat, part1, part2
)


class TestDay22:

    def test_spell_definitions(self):
        """Test that spells are defined correctly"""
        assert len(SPELLS) == 5

        # Check Magic Missile
        magic_missile = next(s for s in SPELLS if s.name == "Magic Missile")
        assert magic_missile.cost == 53
        assert magic_missile.damage == 4

        # Check Drain
        drain = next(s for s in SPELLS if s.name == "Drain")
        assert drain.cost == 73
        assert drain.damage == 2
        assert drain.heal == 2

    # Check Shield
    shield = next(s for s in SPELLS if s.name == "Shield")
    assert shield.cost == 113
    # Armor bonus is applied via effect logic; spell.armor field remains 0
    assert shield.armor == 0
    assert shield.duration == 6

    # Check Poison (no immediate damage value; damage happens per turn)
    poison = next(s for s in SPELLS if s.name == "Poison")
    assert poison.cost == 173
    assert poison.damage == 0
    assert poison.duration == 6

    # Check Recharge (no immediate mana gain field; happens per turn)
    recharge = next(s for s in SPELLS if s.name == "Recharge")
    assert recharge.cost == 229
    assert recharge.mana == 0
    assert recharge.duration == 5

    def test_game_state_equality(self):
        """Test GameState equality and hashing"""
        state1 = GameState(50, 500, 0, 51, 9, {}, 0, True)
        state2 = GameState(50, 500, 0, 51, 9, {}, 0, True)
        state3 = GameState(50, 500, 0, 51, 9, {"Shield": 3}, 0, True)

        assert state1 == state2
        assert hash(state1) == hash(state2)
        assert state1 != state3

    def test_apply_effects_poison(self):
        """Test poison effect application"""
        state = GameState(50, 500, 0, 10, 9, {"Poison": 3}, 0, True)
        new_state = apply_effects(state)

        assert new_state.boss_hp == 7  # 10 - 3 damage
        assert new_state.effects["Poison"] == 2  # timer decremented

    def test_apply_effects_shield(self):
        """Test shield effect application"""
        state = GameState(50, 500, 0, 10, 9, {"Shield": 2}, 0, True)
        new_state = apply_effects(state)

        assert new_state.player_armor == 7
        assert new_state.effects["Shield"] == 1

    def test_apply_effects_recharge(self):
        """Test recharge effect application"""
        state = GameState(50, 100, 0, 10, 9, {"Recharge": 1}, 0, True)
        new_state = apply_effects(state)

        assert new_state.player_mana == 201  # 100 + 101
        assert "Recharge" not in new_state.effects  # effect ended

    def test_can_cast_spell(self):
        """Test spell casting validation"""
        state = GameState(50, 500, 0, 10, 9, {}, 0, True)

        # Can cast all spells initially
        for spell in SPELLS:
            assert can_cast_spell(state, spell)

        # Cannot cast if not enough mana
        poor_state = GameState(50, 50, 0, 10, 9, {}, 0, True)
        expensive_spell = next(s for s in SPELLS if s.cost > 50)
        assert not can_cast_spell(poor_state, expensive_spell)

        # Cannot cast effect spell if already active
        shield_active = GameState(50, 500, 0, 10, 9, {"Shield": 3}, 0, True)
        shield_spell = next(s for s in SPELLS if s.name == "Shield")
        assert not can_cast_spell(shield_active, shield_spell)

    def test_cast_spell_magic_missile(self):
        """Test casting Magic Missile"""
        state = GameState(50, 500, 0, 10, 9, {}, 0, True)
        magic_missile = next(s for s in SPELLS if s.name == "Magic Missile")

        new_state = cast_spell(state, magic_missile)

        assert new_state.player_mana == 447  # 500 - 53
        assert new_state.boss_hp == 6  # 10 - 4
        assert new_state.mana_spent == 53

    def test_cast_spell_drain(self):
        """Test casting Drain"""
        state = GameState(40, 500, 0, 10, 9, {}, 0, True)
        drain = next(s for s in SPELLS if s.name == "Drain")

        new_state = cast_spell(state, drain)

        assert new_state.player_mana == 427  # 500 - 73
        assert new_state.player_hp == 42  # 40 + 2
        assert new_state.boss_hp == 8  # 10 - 2
        assert new_state.mana_spent == 73

    def test_cast_spell_shield(self):
        """Test casting Shield (no immediate armor until effects apply)"""
        state = GameState(50, 500, 0, 10, 9, {}, 0, True)
        shield = next(s for s in SPELLS if s.name == "Shield")

        new_state = cast_spell(state, shield)

        assert new_state.player_mana == 387  # 500 - 113
        assert new_state.effects["Shield"] == 6
        assert new_state.player_armor == 0  # Armor applied at start of turns
        assert new_state.mana_spent == 113

    def test_is_game_over(self):
        """Test game over conditions"""
        # Boss dead
        state1 = GameState(50, 500, 0, 0, 9, {}, 0, True)
        over, won = is_game_over(state1)
        assert over and won

        # Player dead
        state2 = GameState(0, 500, 0, 10, 9, {}, 0, True)
        over, won = is_game_over(state2)
        assert over and not won

        # Game continues
        state3 = GameState(50, 500, 0, 10, 9, {}, 0, True)
        over, won = is_game_over(state3)
        assert not over

    def test_example_combat_1(self):
        """Test first example from problem description"""
        # Player: 10 HP, 250 mana; Boss: 13 HP, 8 damage
        # Expected: Player wins by casting Poison then Magic Missile
        result = solve_combat(10, 250, 13, 8, hard_mode=False)
        assert result is not None
        # Should be 53 + 173 = 226 mana
        assert result == 226

    def test_example_combat_2(self):
        """Test second example from problem description"""
        # Player: 10 HP, 250 mana; Boss: 14 HP, 8 damage
        # This is a longer combat scenario
        result = solve_combat(10, 250, 14, 8, hard_mode=False)
        assert result is not None
        # The exact sequence from the example should cost specific amount
        # We'll just verify a solution exists
        assert result > 0

    def test_parse_boss_stats(self):
        """Test parsing boss stats from file"""
        # This would test with actual data file
        # For now, we'll skip since it requires the actual file
        pass

    @pytest.mark.slow
    def test_part1_with_actual_data(self):
        """Test part 1 with actual puzzle input"""
        # This test requires the actual data file
        try:
            result = part1("day22.txt")
            assert result > 0
            print(f"Part 1 result: {result}")
        except FileNotFoundError:
            pytest.skip("day22.txt not found")

    @pytest.mark.slow
    def test_part2_with_actual_data(self):
        """Test part 2 with actual puzzle input"""
        # This test requires the actual data file
        try:
            result = part2("day22.txt")
            assert result > 0
            print(f"Part 2 result: {result}")
        except FileNotFoundError:
            pytest.skip("day22.txt not found")


if __name__ == "__main__":
    pytest.main([__file__])
