import asyncio
import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(BASE_DIR, "src"))
sys.path.insert(1, os.path.join(BASE_DIR, "venv"))

from dotenv import load_dotenv

load_dotenv()

# Import from authorize
from authorizer import verify_token


def main():
    access_token = input("Enter you access token: ")
    response = verify_token(access_token)

    print("Verify token response:", response)

    return


if __name__ == "__main__":
    main()
