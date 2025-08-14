from utils.file_utils import read_file


def process_data():
    lines = read_file("day02.txt")
    return [tuple(map(int, line.split("x"))) for line in lines]


def part1(data):
    return sum(wrap(length, width, height) for length, width, height in data)


def wrap(length: int, width: int, height: int) -> int:
    return 2 * (length * width + width * height + height * length) + min(
        length * width, width * height, height * length
    )


def ribbon(length: int, width: int, height: int) -> int:
    return (
        2 * min(length + width, width + height, height + length)
        + length * width * height
    )


def part2(data):
    return sum(ribbon(length, width, height) for length, width, height in data)


if __name__ == "__main__":
    data = process_data()
    print(part1(data))
    print(part2(data))
