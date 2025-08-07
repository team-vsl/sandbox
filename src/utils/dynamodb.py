from typing import Any, Tuple, Union

import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

import utils.exceptions as Exps
from utils.aws_clients import get_dynamodb_table
from utils.helpers.boolean import is_empty


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
        params (dict): parameters of this function

    Returns:
        dict: response from Table.query
    """
    table_name: str = params.get("table_name", "")
    partition_query: dict | None = params.get("partition_query", None)
    sort_query: dict | None = params.get("sort_query", None)
    limit: int | None = params.get("limit", None)

    if is_empty(table_name):
        raise Exps.InternalException("Table name is required to query item")

    if partition_query is None:
        raise Exps.InternalException(
            "There is an error in server, partition query are not found."
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
        if sort_query.get("op", None) is None:
            sort_query["op"] = EnumComparisonOperator.Equal

        if not EnumComparisonOperator.validate(sort_query.get("op")):
            raise Exps.InternalException("Invalid comparison expression in sort query")

        if not is_empty(sort_query.get("key")):

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

    table = get_dynamodb_table(table_name)
    response = table.query(**_params)

    if not response.get("Items"):
        raise Exps.BadRequestException("Items are not found")

    return response.get("Items")


def query_items_with_gsi(**params):
    """Query items in a table with Global Secondary Index

    Args:
        params (dict): parameters of this function

    Returns:
        dict: response from Table.query
    """
    table_name: str = params.get("table_name", "")
    index_name: str | None = params.get("index_name")
    partition_query: dict | None = params.get("partition_query", None)
    sort_query: dict | None = params.get("sort_query", None)
    limit: int | None = params.get("limit", None)

    if is_empty(table_name):
        raise Exps.InternalException("Table name is required to query item")

    if is_empty(index_name):
        raise Exps.InternalException("Index name is required to query item with GSI")

    if partition_query is None:
        raise Exps.InternalException(
            "There is an error in server, partition query are not found."
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
        if sort_query.get("op", None) is None:
            sort_query["op"] = EnumComparisonOperator.Equal

        if not EnumComparisonOperator.validate(sort_query.get("op")):
            raise Exps.InternalException("Invalid comparison expression in sort query")

        if not is_empty(sort_query.get("key")):

            key_condition_exp = key_condition_exp & build_expression(
                Condition(
                    key=sort_query.get("key"),
                    value=sort_query.get("value"),
                    operator=sort_query.get("op"),
                ),
                use_key=True,
            )

    _params = {"KeyConditionExpression": key_condition_exp, "IndexName": index_name}

    if limit is not None:
        _params["Limit"] = limit

    table = get_dynamodb_table(table_name)
    response = table.query(**_params)

    if not response.get("Items"):
        raise Exps.BadRequestException("Items are not found")

    return response.get("Items")


def query_item(**params):
    """Query an item in a table by limit query items by 1

    Args:
        params (dict): parameters of this function

    Returns:
        dict: response from Table.query
    """
    return query_items(**params, limit=1)[0]


def add_item(**params):
    table_name: str = params.get("table_name", "")
    data: dict | None = params.get("data", None)

    if is_empty(table_name):
        raise Exps.InternalException("Table name is required to add new item")

    if data is None:
        raise Exps.InternalException("Data of item is not found")

    table = get_dynamodb_table(table_name)
    table.put_item(Item=data)

    return data


def update_item(**params):
    table_name: str = params.get("table_name", "")
    data: dict | None = params.get("data", None)
    partition_query: dict | None = params.get("partition_query", None)
    sort_query: dict | None = params.get("sort_query", None)

    if is_empty(table_name):
        raise Exps.InternalException("Table name is required to add new item")

    if partition_query is None:
        raise Exps.InternalException("Partition query is required to update item")

    if sort_query is None:
        raise Exps.InternalException("Sort query is required to update item")

    if data is None:
        raise Exps.InternalException("Data of item is not found")

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
    table_name: str = params.get("table_name", "")
    partition_query: dict | None = params.get("partition_query", None)
    sort_query: dict | None = params.get("sort_query", None)

    if is_empty(table_name):
        raise Exps.InternalException("Table name is required to add new item")

    if partition_query is None:
        raise Exps.InternalException("Partition query is required to update item")

    if sort_query is None:
        raise Exps.InternalException("Sort query is required to update item")

    table = get_dynamodb_table(table_name)
    table.delete_item(
        Key={
            partition_query.get("key"): partition_query.get("value"),
            sort_query.get("key"): sort_query.get("value"),
        }
    )

    return True
