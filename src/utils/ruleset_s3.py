import os
import json
from botocore.exceptions import ClientError
from utils.aws_clients import get_s3_client

RULESET_BUCKET_NAME = os.getenv("RULESET_BUCKET_NAME")
RULESET_PREFIX = "rulesets/"
PENDING_PREFIX = f"{RULESET_PREFIX}pending/"
APPROVED_PREFIX = f"{RULESET_PREFIX}approved/"
REJECTED_PREFIX = f"{RULESET_PREFIX}rejected/"

def list_rulesets(status="pending", **params: dict):
    s3_client = params.get("s3_client") or get_s3_client()
    if status == "approved":
        prefix = APPROVED_PREFIX
    elif status == "rejected":
        prefix = REJECTED_PREFIX
    else:
        prefix = PENDING_PREFIX
    response = s3_client.list_objects_v2(Bucket=RULESET_BUCKET_NAME, Prefix=prefix)
    ruleset_ids = []
    for obj in response.get("Contents", []):
        key = obj["Key"]
        if key.endswith(".json"):
            ruleset_ids.append(os.path.splitext(os.path.basename(key))[0])
    return ruleset_ids

def get_ruleset(ruleset_id, status="pending", **params: dict):
    s3_client = params.get("s3_client") or get_s3_client()
    if status == "approved":
        prefix = APPROVED_PREFIX
    elif status == "rejected":
        prefix = REJECTED_PREFIX
    else:
        prefix = PENDING_PREFIX
    key = f"{prefix}{ruleset_id}.json"
    try:
        response = s3_client.get_object(Bucket=RULESET_BUCKET_NAME, Key=key)
        return response["Body"].read().decode("utf-8")
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey":
            return None
        raise

def upload_ruleset(ruleset_id, content, **params: dict):
    s3_client = params.get("s3_client") or get_s3_client()
    key = f"{PENDING_PREFIX}{ruleset_id}.json"
    if isinstance(content, dict):
        content = json.dumps(content)
    s3_client.put_object(Bucket=RULESET_BUCKET_NAME, Key=key, Body=content, ContentType="application/json")
    return True

def _move_ruleset(ruleset_id, src_prefix, dest_prefix, **params):
    s3_client = params.get("s3_client") or get_s3_client()
    src_key = f"{src_prefix}{ruleset_id}.json"
    dest_key = f"{dest_prefix}{ruleset_id}.json"
    copy_source = {"Bucket": RULESET_BUCKET_NAME, "Key": src_key}
    s3_client.copy_object(Bucket=RULESET_BUCKET_NAME, CopySource=copy_source, Key=dest_key)
    s3_client.delete_object(Bucket=RULESET_BUCKET_NAME, Key=src_key)
    return True

def approve_ruleset(ruleset_id, **params: dict):
    return _move_ruleset(ruleset_id, PENDING_PREFIX, APPROVED_PREFIX, **params)

def reject_ruleset(ruleset_id, **params: dict):
    return _move_ruleset(ruleset_id, PENDING_PREFIX, REJECTED_PREFIX, **params) 