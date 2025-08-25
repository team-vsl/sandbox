def is_integer(value):
    """Check if `value` is an integer number or not

    Args:
        value (Any): value to check

    Returns:
        bool: True if `value` is int number, otherwise False
    """

    try:
        value = int(value)

        if isinstance(value, int):
            return True

        return False
    except:
        return False


def is_float(value):
    """Check if `value` is a real number or not

    Args:
        value (Any): value to check

    Returns:
        bool: True if `value` is real number, otherwise False
    """

    try:
        value = float(value)

        if isinstance(value, float):
            return True

        return False
    except:
        return False
