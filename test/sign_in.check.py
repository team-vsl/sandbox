import asyncio
import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(BASE_DIR, "src"))
sys.path.insert(1, os.path.join(BASE_DIR, "venv"))

from dotenv import load_dotenv

load_dotenv()

# Import from authorize
from authorizer import sign_in


async def main():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    response = await sign_in(username=username, password=password)

    print("Initiate Response:", response)

    return


if __name__ == "__main__":
    asyncio.run(main())
