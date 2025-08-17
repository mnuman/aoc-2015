from collections import defaultdict
import re
from utils.file_utils import read_file
from itertools import permutations

PATTERN = re.compile(r"^(\w+) \w+ (\w+) (\d+) .* (\w+)\.$")


def parse_rules(fname):
    rules = defaultdict(dict)
    for line in read_file(fname):
        matches = PATTERN.findall(line)[0]
        val = int(matches[2]) * (1 if matches[1] == "gain" else -1)
        rules[matches[0]][matches[3]] = val
    return rules


def part1(rules):
    all_persons = list(rules.keys())
    max_value = 0
    for permutation in permutations(all_persons, len(all_persons)):
        val = 0
        for pair in zip(permutation, permutation[1:] + (permutation[0],)):
            val += rules[pair[0]][pair[1]] + rules[pair[1]][pair[0]]
        max_value = max(max_value, val)
    return max_value


def part2(rules):
    # Add ME to the rules, which has no preferences. Need to use GET with a default value of 0
    # for both my preferences and the preference of others.
    rules["ME"] = {}
    all_persons = list(rules.keys())
    max_value = 0
    for permutation in permutations(all_persons, len(all_persons)):
        val = 0
        for pair in zip(permutation, permutation[1:] + (permutation[0],)):
            val += rules[pair[0]].get(pair[1], 0) + rules[pair[1]].get(pair[0], 0)
        max_value = max(max_value, val)
    return max_value


if __name__ == "__main__":
    rules = parse_rules("day13.txt")
    print(part1(rules))
    print(part2(rules))
