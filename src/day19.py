from collections import defaultdict
from utils.file_utils import read_file


def parse(fname):
    replacements = defaultdict(list)

    data = read_file(fname)
    while data:
        line = data.pop(0)
        if "=>" in line:
            before, after = line.split("=>")
            replacements[before.strip()].append(after.strip())
        else:
            break
    molecule = data.pop(0).strip()
    return replacements, molecule


def generate_backward_replacements(replacements):
    """Generate backward replacements by swapping left and right sides"""
    backward_replacements = defaultdict(list)
    for before, afters in replacements.items():
        for after in afters:
            backward_replacements[after].append(before)
    return backward_replacements


def part2(reductions, molecule):
    """Find minimum steps to reduce molecule to 'e' using greedy approach"""
    current = molecule
    steps = 0

    # Sort reductions by length (longest first) for greedy approach
    sorted_reductions = []
    for before, afters in reductions.items():
        for after in afters:
            sorted_reductions.append((before, after))
    # Sort by length of the 'before' (what we're replacing) in descending order
    sorted_reductions.sort(key=lambda x: len(x[0]), reverse=True)

    while current != "e":
        found_reduction = False
        for before, after in sorted_reductions:
            if before in current:
                # Apply the first reduction we find
                current = current.replace(before, after, 1)
                steps += 1
                found_reduction = True
                break

        if not found_reduction:
            # If we can't find any reduction, something went wrong
            return -1

    return steps


def part1(replacements, molecule):
    # Generate all possible molecules by applying each replacement once
    generated = set()
    for before, afters in replacements.items():
        start = 0
        while (start := molecule.find(before, start)) != -1:
            for after in afters:
                new_molecule = (
                    molecule[:start] + after + molecule[start + len(before) :]
                )
                generated.add(new_molecule)
            start += 1
    return len(generated)


if __name__ == "__main__":
    replacements, molecule = parse("day19.txt")
    print(f"Replacements: {replacements}")
    print(f"Molecule: {molecule}")
    print(f"Part 1: {part1(replacements, molecule)}")

    # Generate reductions for part 2
    reductions = generate_backward_replacements(replacements)
    # Now, use these reductions (backward replacements) to generate the path from the given molecule to 'e'
    print(f"Part 2: {part2(reductions, molecule)}")
