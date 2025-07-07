import os

from dotenv import load_dotenv

load_dotenv()

DEFAULT_PROFILE_NAME = os.getenv("AWS_PROFILE_NAME", None)
DEFAULT_REGION_NAME = os.getenv("AWS_DEFAULT_REGION", None)
DATACONTRACT_DIR = os.getenv("DATACONTRACT_DIR", None)
