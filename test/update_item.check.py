import asyncio
import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(BASE_DIR, "src"))
sys.path.insert(1, os.path.join(BASE_DIR, "venv"))

from dotenv import load_dotenv

load_dotenv()

from utils.dynamodb import update_item


async def main():
    partition_key = input("Enter partition key: ")
    partition_value = input("Enter partition value: ")
    sort_key = input("Enter sort key: ")
    sort_value = input("Enter sort value: ")
    data_str = input("Enter data by key=value (eg. key=value;key=value): ")
    table_name = "test-table"
    partial_data_str = data_str.split(";")
    data = {}

    for partial in partial_data_str:
        keyvalue = partial.split("=")
        data[keyvalue[0]] = keyvalue[1]

    # Use test table
    response = update_item(
        table_name=table_name,
        partition_query={"key": partition_key, "value": partition_value},
        sort_query={"key": sort_key, "value": sort_value},
        data=data,
    )

    print("Item:", response)

    return


if __name__ == "__main__":
    asyncio.run(main())
