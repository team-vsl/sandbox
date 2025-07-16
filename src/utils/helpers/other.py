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
