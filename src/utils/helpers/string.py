def is_empty(s: str | None):
    """Check if a string is None or empty

    Args:
        s (str | None): string to check

    Returns:
        bool: return True if s is None or empty, else False
    """
    return s is None or isinstance(s, str) and s.strip() == ""
