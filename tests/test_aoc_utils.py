import utils.aoc_utils as u


def test_manhattan_distance():
    assert u.manhattan_distance((0, 0), (2, 2)) == 4
