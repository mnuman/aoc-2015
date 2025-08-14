import utils.file_utils as u


def test_read_file():
    f = u.read_file("test-utils.txt")
    assert len(f) == 6
    assert f[0] == "+1"
    assert f[1] == "-2"


def test_read_file_with_convert():
    f = u.read_file("test-utils.txt", convert=u.toint)
    assert len(f) == 6
    assert f[0] == 1
    assert f[1] == -2


def test_binary_to_int():
    assert u.binary_to_int("0") == 0
    assert u.binary_to_int("00000") == 0
    assert u.binary_to_int("1111") == 15


def test_read_file_g():
    g = u.read_file_g("test-utils.txt")
    lines = [i for i in g]
    assert len(lines) == 6
    assert lines[0] == "+1"
    assert lines[1] == "-2"


def test_read_file_g_convert():
    g = u.read_file_g("test-utils.txt", convert=u.toint)
    lines = [i for i in g]
    assert len(lines) == 6
    assert lines[0] == 1
    assert lines[1] == -2
