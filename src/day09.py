from utils.file_utils import read_file


def parse(fname):
    lines = read_file(fname)
    # Process the lines to extract the relevant information
    data = {}
    for line in lines:
        cities, *distance = line.split(" = ")
        c0, c1 = cities.split(" to ")
        data[(c0, c1)] = int(distance[0])
        data[(c1, c0)] = int(distance[0])
    return data


def part1(fname):
    data = parse(fname)
    from itertools import permutations

    # Generate all permutations of the cities
    cities = set(c for c0, c1 in data.keys() for c in (c0, c1))
    min_distance = float("inf")

    for perm in permutations(cities):
        distance = sum(data[(perm[i], perm[i + 1])] for i in range(len(perm) - 1))
        min_distance = min(min_distance, distance)

    return min_distance


def part2(fname):
    data = parse(fname)
    from itertools import permutations

    # Generate all permutations of the cities
    cities = set(c for c0, c1 in data.keys() for c in (c0, c1))
    max_distance = 0.0
    for perm in permutations(cities):
        distance = sum(data[(perm[i], perm[i + 1])] for i in range(len(perm) - 1))
        max_distance = max(max_distance, distance)

    return max_distance


if __name__ == "__main__":
    print(part1("day09.txt"))
    print(part2("day09.txt"))
