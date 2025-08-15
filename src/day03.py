from utils.file_utils import read_raw_file


def process_data():
    lines = read_raw_file("day03.txt")
    return [line.strip() for line in lines if line.strip()]


def part1(data):
    currpos = 0, 0
    visited = set(currpos)
    for move in data:
        if move == "^":
            currpos = (currpos[0], currpos[1] + 1)
        elif move == "v":
            currpos = (currpos[0], currpos[1] - 1)
        elif move == ">":
            currpos = (currpos[0] + 1, currpos[1])
        elif move == "<":
            currpos = (currpos[0] - 1, currpos[1])
        visited.add(currpos)
    return len(visited)


def part2(data):
    pass


if __name__ == "__main__":
    data = process_data()
    print(part1(data))
    print(part2(data))
