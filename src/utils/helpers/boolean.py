# Import built-in
from typing import TypeGuard, Any

# Import utils
import utils.exceptions as Exps
from utils.helpers.string import is_empty


def check_none_or_throw_error(value: Any, value_name: str, msg: str = ""):
    """Check if a value is None and can throw an error

    Args:
        value (str): value to check
        value_name (str): name of value (or variable name)
        msg (str, optional):

    Returns:
        None: raise error if value is None
    """

    if msg == "":
        msg = f"{value_name} is required"

    if value is None:
        raise Exps.IOException(msg)


def check_empty_or_throw_error(value: str, value_name: str, msg: str = ""):
    """Check if a string is empty or None and can throw an error

    Args:
        value (str): value to check
        value_name (str): name of value (or variable name)
        msg (str, optional):

    Returns:
        None: raise error if value is empty or None
    """

    if msg == "":
        msg = f"{value_name} must be a str and it is required"

    if is_empty(value):
        raise Exps.IOException(msg)


def check_attr_in_dict_or_throw_error(
    attr_name: str, obj: dict, obj_name: str, msg: str = ""
):
    """Check if a attribute is in a dict and can throw an error

    Args:
        attr_name (str): name of wanted attribute
        obj (dict): an object that will be checked
        obj_name (str): name of object (or variable name)
        msg (str, optional): custom error message
    """

    if msg == "":
        msg = f"{attr_name} must be in {obj_name}"

    if attr_name not in obj:
        raise Exps.IOException(msg)
