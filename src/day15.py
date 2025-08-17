# ruff: noqa: E741
import re
from utils.file_utils import read_file


def parse_input(fname):
    ingredients = {}
    for line in read_file(fname):
        match = re.match(r"(\w+): (.+)", line)
        if match:
            name = match.group(1)
            properties = match.group(2).split(", ")
            ingredients[name] = {}
            for prop in properties:
                key, value = prop.split(" ")
                ingredients[name][key] = int(value)
    return ingredients


def part1(ingredients):
    # Calculate the total score for each ingredient
    all_ingredients = list(ingredients.keys())
    max_score = 0
    for i in range(0, 100):
        for j in range(0, 100 - i):
            for k in range(0, 100 - i - j):
                l = 100 - i - j - k
                cap = sum(
                    ingredients[name]["capacity"] * amount
                    for name, amount in zip(all_ingredients, [i, j, k, l])
                )
                dur = sum(
                    ingredients[name]["durability"] * amount
                    for name, amount in zip(all_ingredients, [i, j, k, l])
                )
                flavor = sum(
                    ingredients[name]["flavor"] * amount
                    for name, amount in zip(all_ingredients, [i, j, k, l])
                )
                texture = sum(
                    ingredients[name]["texture"] * amount
                    for name, amount in zip(all_ingredients, [i, j, k, l])
                )
                if cap > 0 and dur > 0 and flavor > 0 and texture > 0:
                    score = cap * dur * flavor * texture
                    if score > max_score:
                        max_score = score
    return max_score


def part2(ingredients):
    # Calculate the total score for each ingredient
    all_ingredients = list(ingredients.keys())
    max_score = 0
    for i in range(0, 100):
        for j in range(0, 100 - i):
            for k in range(0, 100 - i - j):
                l = 100 - i - j - k
                cap = sum(
                    ingredients[name]["capacity"] * amount
                    for name, amount in zip(all_ingredients, [i, j, k, l])
                )
                dur = sum(
                    ingredients[name]["durability"] * amount
                    for name, amount in zip(all_ingredients, [i, j, k, l])
                )
                flavor = sum(
                    ingredients[name]["flavor"] * amount
                    for name, amount in zip(all_ingredients, [i, j, k, l])
                )
                texture = sum(
                    ingredients[name]["texture"] * amount
                    for name, amount in zip(all_ingredients, [i, j, k, l])
                )
                calories = sum(
                    ingredients[name]["calories"] * amount
                    for name, amount in zip(all_ingredients, [i, j, k, l])
                )
                if (
                    calories == 500
                    and cap > 0
                    and dur > 0
                    and flavor > 0
                    and texture > 0
                ):
                    score = cap * dur * flavor * texture
                    if score > max_score:
                        max_score = score
    return max_score


if __name__ == "__main__":
    ingredients = parse_input("day15.txt")
    print(part1(ingredients))
    print(part2(ingredients))
