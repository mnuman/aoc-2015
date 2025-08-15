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
    santapos: tuple[int, int] = (0, 0)
    robopos: tuple[int, int] = (0, 0)
    visited: set[tuple[int, int]] = {santapos}

    for i, move in enumerate(data):
        # Alternate between Santa (even indices) and Robo (odd indices)
        if i % 2 == 0:  # Santa's turn
            if move == "^":
                santapos = (santapos[0], santapos[1] + 1)
            elif move == "v":
                santapos = (santapos[0], santapos[1] - 1)
            elif move == ">":
                santapos = (santapos[0] + 1, santapos[1])
            elif move == "<":
                santapos = (santapos[0] - 1, santapos[1])
            visited.add(santapos)
        else:  # Robo's turn
            if move == "^":
                robopos = (robopos[0], robopos[1] + 1)
            elif move == "v":
                robopos = (robopos[0], robopos[1] - 1)
            elif move == ">":
                robopos = (robopos[0] + 1, robopos[1])
            elif move == "<":
                robopos = (robopos[0] - 1, robopos[1])
            visited.add(robopos)

    return len(visited)


if __name__ == "__main__":
    data = process_data()
    print(part1(data))
    print(part2(data))
