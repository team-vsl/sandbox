import re
from datetime import datetime


def to_camel_case(s: str) -> str:
    if not s:
        return ""

    # Bước 1: Thay thế _ và - thành khoảng trắng
    s = re.sub(r"[_\-]+", " ", s)

    # Bước 2: Tách PascalCase hoặc camelCase (textAText → text A Text)
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", s)
    s = re.sub(r"([A-Z])([A-Z][a-z])", r"\1 \2", s)

    # Bước 3: Tách và chuẩn hóa
    parts = s.strip().split()
    if not parts:
        return ""

    return parts[0].lower() + "".join(p.capitalize() for p in parts[1:])


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
        return {to_camel_case(k): convert_keys_and_values(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_keys_and_values(item) for item in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()
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
