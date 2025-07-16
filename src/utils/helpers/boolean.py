import utils.exceptions as Exps
from utils.helpers.string import is_empty


def check_empty_or_throw_error(value: str, value_name: str):
    if is_empty(value):
        raise Exps.IOException(f"{value_name} is required")


def check_attr_in_dict_or_throw_error(attr_name: str, dict: dict, dict_name: str):
    if f"{attr_name}" not in dict:
        raise Exps.IOException(f"{attr_name} must be in {dict_name}")
