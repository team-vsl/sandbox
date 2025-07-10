import os

from dotenv import load_dotenv

load_dotenv()

PROJECT_NAME = os.getenv("PROJECT_NAME", None)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", None)
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", None)
DEFAULT_PROFILE_NAME = os.getenv("AWS_PROFILE_NAME", None)
DEFAULT_REGION_NAME = os.getenv("AWS_DEFAULT_REGION", None)
DATACONTRACT_DIR = os.getenv("DATACONTRACT_DIR", None)
TEST_DIR = os.getenv("TEST_DIR", None)
TEST_BUCKET_NAME = os.getenv("TEST_BUCKET_NAME", None)
DATACONTRACT_BUCKET_NAME = os.getenv("DATACONTRACT_BUCKET_NAME", None)
