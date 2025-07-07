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
from services.data_contract import generate_draft_datacontract

# Import from utils
from utils.constants import DATACONTRACT_DIR
from utils.file import write_to_file

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main():
    """
    Entrypoint for Anthropic Claude 3 Sonnet example.
    """

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    user_input = input("Enter your question: ")

    try:
        result, messages = generate_draft_datacontract(
            {"body": {"content": user_input}}
        )

        # Show the complete conversation.
        for message in messages:
            print(f"Role: {message['role']}")
            for content in message["content"]:
                print(f"Text: {content['text']}")
            print()

        print(
            "Wrote to file: ",
            write_to_file("draft-datacontract", result, DATACONTRACT_DIR),
        )

    except Exception as err:
        print(f"A client error occured: {str(err)}")


if __name__ == "__main__":
    main()
