from utils.file_utils import read_file
import re

aunt_sue_data = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}
PATTERN = re.compile(r"(\w*): (\d+)")


def parse_sues(fname):
    sues = dict()
    for sue_number, line in enumerate(read_file(fname), start=1):
        props = dict(PATTERN.findall(line))
        sues[sue_number] = props
    return sues


def compare(prop, reading, sue_value):
    if prop in ["cats", "trees"]:
        return reading < sue_value
    if prop in ["pomeranians", "goldfish"]:
        return reading > sue_value
    return reading == sue_value


def part1(sues):
    for sue, props in sues.items():
        if all(aunt_sue_data.get(k) == int(v) for k, v in props.items()):
            return sue
    return None


def part2(sues):
    for sue, props in sues.items():
        if all(compare(k, aunt_sue_data.get(k), int(v)) for k, v in props.items()):
            return sue
    return None


if __name__ == "__main__":
    sues = parse_sues("day16.txt")
    print(f"Part 1 - Exact matches: {part1(sues)}")
    print(f"Part 2 - With ranges: {part2(sues)}")
    print(part2(sues))
