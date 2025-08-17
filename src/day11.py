import re

PASSWORD_CHARS = "abcdefghjkmnpqrstuvwxyz"
PATTERN = re.compile(r"(.)\1.*(.)\2")


def three_increasing_letters(s: str) -> bool:
    """
    Check if the string contains three consecutive increasing letters.
    """
    for i in range(len(s) - 2):
        if ord(s[i]) + 1 == ord(s[i + 1]) and ord(s[i]) + 2 == ord(s[i + 2]):
            return True
    return False


def two_non_overlapping_pairs(s: str) -> bool:
    """
    Check if the string contains two non-overlapping pairs of letters.
    """
    return len(PATTERN.findall(s)) >= 1


def no_invalid_characters(s: str) -> bool:
    """
    Check if the string contains any invalid characters.
    """
    return all(c in PASSWORD_CHARS for c in s)


def is_valid_password(s: str) -> bool:
    """
    Check if the password is valid according to the given criteria.
    """
    return (
        no_invalid_characters(s)
        and three_increasing_letters(s)
        and two_non_overlapping_pairs(s)
    )


def increment_password(s: str) -> str:
    """
    Increment the password by treating it like a base-26 number.
    """
    s = list(s)
    i = len(s) - 1
    while i >= 0:
        if s[i] == "z":
            s[i] = "a"
            i -= 1
        else:
            s[i] = chr(ord(s[i]) + 1)
            break
    return "".join(s).replace("i", "j").replace("o", "p").replace("l", "m")


def find_next_password(s: str) -> str:
    """
    Find the next valid password.
    """
    s = increment_password(s)
    iteration = 0
    while not is_valid_password(s):
        iteration += 1
        if iteration % 5000 == 0:
            print(f"Iteration - {iteration} - password: {s}")
        s = increment_password(s)
    return s


if __name__ == "__main__":
    input_data = "cqjxjnds"
    next_password = find_next_password(input_data)
    print(f"Next valid password after '{input_data}': {next_password}")
    print(f"Is '{next_password}' a valid password? {is_valid_password(next_password)}")
    input_data = next_password
    next_password = find_next_password(input_data)
    print(f"Next valid password after '{input_data}': {next_password}")
    print(f"Is '{next_password}' a valid password? {is_valid_password(next_password)}")
