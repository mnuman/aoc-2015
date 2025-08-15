from utils.file_utils import read_file


def process():
    data = read_file("day05.txt")
    return data


def min_three_vowels(s: str) -> bool:
    vowels = "aeiou"
    count = 0
    for char in s:
        if char in vowels:
            count += 1
        if count >= 3:
            return True
    return False


def has_repeated_letter(s: str) -> bool:
    for i in range(len(s) - 1):
        if s[i] == s[i + 1]:
            return True
    return False


def has_forbidden_substring(s: str) -> bool:
    forbidden = ["ab", "cd", "pq", "xy"]
    for sub in forbidden:
        if sub in s:
            return True
    return False


def is_nice_string(s: str) -> bool:
    return (min_three_vowels(s) and has_repeated_letter(s) and not has_forbidden_substring(s))


def has_repeated_pair(s: str) -> bool:
    pairs = {}
    for i in range(len(s) - 1):
        pair = s[i:i + 2]
        if pair in pairs:
            return True
        pairs[pair] = i
    return False


def has_non_overlapping_pairs(s: str) -> bool:
    for i in range(len(s) - 3):
        pair = s[i:i + 2]
        if pair in s[i + 2:]:
            return True
    return False


def has_repeated_letter_with_single_character_in_between(s: str) -> bool:
    for i in range(len(s) - 2):
        if s[i] == s[i + 2]:
            return True
    return False


def is_nice_string_part2(s: str) -> bool:
    return (has_repeated_pair(s) and has_non_overlapping_pairs(s) and has_repeated_letter_with_single_character_in_between(s))


def part1():
    data = process()
    nice_strings = [s for s in data if is_nice_string(s)]
    print(f"Part 1: {len(nice_strings)} nice strings found.")


def part2():
    data = process()
    nice_strings = [s for s in data if is_nice_string_part2(s)]
    print(f"Part 2: {len(nice_strings)} nice strings found.")


if __name__ == "__main__":
    part1()
    part2()
