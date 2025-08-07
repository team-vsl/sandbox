import logging

import boto3

# Import from utils
from utils.constants import DEFAULT_REGION_NAME, DEFAULT_PROFILE_NAME

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

if DEFAULT_REGION_NAME is None:
    raise Exception("Default region is required. Please setup .env first")

if DEFAULT_PROFILE_NAME is None:
    DEFAULT_PROFILE_NAME = ""


def get_client(
    service_name: str,
    profile_name: str = DEFAULT_PROFILE_NAME,
    region_name: str = DEFAULT_REGION_NAME,
):
    # Create a session using the named profile 'vsl'
    session = boto3.Session(profile_name=profile_name)

    # Create a Service client from the session
    client = session.client(service_name=service_name, region_name=region_name)
    return client


def get_resource(
    service_name: str,
    profile_name: str = DEFAULT_PROFILE_NAME,
    region_name: str = DEFAULT_REGION_NAME,
):
    # Create a session using the named profile 'vsl'
    session = boto3.Session(profile_name=profile_name)

    # Create a service resource
    resource = session.resource(service_name, region_name=region_name)
    return resource


def get_bedrock_client():
    return get_client("bedrock-runtime")


def get_s3_client():
    return get_client("s3")


def get_cognito_client():
    return get_client("cognito-idp")


def get_glue_client():
    return get_client("glue")


def get_dynamodb_client():
    return get_client("dynamodb")


def get_dynamodb_table(table_name: str):
    resource = get_resource("dynamodb")
    table = resource.Table(table_name)
    return table
