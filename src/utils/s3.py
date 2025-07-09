import logging
import os

from botocore.exceptions import ClientError
from botocore.client import BaseClient

# Import helpers
from utils.helpers import string as string_helpers

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def upload_file(**params: dict):
    """Upload file to s3 bucket

    Raises:
        Exception: raise exception when it's is None
        Exception: raise file_name when it's None or empty
        Exception: raise bucket_name when it's None or empty

    Returns:
        bool: return True if upload file successfully, otherwise False
    """
    s3_client = params.get("s3_client")
    file_name = params.get("file_name")
    bucket_name = params.get("bucket_name")
    object_name = params.get("object_name")

    if s3_client is None:
        raise Exception("S3 Client is required")

    if string_helpers.is_empty(file_name):
        raise Exception("Name of file is required")

    if string_helpers.is_empty(bucket_name):
        raise Exception("Name of bucket is required")

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    region = s3_client.meta.region_name

    try:
        url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{object_name}"
        response = s3_client.upload_file(file_name, bucket_name, object_name)
        print("URL:", url)
    except ClientError as e:
        logging.error(e)
        return False

    return True
