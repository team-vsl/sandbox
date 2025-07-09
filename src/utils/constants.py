import os

from dotenv import load_dotenv

load_dotenv()

DEFAULT_PROFILE_NAME = os.getenv("AWS_PROFILE_NAME", None)
DEFAULT_REGION_NAME = os.getenv("AWS_DEFAULT_REGION", None)
DATACONTRACT_DIR = os.getenv("DATACONTRACT_DIR", None)
TEST_DIR = os.getenv("TEST_DIR", None)
TEST_BUCKET_NAME = os.getenv("TEST_BUCKET_NAME", None)
DATACONTRACT_BUCKET_NAME = os.getenv("DATACONTRACT_BUCKET_NAME", None)
