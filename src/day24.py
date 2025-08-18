from utils.file_utils import read_file
from itertools import combinations
from math import prod


def parse(fname):
    return [int(line) for line in read_file(fname)]


def find_valid_3_partitions(weights):
    """Find all valid 3-partitions where each partition has equal sum"""
    total_weight = sum(weights)

    # For a valid 3-partition, each group must have weight = total_weight // 3
    if total_weight % 3 != 0:
        return []

    target_weight = total_weight // 3
    n = len(weights)
    valid_partitions = []

    # Generate all possible combinations for the first group
    for size1 in range(1, n - 1):  # First group size
        for group1 in combinations(weights, size1):
            if sum(group1) == target_weight:
                remaining_weights = [w for w in weights if w not in group1]

                # Generate all possible combinations for the second group from remaining weights
                for size2 in range(1, len(remaining_weights)):
                    for group2 in combinations(remaining_weights, size2):
                        if sum(group2) == target_weight:
                            group3 = tuple(
                                w for w in remaining_weights if w not in group2
                            )

                            # Check if the third group also has the target weight
                            if sum(group3) == target_weight:
                                # Sort groups to ensure uniqueness
                                partition = tuple(
                                    sorted(
                                        [
                                            tuple(sorted(group1)),
                                            tuple(sorted(group2)),
                                            tuple(sorted(group3)),
                                        ]
                                    )
                                )

                                if partition not in valid_partitions:
                                    valid_partitions.append(partition)

    return valid_partitions


def find_minimal_first_group(weights):
    """Find the smallest first group that allows for a valid 3-partition"""
    total_weight = sum(weights)

    if total_weight % 3 != 0:
        return None

    target_weight = total_weight // 3

    # Try smallest groups first (by number of packages)
    for size in range(1, len(weights) - 1):
        for group1 in combinations(weights, size):
            if sum(group1) == target_weight:
                remaining_weights = [w for w in weights if w not in group1]

                # Check if remaining weights can be split into two equal groups
                if can_split_into_two_equal_groups(remaining_weights, target_weight):
                    return group1

    return None


def can_split_into_two_equal_groups(weights, target_weight):
    """Check if weights can be split into two groups with target_weight each"""
    n = len(weights)

    for size in range(1, n):
        for group in combinations(weights, size):
            if sum(group) == target_weight:
                remaining = [w for w in weights if w not in group]
                if sum(remaining) == target_weight:
                    return True

    return False


#############################################
# Optimized minimal 3-partition first group #
#############################################


def subset_sum_possible(values: list[int], target: int) -> bool:
    """Bitset subset-sum test: can some subset sum to target?"""
    bits = 1  # bit 0 set
    for v in values:
        bits |= bits << v
        # optional pruning: keep only up to target bits
        if bits.bit_length() > target + 1:
            bits &= (1 << (target + 1)) - 1
    return (bits >> target) & 1 == 1


def best_first_group_min_qe(weights: list[int]) -> tuple[int, ...] | None:
    """Find the smallest-size first group with sum target and minimal QE that
    allows a 3-way partition (groups of equal sum). Returns the group as a sorted tuple.
    """
    total = sum(weights)
    if total % 3 != 0:
        return None
    target = total // 3

    # Work with indices to avoid ambiguity with duplicate weights
    vals = sorted(weights, reverse=True)
    n = len(vals)

    # Try increasing group sizes
    for size in range(1, n + 1):
        candidates = []  # list of (QE, indices tuple)
        for idxs in combinations(range(n), size):
            s = sum(vals[i] for i in idxs)
            if s == target:
                qe = prod(vals[i] for i in idxs)
                candidates.append((qe, idxs))
        if not candidates:
            continue
        # Sort by quantum entanglement
        candidates.sort()

        # Check feasibility for remaining items using subset-sum
        for _, idxs in candidates:
            remaining = [vals[i] for i in range(n) if i not in idxs]
            # Remaining must split into two groups of 'target': it's enough to
            # check that some subset sums to target (then the rest is target too)
            if sum(remaining) != 2 * target:
                continue
            if subset_sum_possible(remaining, target):
                return tuple(sorted(vals[i] for i in idxs))
        # If no candidate of this size works, try next size
    return None


def best_first_group_min_qe_groups(
    weights: list[int], groups: int
) -> tuple[int, ...] | None:
    """Generalized version for `groups` equal-sum partitions (e.g., 4 for Part 2).
    Returns the minimal-size first group with minimal QE as a sorted tuple, or None.
    """
    total = sum(weights)
    if total % groups != 0:
        return None
    target = total // groups

    vals = sorted(weights, reverse=True)
    n = len(vals)

    # Helper: recursively check if remaining indices can be partitioned into k groups
    def can_partition_k_groups(idx_set: set[int], k: int) -> bool:
        if k == 0:
            return len(idx_set) == 0
        if sum(vals[i] for i in idx_set) != k * target:
            return False
        # Quick prune with subset-sum
        if not subset_sum_possible([vals[i] for i in idx_set], target):
            return False

        # Find one subset summing to target via DFS, then recurse
        avail = sorted(idx_set, key=lambda i: vals[i], reverse=True)
        picked: list[int] = []

        def dfs(start: int, s: int) -> list[int] | None:
            if s == target:
                return list(picked)
            if s > target:
                return None
            # optimistic bound
            rem_sum = 0
            for j in range(start, len(avail)):
                rem_sum += vals[avail[j]]
            if s + rem_sum < target:
                return None
            last_v = None
            for j in range(start, len(avail)):
                i = avail[j]
                v = vals[i]
                if last_v is not None and v == last_v:
                    continue
                last_v = v
                picked.append(i)
                res = dfs(j + 1, s + v)
                if res is not None:
                    return res
                picked.pop()
            return None

        subset = dfs(0, 0)
        if subset is None:
            return False
        rest = set(idx_set) - set(subset)
        return can_partition_k_groups(rest, k - 1)

    # Try increasing first-group sizes; within size, try ascending QE
    for size in range(1, n + 1):
        candidates = []
        for idxs in combinations(range(n), size):
            s = sum(vals[i] for i in idxs)
            if s == target:
                candidates.append((prod(vals[i] for i in idxs), idxs))
        if not candidates:
            continue
        candidates.sort()
        for _, idxs in candidates:
            remaining = set(range(n)) - set(idxs)
            # Need to partition remaining into (groups-1) groups
            if can_partition_k_groups(remaining, groups - 1):
                return tuple(sorted(vals[i] for i in idxs))
    return None


if __name__ == "__main__":
    weights = parse("day24.txt")
    total = sum(weights)
    print(f"Total weight: {total}")

    # Part 1: 3 groups
    if total % 3 != 0:
        print("Part 1: Not divisible by 3; no 3-way partition possible.")
    else:
        target = total // 3
        print(f"Part 1 target per group: {target}")
        best1 = best_first_group_min_qe_groups(weights, groups=3)
        if best1 is None:
            print("Part 1: No valid 3-way partition found.")
        else:
            print(f"Part 1 best first group: {best1}")
            print(f"Size={len(best1)}, QE={prod(best1)}, sum={sum(best1)}")

    # Part 2: 4 groups
    if total % 4 != 0:
        print("Part 2: Not divisible by 4; no 4-way partition possible.")
    else:
        target2 = total // 4
        print(f"Part 2 target per group: {target2}")
        best2 = best_first_group_min_qe_groups(weights, groups=4)
        if best2 is None:
            print("Part 2: No valid 4-way partition found.")
        else:
            print(f"Part 2 best first group: {best2}")
            print(f"Size={len(best2)}, QE={prod(best2)}, sum={sum(best2)}")
