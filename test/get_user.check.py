import asyncio
import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(BASE_DIR, "src"))
sys.path.insert(1, os.path.join(BASE_DIR, "venv"))

from dotenv import load_dotenv

load_dotenv()

import logging

# Import from services
from utils.cognito import get_user

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main():
    username = input("Enter username: ")

    response = get_user(username=username)

    print("get_user response:", response)


if __name__ == "__main__":
    main()
