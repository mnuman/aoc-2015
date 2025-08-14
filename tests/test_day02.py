from day02 import wrap, ribbon


def test_wrap():
    assert wrap(2, 3, 4) == 58
    assert wrap(1, 1, 10) == 43


def test_ribbon():
    assert ribbon(2, 3, 4) == 34
    assert ribbon(1, 1, 10) == 14
