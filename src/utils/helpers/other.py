import re
from datetime import datetime


def to_camel_case(s):
    for sep in ["-", "_"]:
        s = s.replace(sep, " ")

    parts = s.split()

    if not parts:
        return ""

    return parts[0].lower() + "".join(word.capitalize() for word in parts[1:])


def convert_keys_and_values(obj):
    if isinstance(obj, dict):
        return {to_camel_case(k): convert_keys_and_values(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_keys_and_values(item) for item in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()
    else:
        return obj


def convert_keys_to_camel_case(obj):
    if isinstance(obj, dict):
        return {to_camel_case(k): convert_keys_to_camel_case(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_keys_to_camel_case(item) for item in obj]
    else:
        return obj


def extract_kwargs(kwargs, *keys):
    """Extract all key-value in a kwargs (dict) to a tuple

    Args:
        kwargs (dict): a dict of kwargs

    Returns:
        tuple: result

    Example:
    ```
    def create_person(**kwargs):
        name, age, address = extract_kwargs(kwargs, "name", "age", "address")

        return {
            "name": name,
            "age": age,
            "address": address
        }

    print(create_person(name="Nguyen Anh Tuan", age=23, address="Tam Hiep Ward, Bien Hoa, Dong Nai"))
    ```
    """
    result = []

    for key in keys:
        result.append(kwargs.get(key))

    return tuple(result)
