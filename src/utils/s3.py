import logging
import os

from botocore.exceptions import ClientError
from botocore.client import BaseClient

# Import helpers
from utils.helpers import string as string_helpers

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def upload_file(**params: dict):
    """Upload file to s3 bucket"""
    s3_client = params.get("s3_client")
    file_name = params.get("file_name")
    bucket_name = params.get("bucket_name")
    object_name = params.get("object_name")
    metadata = params.get("metadata", {})

    if s3_client is None:
        raise Exception("S3 Client is required")

    if string_helpers.is_empty(file_name):
        raise Exception("Name of file is required")

    if string_helpers.is_empty(bucket_name):
        raise Exception("Name of bucket is required")

    if object_name is None:
        object_name = os.path.basename(file_name)

    region = s3_client.meta.region_name

    try:
        url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{object_name}"
        extra_args = {"Metadata": metadata} if metadata else {}
        s3_client.upload_file(file_name, bucket_name, object_name, ExtraArgs=extra_args)
        print("URL:", url)
    except ClientError as e:
        logging.error(e)
        return False

    return True


def list_files(**params: dict):
    """List all files under a given prefix in an S3 bucket"""
    s3_client = params.get("s3_client")
    bucket_name = params.get("bucket_name")
    prefix = params.get("prefix", "")

    if s3_client is None:
        raise Exception("S3 Client is required")

    if string_helpers.is_empty(bucket_name):
        raise Exception("Name of bucket is required")

    try:
        paginator = s3_client.get_paginator("list_objects_v2")
        page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

        files = []
        for page in page_iterator:
            contents = page.get("Contents", [])
            files.extend([obj["Key"] for obj in contents])

        return files
    except ClientError as e:
        logging.error(e)
        return []


def move_file(**params: dict):
    """Move a file from one prefix to another, optionally updating metadata"""
    s3_client = params.get("s3_client")
    bucket_name = params.get("bucket_name")
    source_key = params.get("source_key")
    destination_prefix = params.get("destination_prefix")
    new_metadata = params.get("metadata", {})

    if s3_client is None:
        raise Exception("S3 Client is required")

    if string_helpers.is_empty(bucket_name):
        raise Exception("Name of bucket is required")

    if string_helpers.is_empty(source_key):
        raise Exception("Source key is required")

    if string_helpers.is_empty(destination_prefix):
        raise Exception("Destination prefix is required")

    dest_key = os.path.join(destination_prefix, os.path.basename(source_key))
    copy_source = {"Bucket": bucket_name, "Key": source_key}

    try:
        # Nếu có metadata mới → REPLACE, ngược lại giữ nguyên
        copy_args = {
            "Bucket": bucket_name,
            "CopySource": copy_source,
            "Key": dest_key,
            "MetadataDirective": "COPY"
        }

        if new_metadata:
            copy_args["MetadataDirective"] = "REPLACE"
            copy_args["Metadata"] = new_metadata

        s3_client.copy_object(**copy_args)
        s3_client.delete_object(Bucket=bucket_name, Key=source_key)
        logger.info(f"[✓] Moved: {source_key} → {dest_key}")
        return True
    except ClientError as e:
        logging.error(e)
        return False

def delete_file(**params: dict):
    """Delete a file from S3 bucket"""
    s3_client = params.get("s3_client")
    bucket_name = params.get("bucket_name")
    object_key = params.get("object_key")

    if s3_client is None:
        raise Exception("S3 Client is required")

    if string_helpers.is_empty(bucket_name):
        raise Exception("Name of bucket is required")

    if string_helpers.is_empty(object_key):
        raise Exception("Object key is required")

    try:
        s3_client.delete_object(Bucket=bucket_name, Key=object_key)
        logger.info(f"[✓] Deleted: {object_key}")
        return True
    except ClientError as e:
        logging.error(e)
        return False
