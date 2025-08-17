from utils.file_utils import read_file


def part1(fname):
    lines = read_file(fname)
    raw = 0
    in_memory = 0
    # Process the lines to extract the relevant information
    for line in lines:
        raw += len(line)
        in_memory += len(eval(line))
        # print(
        #     f"Processing line: {line}, length: {len(line) - 2}, evaluated length: {len(eval(line))}, running raw: {raw}, in-memory: {in_memory}"
        # )
    print(f"Raw length: {raw}, in-memory length: {in_memory} --> {raw - in_memory}")


def part2(fname):
    lines = read_file(fname)
    raw = 0
    encoded = 0
    # Process the lines to extract the relevant information
    for line in lines:
        raw += len(line)
        # every quotation mark or backslash incurs and extra character, plus two additional quotation marks to encode the string itself
        encoded += len(line) + line.count('"') + line.count("\\") + 2
        # print(
        #     f"Processing line: {line}, length: {len(line) - 2}, encoded length: {encoded}, running raw: {raw}, encoded: {encoded}"
        # )
    print(f"Raw length: {raw}, encoded length: {encoded} --> {encoded - raw}")


if __name__ == "__main__":
    part1("day08.txt")
    part2("day08.txt")
