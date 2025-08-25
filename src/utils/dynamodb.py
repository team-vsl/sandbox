from typing import Any, Tuple, Union

import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

# Import utils
import utils.exceptions as Exps
from utils.aws_clients import get_dynamodb_table
from utils.helpers.boolean import (
    is_empty,
    check_none_or_throw_error,
    check_empty_or_throw_error,
    check_attr_in_dict_or_throw_error,
)


class EnumComparisonOperator:
    Equal = "eq"
    NotEqual = "ne"
    LargeThan = "lt"
    LargeThanOrEqual = "lte"
    GreatThan = "gt"
    GreatThanOrEqual = "gte"
    Contains = "contains"
    NotContains = "not_contains"
    BeginsWith = "begins_with"
    Exists = "exists"
    Between = "in"

    @classmethod
    def all(cls) -> set[str]:
        return {
            cls.Equal,
            cls.NotEqual,
            cls.LargeThan,
            cls.LargeThanOrEqual,
            cls.GreatThan,
            cls.GreatThanOrEqual,
            cls.Contains,
            cls.NotContains,
            cls.BeginsWith,
            cls.Exists,
            cls.Between,
        }

    @classmethod
    def validate(cls, op: str):
        if op not in cls.all():
            return False
        return True


class Condition:
    def __init__(self, key: str, operator: str, value: Union[Any, Tuple[Any, Any]]):
        self.key = key
        self.operator = operator
        self.value = value


def build_expression(cond: Condition, use_key: bool = False):
    expr_target = Key(cond.key) if use_key else Attr(cond.key)

    match cond.operator:
        case EnumComparisonOperator.Equal:
            return expr_target.eq(cond.value)
        case EnumComparisonOperator.NotEqual:
            return expr_target.ne(cond.value)
        case EnumComparisonOperator.LargeThan:
            return expr_target.lt(cond.value)
        case EnumComparisonOperator.LargeThanOrEqual:
            return expr_target.lte(cond.value)
        case EnumComparisonOperator.GreatThan:
            return expr_target.gt(cond.value)
        case EnumComparisonOperator.GreatThanOrEqual:
            return expr_target.gte(cond.value)
        case EnumComparisonOperator.Between:
            return expr_target.between(*cond.value)
        case EnumComparisonOperator.BeginsWith:
            return expr_target.begins_with(cond.value)
        case EnumComparisonOperator.Contains:
            return expr_target.contains(cond.value)
        case EnumComparisonOperator.NotContains:
            return expr_target.not_contains(cond.value)
        case _:
            raise Exps.InternalException(f"Unsupported operator: {cond.operator}")


def build_update_expressions(update_data: dict):
    """Build UpdateExpression, ExpressionAttributeValues and ExpressionAttributeNames
    from data of item

    Args:
        update_data (dict): data item to update

    Returns:
        dict: response from Table.update_item
    """
    if not update_data:
        raise Exps.InternalException("Data item is required to update item")

    expression_names = {}
    expression_values = {}
    update_parts = []

    for k, v in update_data.items():
        placeholder_name = f"#{k}"
        placeholder_value = f":{k}"
        expression_names[placeholder_name] = k
        expression_values[placeholder_value] = v
        update_parts.append(f"{placeholder_name} = {placeholder_value}")

    update_expression = "SET " + ", ".join(update_parts)
    return update_expression, expression_values, expression_names


def query_items(**params: Any):
    """Query items in a table with partition key (sort key is optional)

    Args:
        **params: Dictionary of parameters:
            - table_name (str): Name of the DynamoDB table to query. This is required.
            - partition_query (dict, optional): Dictionary specifying the partition key condition. Include:
                - key: name of partition key
                - value: value of partition key
                - op: operator which is used to compare
            - sort_query (dict, optional): Dictionary specifying the sort key condition. Include:
                - key: name of sort key
                - value: value of sort key
                - op: operator which is used to compare
            - limit (int, optional): Maximum number of items to return
            - start_point (dict): Dictionary specifying the start of new query. Include:
                - key: name of start point
                - value: value of start point


    Returns:
        dict: response from Table.query
    """
    table_name = params.get("table_name", "")
    partition_query = params.get("partition_query", None)
    sort_query = params.get("sort_query", None)
    limit = params.get("limit", 10)
    start_point = params.get("start_point", None)

    check_empty_or_throw_error(table_name, "table_name")

    check_none_or_throw_error(
        partition_query,
        "partition_query",
        "partition_query is required to query item",
    )
    check_attr_in_dict_or_throw_error(
        "key",
        partition_query,
        "partition_query",
        "key of partition_query is required to query item",
    )
    check_attr_in_dict_or_throw_error(
        "value",
        partition_query,
        "partition_query",
        "value of partition_query is required to query item",
    )

    if partition_query.get("op", None) is None:
        partition_query["op"] = EnumComparisonOperator.Equal

    if not EnumComparisonOperator.validate(partition_query.get("op")):
        raise Exps.InternalException("Invalid comparison expression in partition query")

    key_condition_exp = build_expression(
        Condition(
            key=partition_query.get("key"),
            value=partition_query.get("value"),
            operator=partition_query.get("op"),
        ),
        use_key=True,
    )

    if sort_query:
        check_attr_in_dict_or_throw_error(
            "key",
            sort_query,
            "sort_query",
            "key of sort_query is required to query item",
        )
        check_attr_in_dict_or_throw_error(
            "value",
            sort_query,
            "sort_query",
            "value of sort_query is required to query item",
        )

        if sort_query.get("op", None) is None:
            sort_query["op"] = EnumComparisonOperator.Equal

        if not EnumComparisonOperator.validate(sort_query.get("op")):
            raise Exps.InternalException("Invalid comparison expression in sort query")

        key_condition_exp = key_condition_exp & build_expression(
            Condition(
                key=sort_query.get("key"),
                value=sort_query.get("value"),
                operator=sort_query.get("op"),
            ),
            use_key=True,
        )

    _params = {"KeyConditionExpression": key_condition_exp}

    if limit is not None:
        _params["Limit"] = limit

    if start_point is not None:
        check_attr_in_dict_or_throw_error(
            "key",
            start_point,
            "start_point",
            "key of start_point is required to query item",
        )
        check_attr_in_dict_or_throw_error(
            "value",
            start_point,
            "start_point",
            "value of start_point is required to query item",
        )

        _params["ExclusiveStartKey"] = {
            start_point.get("key"): start_point.get("value")
        }

    table = get_dynamodb_table(table_name)
    response = table.query(**_params)

    if not response.get("Items"):
        raise Exps.BadRequestException("Items are not found")

    return response.get("Items")


def query_items_with_gsi(**params):
    """Query items in a table with Global Secondary Index

    Args:
        **params: Dictionary of parameters:
            - table_name (str): Name of the DynamoDB table to query. This is required
            - index_name (str, optional): Name of the Global Secondary Index (GSI) to query
            - partition_query (dict, optional): Dictionary specifying the partition key condition. Include:
                - key: name of partition key
                - value: value of partition key
                - op: operator which is used to compare
            - sort_query (dict, optional): Dictionary specifying the sort key condition. Include:
                - key: name of sort key
                - value: value of sort key
                - op: operator which is used to compare
            - limit (int, optional): Maximum number of items to return
            - start_point (dict): Dictionary specifying the start of new query. Include:
                - key: name of start point
                - value: value of start point

    Returns:
        dict: response from Table.query
    """
    table_name = params.get("table_name", "")
    index_name = params.get("index_name", "")
    partition_query = params.get("partition_query", None)
    sort_query = params.get("sort_query", None)
    limit = params.get("limit", None)
    start_point = params.get("start_point", None)

    check_empty_or_throw_error(
        table_name, "table_name", "Table name is required to query item"
    )
    check_empty_or_throw_error(
        index_name, "index_name", "Index name is required to query item with GSI"
    )

    check_none_or_throw_error(
        partition_query, "partition_query", "partition_query is required to query item"
    )
    check_attr_in_dict_or_throw_error(
        "key",
        partition_query,
        "partition_query",
        "key of partition_query is required to query item",
    )
    check_attr_in_dict_or_throw_error(
        "value",
        partition_query,
        "partition_query",
        "value of partition_query is required to query item",
    )

    if partition_query.get("op", None) is None:
        partition_query["op"] = EnumComparisonOperator.Equal

    if not EnumComparisonOperator.validate(partition_query.get("op")):
        raise Exps.InternalException("Invalid comparison expression in partition query")

    key_condition_exp = build_expression(
        Condition(
            key=partition_query.get("key"),
            value=partition_query.get("value"),
            operator=partition_query.get("op"),
        ),
        use_key=True,
    )

    if sort_query:
        check_attr_in_dict_or_throw_error(
            "key",
            sort_query,
            "sort_query",
            "key of sort_query is required to query item",
        )
        check_attr_in_dict_or_throw_error(
            "value",
            sort_query,
            "sort_query",
            "value of sort_query is required to query item",
        )

        if sort_query.get("op", None) is None:
            sort_query["op"] = EnumComparisonOperator.Equal

        if not EnumComparisonOperator.validate(sort_query.get("op")):
            raise Exps.InternalException("Invalid comparison expression in sort query")

        key_condition_exp = key_condition_exp & build_expression(
            Condition(
                key=sort_query.get("key"),
                value=sort_query.get("value"),
                operator=sort_query.get("op"),
            ),
            use_key=True,
        )

    _params = {"IndexName": index_name, "KeyConditionExpression": key_condition_exp}

    if limit is not None:
        _params["Limit"] = limit

    if start_point is not None:
        check_attr_in_dict_or_throw_error(
            "key",
            start_point,
            "start_point",
            "key of start_point is required to query item",
        )
        check_attr_in_dict_or_throw_error(
            "value",
            start_point,
            "start_point",
            "value of start_point is required to query item",
        )

        _params["ExclusiveStartKey"] = {
            start_point.get("key"): start_point.get("value")
        }

    table = get_dynamodb_table(table_name)
    response = table.query(**_params)

    if not response.get("Items"):
        raise Exps.BadRequestException("Items are not found")

    return response.get("Items")


def query_item(**params):
    """Query an item in a table by limit query items by 1

    Args:
        **params: Dictionary of parameters:
            - table_name (str): Name of the DynamoDB table to query. This is required.
            - partition_query (dict, optional): Dictionary specifying the partition key condition. Include:
                - key: name of partition key
                - value: value of partition key
                - op: operator which is used to compare
            - sort_query (dict, optional): Dictionary specifying the sort key condition. Include:
                - key: name of sort key
                - value: value of sort key
                - op: operator which is used to compare
            - limit (int, optional): Maximum number of items to return
            - start_point (dict): Dictionary specifying the start of new query. Include:
                - key: name of start point
                - value: value of start point

    Returns:
        dict: response from Table.query
    """
    return query_items(**params, limit=1)[0]


def query_item_with_gsi(**params):
    """Query an item in a table by limit query items by 1

    Args:
        **params: Dictionary of parameters:
            - table_name (str): Name of the DynamoDB table to query. This is required
            - index_name (str, optional): Name of the Global Secondary Index (GSI) to query
            - partition_query (dict, optional): Dictionary specifying the partition key condition. Include:
                - key: name of partition key
                - value: value of partition key
                - op: operator which is used to compare
            - sort_query (dict, optional): Dictionary specifying the sort key condition. Include:
                - key: name of sort key
                - value: value of sort key
                - op: operator which is used to compare
            - limit (int, optional): Maximum number of items to return
            - start_point (dict): Dictionary specifying the start of new query. Include:
                - key: name of start point
                - value: value of start point

    Returns:
        dict: response from Table.query
    """
    return query_item_with_gsi(**params, limit=1)[0]


def add_item(**params):
    """Add new item to a dynamodb table

    Args:
        **params: Dictionary of parameters:
            - table_name (str): Name of the DynamoDB table to insert the item into. This is required
            - data (dict): Dictionary representing the item to be added. This is required

    Returns:
        dict: response from Table.put_item
    """
    table_name = params.get("table_name", "")
    data = params.get("data", None)

    check_empty_or_throw_error(
        table_name, "table_name", "Table name is required to add new item"
    )

    check_none_or_throw_error(
        data, "item data", "Data of item is required to add new item"
    )

    table = get_dynamodb_table(table_name)
    table.put_item(Item=data)

    return data


def update_item(**params):
    """Update existed item from a dynamodb table

    Args:
        **params: Dictionary of parameters:
            - table_name (str): Name of the DynamoDB table to update the item in. This is required.
            - data (dict): Dictionary of attributes to update in the item. This is required.
            - partition_query (dict): Dictionary with keys:
                - key (str): Name of the partition key.
                - value: Value of the partition key used to locate the item. This is required.
            - sort_query (dict): Dictionary with keys:
                - key (str): Name of the sort key.
                - value: Value of the sort key used to locate the item. This is required.

    Returns:
        dict: new data of item
    """
    table_name = params.get("table_name", "")
    data = params.get("data", None)
    partition_query = params.get("partition_query", None)
    sort_query = params.get("sort_query", None)

    check_empty_or_throw_error(
        table_name, "table_name", "Table name is required to update item"
    )

    check_none_or_throw_error(
        partition_query,
        "partition_query",
        "partition_query is required to update item",
    )
    check_attr_in_dict_or_throw_error(
        "key",
        partition_query,
        "partition_query",
        "key of partition_query is required to update item",
    )
    check_attr_in_dict_or_throw_error(
        "value",
        partition_query,
        "partition_query",
        "value of partition_query is required to update item",
    )

    check_none_or_throw_error(
        sort_query,
        "sort_query",
        "sort_query is required to update item",
    )
    check_attr_in_dict_or_throw_error(
        "key",
        sort_query,
        "sort_query",
        "key of sort_query is required to update item",
    )
    check_attr_in_dict_or_throw_error(
        "value",
        sort_query,
        "sort_query",
        "value of sort_query is required to update item",
    )

    check_none_or_throw_error(
        data, "item data", "Data of item is required to add new item"
    )

    update_expression, expression_values, expression_names = build_update_expressions(
        data
    )

    table = get_dynamodb_table(table_name)
    response = table.update_item(
        Key={
            partition_query.get("key"): partition_query.get("value"),
            sort_query.get("key"): sort_query.get("value"),
        },
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_values,
        ExpressionAttributeNames=expression_names,
        ReturnValues="UPDATED_NEW",
    )

    attrs = response.get("Attributes", {})
    attrs[partition_query.get("key")] = partition_query.get("value")
    attrs[sort_query.get("key")] = sort_query.get("value")

    return attrs


def delete_item(**params):
    """Delete an existed item in a dynamodb table

    Args:
        **params: Dictionary of parameters:
            - table_name (str): Name of the DynamoDB table from which the item will be deleted. This is required
            - partition_query (dict): Dictionary with keys:
                - key (str): Name of the partition key
                - value: Value of the partition key used to locate the item. This is required
            - sort_query (dict): Dictionary with keys:
                - key (str): Name of the sort key
                - value: Value of the sort key used to locate the item. This is required

    Returns:
        bool: return True if item is deleted, otherwise throw error
    """
    table_name = params.get("table_name", "")
    partition_query = params.get("partition_query", None)
    sort_query = params.get("sort_query", None)

    check_empty_or_throw_error(
        table_name, "table_name", "Table name is required to delete item"
    )

    check_none_or_throw_error(
        partition_query,
        "partition_query",
        "partition_query is required to delete item",
    )
    check_attr_in_dict_or_throw_error(
        "key",
        partition_query,
        "partition_query",
        "key of partition_query is required to delete item",
    )
    check_attr_in_dict_or_throw_error(
        "value",
        partition_query,
        "partition_query",
        "value of partition_query is required to delete item",
    )

    check_none_or_throw_error(
        sort_query,
        "sort_query",
        "sort_query is required to delete item",
    )
    check_attr_in_dict_or_throw_error(
        "key",
        sort_query,
        "sort_query",
        "key of sort_query is required to delete item",
    )
    check_attr_in_dict_or_throw_error(
        "value",
        sort_query,
        "sort_query",
        "value of sort_query is required to delete item",
    )

    table = get_dynamodb_table(table_name)
    table.delete_item(
        Key={
            partition_query.get("key"): partition_query.get("value"),
            sort_query.get("key"): sort_query.get("value"),
        }
    )

    return True
