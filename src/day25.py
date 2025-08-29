#!/usr/bin/env python3
"""
Day 25: Let It Snow
"""

from utils.file_utils import read_raw_file


def get_position_for_coordinates(row, col):
    """
    Convert row/column coordinates to position in the diagonal sequence.

    Looking at the pattern:
    Diagonal 1: (1,1) -> 1
    Diagonal 2: (2,1) -> 2, (1,2) -> 3
    Diagonal 3: (3,1) -> 4, (2,2) -> 5, (1,3) -> 6
    Diagonal 4: (4,1) -> 7, (3,2) -> 8, (2,3) -> 9, (1,4) -> 10

    Within each diagonal d (where d = row + col - 1):
    - We start from (d,1) and go to (1,d)
    - So (row, col) is the (d - row + 1)th element in the diagonal
    Wait, that's not right either.

    Let me be more systematic:
    Diagonal d contains positions where row + col = d + 1
    Within diagonal d, positions are filled in order:
    (d,1), (d-1,2), (d-2,3), ..., (1,d)

    So for (row, col) in diagonal d:
    - position within diagonal = d - row + 1
    """
    diagonal = row + col - 1

    # Number of positions before this diagonal
    positions_before_diagonal = (diagonal - 1) * diagonal // 2

    # Position within the diagonal (starting from 1)
    # In diagonal d, we have: (d,1), (d-1,2), (d-2,3), ..., (1,d)
    # So for (row, col), it's the (diagonal - row + 1)th position
    position_in_diagonal = diagonal - row + 1

    return positions_before_diagonal + position_in_diagonal


def generate_code(position):
    """
    Generate the code at the given position.

    First code: 20151125
    Each subsequent: (previous * 252533) % 33554393
    """
    code = 20151125

    for _ in range(position - 1):
        code = (code * 252533) % 33554393

    return code


def solve_part1(input_text):
    """
    Parse the input to get row and column, then find the code.
    """
    # Parse input like "To continue, please consult the code grid in the manual.  Enter the code at row 3010, column 3019."
    words = input_text.strip().split()

    # Find row and column numbers
    row_idx = words.index("row") + 1
    col_idx = words.index("column") + 1

    row = int(words[row_idx].rstrip(","))
    col = int(words[col_idx].rstrip("."))

    print(f"Looking for code at row {row}, column {col}")

    position = get_position_for_coordinates(row, col)
    print(f"This is position {position} in the sequence")

    code = generate_code(position)
    return code


def main():
    input_text = read_raw_file("day25.txt")

    result1 = solve_part1(input_text)
    print(f"Part 1: {result1}")


if __name__ == "__main__":
    main()
