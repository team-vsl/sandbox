import asyncio
import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(BASE_DIR, "src"))
sys.path.insert(1, os.path.join(BASE_DIR, "venv"))

from dotenv import load_dotenv

load_dotenv()

from utils.dynamodb import query_items_with_gsi


async def main():
    index_name: str = input("Enter intex name: ")
    partition_key = input("Enter partition key: ")
    partition_value = input("Enter partition value: ")
    sort_key = input("Enter sort key: ")
    sort_value = input("Enter sort value: ")

    response = query_items_with_gsi(
        index_name=index_name,
        partition_query={"key": partition_key, "value": partition_value},
        sort_query={"key": sort_key, "value": sort_value},
    )

    print("Items", response)

    return


if __name__ == "__main__":
    asyncio.run(main())
