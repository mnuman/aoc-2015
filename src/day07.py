from utils.file_utils import read_file
from typing import Dict


def parse(fname: str) -> Dict[str, str]:
    """Parse instructions into a dictionary mapping wire -> instruction"""
    instructions = {}
    for line in read_file(fname):
        parts = line.split(" -> ")
        source = parts[0]
        target = parts[1]
        instructions[target] = source
    return instructions


def evaluate_wire(
    wire: str, instructions: Dict[str, str], cache: Dict[str, int]
) -> int:
    """Recursively evaluate a wire's signal value with memoization"""

    # If already computed, return cached value
    if wire in cache:
        return cache[wire]

    # If it's a number, return it directly
    if wire.isdigit():
        value = int(wire)
        cache[wire] = value
        return value

    # Get the instruction for this wire
    if wire not in instructions:
        raise ValueError(f"No instruction found for wire {wire}")

    instruction = instructions[wire]
    parts = instruction.split()

    if len(parts) == 1:
        # Direct assignment: "123" or "x"
        value = evaluate_wire(parts[0], instructions, cache)
    elif len(parts) == 2:
        # NOT operation: "NOT x"
        if parts[0] == "NOT":
            value = (~evaluate_wire(parts[1], instructions, cache)) & 0xFFFF
        else:
            raise ValueError(f"Unknown single operator: {parts[0]}")
    elif len(parts) == 3:
        # Binary operations: "x AND y", "x OR y", "x LSHIFT 2", "y RSHIFT 2"
        left = evaluate_wire(parts[0], instructions, cache)
        operator = parts[1]
        right = evaluate_wire(parts[2], instructions, cache)

        if operator == "AND":
            value = left & right
        elif operator == "OR":
            value = left | right
        elif operator == "LSHIFT":
            value = (left << right) & 0xFFFF
        elif operator == "RSHIFT":
            value = (left >> right) & 0xFFFF
        else:
            raise ValueError(f"Unknown operator: {operator}")
    else:
        raise ValueError(f"Invalid instruction format: {instruction}")

    # Ensure 16-bit range
    value = value & 0xFFFF
    cache[wire] = value
    return value


def solve_part1(fname: str) -> int:
    """Solve part 1: find signal on wire 'a'"""
    instructions = parse(fname)
    cache = {}
    return evaluate_wire("a", instructions, cache)


def solve_part2(fname: str) -> int:
    """Solve part 2: override wire 'b' with part 1 result, then find new 'a'"""
    instructions = parse(fname)

    # First, get the original value of wire 'a'
    cache = {}
    original_a = evaluate_wire("a", instructions, cache)

    # Override wire 'b' with the original 'a' value
    instructions["b"] = str(original_a)

    # Clear cache and compute new 'a'
    cache = {}
    return evaluate_wire("a", instructions, cache)


if __name__ == "__main__":
    # Test with example
    print("Testing with example:")
    test_instructions = parse("test_day07.txt")
    test_cache = {}

    expected = {
        "d": 72,
        "e": 507,
        "f": 492,
        "g": 114,
        "h": 65412,
        "i": 65079,
        "x": 123,
        "y": 456,
    }

    print("Expected vs Actual:")
    for wire, expected_value in expected.items():
        actual = evaluate_wire(wire, test_instructions, test_cache)
        print(
            f"{wire}: {expected_value} vs {actual} {'✓' if expected_value == actual else '✗'}"
        )

    print("\nSolving actual puzzle:")
    part1_result = solve_part1("day07.txt")
    print(f"Part 1 - Signal on wire 'a': {part1_result}")

    part2_result = solve_part2("day07.txt")
    print(f"Part 2 - Signal on wire 'a' after override: {part2_result}")
