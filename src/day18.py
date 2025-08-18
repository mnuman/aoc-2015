from utils.file_utils import read_file
from utils.aoc_utils import neighbours
from copy import deepcopy

ON = "#"
OFF = "."


def parse_input(file_path):
    data = [[c for c in line] for line in read_file(file_path)]
    return data


def next_value(data, r, c, cell):
    neighbours_on = sum(
        1
        for nr, nc in neighbours(r, c, len(data), len(data[0]), include_diagonals=True)
        if data[nr][nc] == ON
    )
    if cell == ON:
        return ON if neighbours_on in (2, 3) else OFF
    else:
        return ON if neighbours_on == 3 else OFF


def part1(data):
    for i in range(1, 101):
        next_cycle = list()
        for r, row in enumerate(data):
            line = list()
            for c, cell in enumerate(row):
                line.append(next_value(data, r, c, cell))
            next_cycle.append(line)
        on_count = sum(cell == ON for row in next_cycle for cell in row)
        print(f"After {i} cycles: {on_count} lights on")
        data = next_cycle


def part2(data):
    max_dim = len(data) - 1
    data[0][0] = ON
    data[0][max_dim] = ON
    data[max_dim][0] = ON
    data[max_dim][max_dim] = ON

    for i in range(1, 101):
        next_cycle = list()
        for r, row in enumerate(data):
            line = list()
            for c, cell in enumerate(row):
                nv = (
                    ON
                    if r in (0, len(data) - 1) and c in (0, len(data[0]) - 1)
                    else next_value(data, r, c, cell)
                )
                line.append(nv)
            next_cycle.append(line)
        # dump(next_cycle)
        on_count = sum(cell == ON for row in next_cycle for cell in row)
        print(f"After {i} cycles: {on_count} lights on")
        data = next_cycle


def dump(data):
    for row in data:
        print("".join(row))
    print()


if __name__ == "__main__":
    input_data = parse_input("day18.txt")
    print(f"Part 1: {part1(deepcopy(input_data))}")
    print(f"Part 2: {part2(deepcopy(input_data))}")
