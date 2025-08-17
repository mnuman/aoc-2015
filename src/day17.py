from utils.file_utils import read_file


def parse(fname):
    data = []
    for line in read_file(fname):
        # Assuming each line is a number
        data.append(int(line.strip()))
    return data


def part1(containers):
    target = 150
    count = 0

    def backtrack(remaining, start):
        nonlocal count
        if remaining == 0:
            count += 1
            return
        for i in range(start, len(containers)):
            if containers[i] <= remaining:
                backtrack(remaining - containers[i], i + 1)

    backtrack(target, 0)
    return count


def part2(containers):
    target = 150
    solutions = []

    def backtrack(remaining, start, used):
        nonlocal solutions
        if remaining == 0:
            solutions.append(used.copy())
            return
        for i in range(start, len(containers)):
            if containers[i] <= remaining:
                used.append(containers[i])
                backtrack(remaining - containers[i], i + 1, used)
                used.pop()

    backtrack(target, 0, [])
    for sol in solutions:
        if sum(sol) != 150:
            print(f"Part 2 - Invalid combination found: {sol}")
            continue
    return solutions


if __name__ == "__main__":
    data = parse("day17.txt")
    print(f"Parsed data: {data}")
    print(f"Part 1 - Exact matches: {part1(data)}")
    solutions = part2(data)
    # print(f"Part 2 - All combinations: {solutions}")
    print(f"Part 2 - Number of combinations: {len(solutions)}")
    min_containers = min(len(sol) for sol in solutions) if solutions else None
    print(f"Part 2 - Smallest combination: {min_containers}")
    print(
        f"Part 2 - Total combinations with {min_containers}: {sum(1 for sol in solutions if len(sol) == min_containers)}"
    )
