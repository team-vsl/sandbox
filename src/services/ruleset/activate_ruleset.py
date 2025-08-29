# Import built-in libraries
import asyncio
import os
import sys

# Import 3rd-party libraries
import requests

# Import from utils
from utils.constants import (
    RULESET_BUCKET_NAME,
    RULESET_MAPPING_DYNAMODB_TABLE_NAME,
)
from utils.dynamodb import update_item
from utils.rl_state import RulesetState
from utils.s3 import move_file, get_file
from utils.glue import update_inline_ruleset_in_job
from utils.helpers.boolean import check_empty_or_throw_error


async def activate_ruleset(params):
    """
    Activate a inactive ruleset

    Args:
        params (dict): Parameters of this function.

    Returns:
        dict: response from activate_ruleset
    """
    path_params = params.get("path_params")
    query = params.get("query")
    body = params.get("body")
    headers = params.get("headers")
    meta = params.get("meta", {})

    object_name = path_params.get("ruleset_name", "")

    job_name = body.get("jobName", "")
    version = body.get("version", "")
    current_active_ruleset_name = body.get("currentActiveRulesetName", "")
    current_active_ruleset_version = body.get("currentActiveRulesetVersion", "")

    check_empty_or_throw_error(
        version,
        "version",
        "Version of data contract must be specified to update its metadata",
    )
    check_empty_or_throw_error(
        job_name,
        "job_name",
        "Name of job is required to activate ruleset",
    )

    default_ext = "txt"
    old_state = RulesetState.Inactive
    new_state = RulesetState.Active
    source_object_key = f"{old_state}/{object_name}.{default_ext}"
    dest_object_key = f"{new_state}/{object_name}.{default_ext}"

    # Move object from /pending to /approved
    move_file_tasks = [
        asyncio.to_thread(
            move_file,
            bucket_name=RULESET_BUCKET_NAME,
            source_key=source_object_key,
            dest_bucket_name=RULESET_BUCKET_NAME,
            dest_key=dest_object_key,
        ),
    ]

    update_item_tasks = [
        asyncio.to_thread(
            update_item,
            table_name=RULESET_MAPPING_DYNAMODB_TABLE_NAME,
            partition_query={"key": "name", "value": object_name},
            sort_query={"key": "version", "value": version},
            data={"state": new_state, "job_name": job_name},
        )
    ]

    if current_active_ruleset_name:
        check_empty_or_throw_error(
            current_active_ruleset_version,
            "current_active_ruleset_version",
            "Version of current active ruleset is required when name of it is set",
        )

        current_active_rl_state = RulesetState.Active
        current_active_rl_new_state = RulesetState.Inactive
        currect_active_rl_object_key = (
            f"{current_active_rl_state}/{current_active_ruleset_name}.{default_ext}"
        )
        current_active_rl_dest_object_key = (
            f"{current_active_rl_new_state}/{current_active_ruleset_name}.{default_ext}"
        )

        move_file_tasks.append(
            asyncio.to_thread(
                move_file,
                bucket_name=RULESET_BUCKET_NAME,
                source_key=currect_active_rl_object_key,
                dest_bucket_name=RULESET_BUCKET_NAME,
                dest_key=current_active_rl_dest_object_key,
            )
        )

        update_item_tasks.append(
            asyncio.to_thread(
                update_item,
                table_name=RULESET_MAPPING_DYNAMODB_TABLE_NAME,
                partition_query={"key": "name", "value": current_active_ruleset_name},
                sort_query={"key": "version", "value": current_active_ruleset_version},
                data={"state": current_active_rl_new_state, "job_name": ""},
            )
        )

    await asyncio.gather(*move_file_tasks)
    responses = await asyncio.gather(*update_item_tasks)

    print("DEST:", dest_object_key)

    get_file_response = get_file(
        bucket_name=RULESET_BUCKET_NAME, object_key=dest_object_key
    )
    object_content = get_file_response["Body"].read()
    ruleset_content = object_content.decode("utf-8")

    update_inline_ruleset_in_job(job_name=job_name, new_ruleset=ruleset_content)

    return responses[0]
