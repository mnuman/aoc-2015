from day20 import presents


def test_presents():
    assert presents(1) == 10
    assert presents(2) == 30
    assert presents(3) == 40
    assert presents(4) == 70
    assert presents(5) == 60
    assert presents(6) == 120
    assert presents(7) == 80
    assert presents(8) == 150
    assert presents(9) == 130
