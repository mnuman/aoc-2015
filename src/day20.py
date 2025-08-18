from math import sqrt


def divisors(n: int) -> set[int]:
    # determine all numbers properly dividing n
    result = set()
    for i in range(1, int(sqrt(n)) + 1):
        if n % i == 0:
            result.add(i)
            result.add(n // i)
    return result


def presents(housenumber: int) -> int:
    return 10 * sum(d for d in divisors(housenumber))


def limited_presents(housenumber: int) -> int:
    return 11 * sum(d for d in divisors(housenumber) if housenumber // d <= 50)


def part1() -> str:
    n = 33_100_000
    print("====================================================")
    for i in range(1, 1_000_000):
        if presents(i) >= n:
            return f"Solved for {i}, presents(i) = {presents(i)}"
        if i % 500_000 == 0:
            print(i, presents(i))
    return "No solution could be found"


def part2() -> str:
    n = 33_100_000
    print("====================================================")
    for i in range(1, 1_000_000):
        if limited_presents(i) >= n:
            return f"Solved for {i}, limited_presents(i) = {limited_presents(i)}"
        if i % 100_000 == 0:
            print(i, limited_presents(i))
    return "No solution could be found"


if __name__ == "__main__":
    print(part1())
    print(part2())
