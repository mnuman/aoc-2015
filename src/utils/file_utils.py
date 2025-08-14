import os
from typing import Any, Callable, Optional

"""Module implementing miscellaneous utility functions for ramblings in AoC, 2024"""


def toint(s: str):
    """Inline conversion function from string to integer"""
    return int(s)


def read_raw_file(filename: str, directory: str = "/workspaces/aoc-2015/data") -> str:
    """Parse input file, return a list of stripped lines; if separator is
    specified, break up the individual lines on the separator as well
    """
    filepath = filename if directory is None else os.path.join(directory, filename)
    with open(filepath) as f:  # pylint: disable=C0103
        content = f.read()
    return content


def read_file(
    filename: str,
    directory: str = "/workspaces/aoc-2015/data",
    separator: Optional[str] = None,
    convert: Optional[Callable[[str], Any]] = None,
) -> list[str] | list[Any]:
    """Parse input file, return a list of stripped lines; if separator is
    specified, break up the individual lines on the separator as well
    """
    filepath = filename if directory is None else os.path.join(directory, filename)
    with open(filepath) as f:  # pylint: disable=C0103
        content = f.readlines()
    if separator is None:
        if convert is None:
            result = [line.strip() for line in content]
        else:
            result = [convert(line.strip()) for line in content]
    else:
        if convert is None:
            result = [
                field for line in content for field in line.strip().split(separator)
            ]
        else:
            result = [
                convert(field)
                for line in content
                for field in line.strip().split(separator)
            ]
    return result


def binary_to_int(binary_number: str) -> int:
    """Convert a binary number represented as a string to its integer value"""
    return int(binary_number, base=2)


def id(s: Any) -> Any:
    return s


def read_file_g(
    filename: str,
    directory: str = "/workspaces/aoc-2015/data",
    separator: Optional[str] = None,
    convert: Callable[[str], Any] = id,
) -> Any:
    """Attempting a more fluent, pipelined approach using generators. If a separator
    is specified, the line will be separated. All atoms will be converted using
    the convert function.
    """
    filepath = filename if directory is None else os.path.join(directory, filename)
    with open(filepath) as f:
        continue_reading = True
        while continue_reading:
            line = f.readline().strip()
            continue_reading = line != ""
            if continue_reading:
                if separator is None:
                    yield convert(line)
                else:
                    yield map(convert, line.split(separator))


def manhattan_distance(x: tuple[int, int], y: tuple[int, int]) -> int:
    return abs(x[0] - y[0]) + abs(x[1] - y[1])
