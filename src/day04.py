from hashlib import md5
PREFIX = "iwrupvqb"


def part1():
    suffix = 0
    while True:

        key = f"{PREFIX}{suffix}".encode()
        hash = md5(key).hexdigest()
        if hash.startswith("00000"):
            print(f"Found: {suffix} -> {hash}")
            break
        suffix += 1
        if suffix % 100000 == 0:
            print(f"Checked {suffix} suffixes, last hash: {hash}")


def part2():
    suffix = 346386
    while True:

        key = f"{PREFIX}{suffix}".encode()
        hash = md5(key).hexdigest()
        if hash.startswith("000000"):
            print(f"Found: {suffix} -> {hash}")
            break
        suffix += 1
        if suffix % 100000 == 0:
            print(f"Checked {suffix} suffixes, last hash: {hash}")


if __name__ == "__main__":
    part1()
    part2()
