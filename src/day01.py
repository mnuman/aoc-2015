from pathlib import Path


def do_floor(s: str) -> int:
    """Calculate Santa's final floor based on the input string.

    ( means Santa goes up a floor, ) means Santa goes down a floor.
    We're starting on floor 0, there is no minimum nor maximum floor.
    """
    floor = 0
    for char in s:
        if char == "(":
            floor += 1
        elif char == ")":
            floor -= 1
    return floor


def basement(s: str) -> int:
    """Find the position of the first character that causes Santa to enter the basement."""
    floor = 0
    for i, char in enumerate(s):
        if char == "(":
            floor += 1
        elif char == ")":
            floor -= 1
        if floor < 0:
            return i + 1  # Return position (1-indexed)
    return -1  # If never enters basement


def main():
    """Read input and print the final floor."""
    with Path("./data/day01.txt").open("r") as file:
        data = file.read().strip()
    final_floor = do_floor(data)
    print(f"Santa ends up on floor: {final_floor}")
    print(f"First basement entry at position: {basement(data)}")


if __name__ == "__main__":
    main()
