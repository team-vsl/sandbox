import logging
import os

from botocore.exceptions import ClientError
from botocore.client import BaseClient

# Import helpers
from utils.aws_clients import get_s3_client
from utils.helpers import string as string_helpers
from utils.helpers.boolean import check_empty_or_throw_error

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def upload_fileobj(**params: dict):
    """Upload file-like object to s3 bucket.

    Args:
        **params (dict): Dictionary of parameters. Expected keys:
            - bytes (BytesIO): File-like object to upload. Required.
            - bucket_name (str): Name of the S3 bucket. Required.
            - object_name (str, optional): S3 object name. Defaults to file name.
            - metadata (dict, optional): Metadata to attach to the uploaded file.
            - client (boto3.Client, optional): S3 client instance. Defaults to result of get_s3_client().

    Returns:
        str: Public URL of the uploaded file in the S3 bucket.
    """

    s3_client = params.get("client", get_s3_client())

    file_name = params.get("file_name", "")
    bucket_name = params.get("bucket_name", "")
    object_name = params.get("object_name", "")
    metadata = params.get("metadata", {})

    check_empty_or_throw_error(
        file_name, "file_name", "File name is required to upload file"
    )
    check_empty_or_throw_error(
        bucket_name, "bucket_name", "Bucket name is required to upload file"
    )
    check_empty_or_throw_error(
        object_name, "object_name", "Object name is required to upload file"
    )

    region = s3_client.meta.region_name

    url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{object_name}"
    extra_args = {"Metadata": metadata} if metadata else {}

    s3_client.upload_fileobj(bytes, bucket_name, object_name, ExtraArgs=extra_args)

    return url


def upload_file(**params: dict):
    """Upload file to s3 bucket.

    Args:
        **params (dict): Dictionary of parameters. Expected keys:
            - file_name (str): Path to the file to upload. Required.
            - bucket_name (str): Name of the S3 bucket. Required.
            - object_name (str, optional): S3 object name. Defaults to file name.
            - metadata (dict, optional): Metadata to attach to the uploaded file.
            - client (boto3.Client, optional): S3 client instance. Defaults to result of get_s3_client().

    Returns:
        str: Public URL of the uploaded file in the S3 bucket.
    """

    s3_client = params.get("client", get_s3_client())

    file_name = params.get("file_name", "")
    bucket_name = params.get("bucket_name", "")
    object_name = params.get("object_name", "")
    metadata = params.get("metadata", {})

    check_empty_or_throw_error(
        file_name, "file_name", "File name is required to upload file"
    )
    check_empty_or_throw_error(
        bucket_name, "bucket_name", "Bucket name is required to upload file"
    )

    if object_name is None:
        object_name = os.path.basename(file_name)

    region = s3_client.meta.region_name

    url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{object_name}"
    extra_args = {"Metadata": metadata} if metadata else {}

    s3_client.upload_file(file_name, bucket_name, object_name, ExtraArgs=extra_args)

    return url


def get_file_meta(**params: dict):
    """Get metadata of an object from S3.

    Args:
        **params (dict): Dictionary of parameters. Expected keys:
            - bucket_name (str): Name of the S3 bucket. Required.
            - object_key (str): Key of the object in the bucket. Required.
            - client (boto3.Client, optional): S3 client instance. Defaults to result of get_s3_client().

    Returns:
        dict: Metadata and other response headers returned by S3's head_object API.
    """
    s3_client = params.get("client", get_s3_client())

    bucket_name = params.get("bucket_name", "")
    object_key = params.get("object_key", "")

    check_empty_or_throw_error(
        bucket_name, "bucket_name", "Bucket name is required to get file metadata"
    )
    check_empty_or_throw_error(
        object_key, "object_name", "Object name is required to get file metadata"
    )

    response = s3_client.head_object(Bucket=bucket_name, Key=object_key)

    return response


def get_file(**params: dict):
    """Get content of an object in S3 bucket.

    Args:
        **params (dict): Dictionary of parameters. Expected keys:
            - bucket_name (str): Name of the S3 bucket. Required.
            - object_key (str): Key of the object in the bucket. Required.
            - client (boto3.Client, optional): S3 client instance. Defaults to result of get_s3_client().

    Returns:
        dict: Response from S3 containing the object's content and metadata.
    """
    s3_client = params.get("client", get_s3_client())

    bucket_name = params.get("bucket_name", "")
    object_key = params.get("object_key", "")

    check_empty_or_throw_error(
        bucket_name, "bucket_name", "Bucket name is required to get file"
    )
    check_empty_or_throw_error(
        object_key, "object_name", "Object name is required to get file"
    )

    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)

    return response


def list_files(**params: dict):
    """List all files under a given prefix in an S3 bucket.

    Args:
        **params (dict): Dictionary of parameters. Expected keys:
            - bucket_name (str): Name of the S3 bucket. Required.
            - prefix (str, optional): Prefix to filter objects. Defaults to empty string.
            - client (boto3.Client, optional): S3 client instance. Defaults to result of get_s3_client().

    Returns:
        list: List of objects (dicts) returned by S3 under the specified prefix.
    """
    s3_client = params.get("client", get_s3_client())

    bucket_name = params.get("bucket_name", "")
    prefix = params.get("prefix", "")

    check_empty_or_throw_error(
        bucket_name, "bucket_name", "Bucket name is required to get file metadata"
    )

    paginator = s3_client.get_paginator("list_objects_v2")
    page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

    files = []
    for page in page_iterator:
        contents = page.get("Contents", [])
        files.extend(contents)

    return files


def move_file(**params: dict):
    """Move a file from one prefix to another in S3, optionally updating metadata.

    Args:
        **params (dict): Dictionary of parameters. Expected keys:
            - bucket_name (str): Name of the source S3 bucket. Required.
            - source_key (str): Key of the source object. Required.
            - dest_bucket_name (str): Name of the destination S3 bucket. Required.
            - dest_key (str): Key for the destination object. Required.
            - metadata (dict, optional): New metadata to apply. If provided, replaces existing metadata.
            - client (boto3.Client, optional): S3 client instance. Defaults to result of get_s3_client().

    Returns:
        str: Public URL of the moved file in the destination S3 bucket.
    """
    s3_client = params.get("client", get_s3_client())

    bucket_name = params.get("bucket_name", "")
    source_key = params.get("source_key", "")
    dest_bucket_name = params.get("dest_bucket_name", "")
    dest_key = params.get("dest_key", "")
    new_metadata = params.get("metadata", {})

    check_empty_or_throw_error(
        bucket_name, "bucket_name", "Bucket name is required to move file"
    )
    check_empty_or_throw_error(
        source_key, "source_key", "Source name is required to move file"
    )
    check_empty_or_throw_error(
        dest_bucket_name,
        "dest_bucket_name",
        "Name of destination bucket is required to move file",
    )
    check_empty_or_throw_error(
        dest_key, "dest_key", "Destination key is required to move file"
    )

    dest_key = os.path.join(destination_prefix, os.path.basename(source_key))
    copy_source = {"Bucket": bucket_name, "Key": source_key}

    # Nếu có metadata mới → REPLACE, ngược lại giữ nguyên
    copy_args = {
        "Bucket": bucket_name,
        "CopySource": copy_source,
        "Key": dest_key,
        "MetadataDirective": "COPY",
    }

    if new_metadata:
        copy_args["MetadataDirective"] = "REPLACE"
        copy_args["Metadata"] = new_metadata

    s3_client.copy_object(**copy_args)
    s3_client.delete_object(Bucket=bucket_name, Key=source_key)

    region = s3_client.meta.region_name

    url = f"https://{dest_bucket_name}.s3.{region}.amazonaws.com/{dest_key}"

    return url


def delete_file(**params: dict):
    """Delete a file from S3 bucket.

    Args:
        **params (dict): Dictionary of parameters. Expected keys:
            - bucket_name (str): Name of the S3 bucket. Required.
            - object_key (str): Key of the object to delete. Required.
            - client (boto3.Client, optional): S3 client instance. Defaults to result of get_s3_client().

    Returns:
        bool: True if the deletion request was sent successfully.
    """
    s3_client = params.get("client", get_s3_client())

    bucket_name = params.get("bucket_name", "")
    object_key = params.get("object_key", "")

    check_empty_or_throw_error(
        bucket_name, "bucket_name", "Bucket name is required to get file"
    )
    check_empty_or_throw_error(
        object_key, "object_name", "Object name is required to get file"
    )

    s3_client.delete_object(Bucket=bucket_name, Key=object_key)

    return True
