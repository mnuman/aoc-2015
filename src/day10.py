import re

PATTERN = re.compile(r"((.)\2*)")


def look_and_say(s):
    return "".join([f"{len(m[0])}{m[1]}" for m in PATTERN.findall(s)])


def part1(s):
    for i in range(1, 41):
        s = look_and_say(s)
        print(f"Length after iteration {i}: {len(s)}")
    return len(s)


def part2(s):
    for i in range(1, 51):
        s = look_and_say(s)
    return len(s)


if __name__ == "__main__":
    input_data = "1113222113"
    print(part1(input_data))
    print(part2(input_data))
