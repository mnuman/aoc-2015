import re
import json
from utils.file_utils import read_raw_file

PATTERN = re.compile(r"-?\d+")


def sum_numbers(s: str) -> int:
    """
    Sum all numbers in the given string.
    """
    return sum(int(match) for match in PATTERN.findall(s))


def remove_red_objects(data):
    """
    Recursively remove objects that contain the value "red" in any property.
    Returns the filtered data structure.
    """
    if isinstance(data, dict):
        # Check if any value in this dict is "red"
        if "red" in data.values():
            return {}  # Return empty dict (effectively removing this object)
        # Recursively process all values in the dict
        return {key: remove_red_objects(value) for key, value in data.items()}
    elif isinstance(data, list):
        # Recursively process all items in the list
        return [remove_red_objects(item) for item in data]
    else:
        # For primitive values (strings, numbers, etc.), return as-is
        return data


def sum_numbers_excluding_red(data) -> int:
    """
    Sum all numbers in the JSON data, excluding objects that contain "red".
    """
    # Remove objects with "red" values
    filtered_data = remove_red_objects(data)
    # Convert back to string and sum numbers
    return sum_numbers(json.dumps(filtered_data))


if __name__ == "__main__":
    input_data = read_raw_file("day12.txt")
    result = sum_numbers(input_data)
    print(f"Sum of all numbers in the input: {result}")

    # Parse JSON and remove red objects
    json_data = json.loads(input_data)
    result_no_red = sum_numbers_excluding_red(json_data)
    print(f"Sum excluding objects with 'red': {result_no_red}")
