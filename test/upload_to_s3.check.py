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
from utils.constants import TEST_DIR, TEST_BUCKET_NAME
from utils.s3 import upload_file
from utils.aws_clients import get_s3_client

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def main():
    """
    Entrypoint for Anthropic Claude 3 Sonnet example.
    """

    source_dir = TEST_DIR
    file_name = "hello.txt"
    bucket_name = TEST_BUCKET_NAME

    file_path = f"{source_dir}/{file_name}"

    s3_client = get_s3_client()

    try:
        upload_file(s3_client=s3_client, file_name=file_path, bucket_name=bucket_name)

    except Exception as err:
        print(f"A client error occured: {str(err)}")


if __name__ == "__main__":
    main()
