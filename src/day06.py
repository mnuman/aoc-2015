import re
from utils.file_utils import read_file

PATTERN = re.compile(r"^(\w+ *\w*) (\d+,\d+) through (\d+,\d+)$")


def process_data():
    instructions = []
    data = read_file("day06.txt")
    for line in data:
        match = PATTERN.findall(line)[0]
        if match:
            instructions.append(
                (
                    match[0],
                    tuple(map(int, match[1].split(","))),
                    tuple(map(int, match[2].split(","))),
                )
            )
        else:
            print(f"No match found for {line.strip()}")
    return instructions


def part1(instructions):
    grid = [False] * 1000 * 1000
    for instruction in instructions:
        action, start, end = instruction
        for y in range(start[1], end[1] + 1):
            for x in range(start[0], end[0] + 1):
                if action == "turn on":
                    grid[y * 1000 + x] = True
                elif action == "turn off":
                    grid[y * 1000 + x] = False
                elif action == "toggle":
                    grid[y * 1000 + x] = not grid[y * 1000 + x]
    return sum(grid)


def part2(instructions):
    grid = [0] * 1000 * 1000
    for instruction in instructions:
        action, start, end = instruction
        for y in range(start[1], end[1] + 1):
            for x in range(start[0], end[0] + 1):
                if action == "turn on":
                    grid[y * 1000 + x] += 1
                elif action == "turn off":
                    grid[y * 1000 + x] = max(0, grid[y * 1000 + x] - 1)
                elif action == "toggle":
                    grid[y * 1000 + x] += 2
    return sum(grid)


if __name__ == "__main__":
    instructions = process_data()
    print(f"Part 1: {part1(instructions)}")
    print(f"Part 2: {part2(instructions)}")
