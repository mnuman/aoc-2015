import utils.aoc_utils as u


def test_manhattan_distance():
    assert u.manhattan_distance((0, 0), (2, 2)) == 4


def test_neighbours():
    assert u.lists_equal_any_order(
        u.neighbours(1, 1, 3, 3), [(0, 1), (2, 1), (1, 0), (1, 2)]
    )
    assert u.lists_equal_any_order(
        u.neighbours(0, 0, 3, 3, include_diagonals=True), [(0, 1), (1, 0), (1, 1)]
    )


def test_lists_equal_any_order():
    # Test identical lists
    assert u.lists_equal_any_order([1, 2, 3], [1, 2, 3])

    # Test lists with same elements in different order
    assert u.lists_equal_any_order([1, 2, 3], [3, 1, 2])
    assert u.lists_equal_any_order([1, 2, 3], [2, 3, 1])

    # Test lists with duplicates
    assert u.lists_equal_any_order([1, 2, 2, 3], [2, 1, 3, 2])
    assert u.lists_equal_any_order([1, 1, 2], [1, 2, 1])

    # Test different lists
    assert not u.lists_equal_any_order([1, 2, 3], [1, 2, 4])
    assert not u.lists_equal_any_order([1, 2], [1, 2, 3])
    assert not u.lists_equal_any_order([1, 2, 2], [1, 2])

    # Test empty lists
    assert u.lists_equal_any_order([], [])
    assert not u.lists_equal_any_order([1], [])

    # Test with strings
    assert u.lists_equal_any_order(["a", "b", "c"], ["c", "a", "b"])
    assert not u.lists_equal_any_order(["a", "b"], ["a", "c"])
