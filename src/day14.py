from utils.file_utils import read_file


def parse(fname: str) -> dict[str, tuple[int, int, int]]:
    """
    Parse the input file and return a dictionary mapping each reindeer to its speed,
    flying time, and resting time.
    """
    reindeer = {}
    for line in read_file(fname):
        parts = line.split()
        name = parts[0]
        speed = int(parts[3])
        fly_time = int(parts[6])
        rest_time = int(parts[13])
        reindeer[name] = (speed, fly_time, rest_time)
    return reindeer


def part1(reindeer):
    max_dist = 0
    for name, (speed, fly_time, rest_time) in reindeer.items():
        total_time = fly_time + rest_time
        full_cycles = 2503 // total_time
        remaining_time = 2503 % total_time
        distance = full_cycles * speed * fly_time
        distance += min(remaining_time, fly_time) * speed
        max_dist = max(max_dist, distance)
    return max_dist


def part2(reindeer):
    points = {name: 0 for name in reindeer}
    distances = {name: 0 for name in reindeer}

    for t in range(1, 2504):
        for name, (speed, fly_time, rest_time) in reindeer.items():
            if 1 <= t % (fly_time + rest_time) <= fly_time:
                distances[name] += speed

        # update score board after every cycle
        max_dist = max(distances.values())
        for name, dist in distances.items():
            if dist == max_dist:
                points[name] += 1

    return max(points.values())


if __name__ == "__main__":
    reindeer = parse("day14.txt")
    print(reindeer)
    print(part1(reindeer))
    print(part2(reindeer))
