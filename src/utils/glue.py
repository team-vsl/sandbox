# Import built-in libraries
import json
import uuid

# Import utils
import utils.exceptions as Exps
from utils.aws_clients import get_glue_client
from utils.helpers.other import extract_kwargs
from utils.helpers.boolean import (
    check_empty_or_throw_error,
    check_attr_in_dict_or_throw_error,
)


def start_job(**params):
    """Run a job

    Returns:
        dict: response from start_job_run
    """
    glue_client = get_glue_client()

    job_name, prev_job_run_id, worker_type, number_of_workers = extract_kwargs(
        params, "job_name", "prev_job_run_id", "worker_type", "number_of_workers"
    )

    check_empty_or_throw_error(job_name, "job_name")

    if not worker_type:
        worker_type = "G.1X"

    if not number_of_workers:
        number_of_workers = 2

    response = glue_client.start_job_run(
        JobName=job_name,
        JobRunId=prev_job_run_id,
        WorkerType=worker_type,
        NumberOfWorkers=number_of_workers,
    )

    return response


def get_job(**params):
    """Get job

    Returns:
        dict: response from get_job
    """
    glue_client = get_glue_client()

    job_name, _ = extract_kwargs(params, "job_name")

    response = glue_client.get_job(JobName=job_name)

    return response


def get_running_job(**params):
    """Get job

    Returns:
        dict: response from start_job_run
    """
    glue_client = get_glue_client()

    job_name, job_run_id = extract_kwargs(params, "job_name", "job_run_id")

    response = glue_client.get_job_run(JobName=job_name, RunId=job_run_id)

    return response


def start_data_quality_evaluation(**params):
    """Evaluate data quality

    Returns:
        dict: response from start_data_quality_ruleset_evaluation_run
    """
    glue_client = get_glue_client()

    target_table, role_arn, ruleset_name = extract_kwargs(
        params, "target_table", "role_arn", "ruleset_name"
    )

    check_empty_or_throw_error(target_table, "target_table")
    check_empty_or_throw_error(role_arn, "name")
    check_empty_or_throw_error(ruleset_name, "ruleset_name")

    check_attr_in_dict_or_throw_error("database_name", target_table, "target_table")
    check_attr_in_dict_or_throw_error("table_name", target_table, "target_table")

    response = glue_client.start_data_quality_ruleset_evaluation_run(
        DataSource={
            "GlueTable": {
                "DatabaseName": target_table["database_name"],
                "TableName": target_table["table_name"],
            }
        },
        Role="string",
        ClientToken=str(uuid.uuid4()),
        RulesetNames=[
            "string",
        ],
    )

    return response


def create_ruleset(**params):
    """Create new ruleset

    Returns:
        dict: response from create_data_quality_ruleset
    """
    glue_client = get_glue_client()

    dqdl_rules, name, description, target_table = extract_kwargs(
        params, "dqdl_rules", "name", "description", "target_table"
    )

    check_empty_or_throw_error(name, "name")
    check_empty_or_throw_error(target_table, "target_table")
    check_empty_or_throw_error(dqdl_rules, "dqdl_rules")

    check_attr_in_dict_or_throw_error("Rules", dqdl_rules, "dqdl_rules")
    check_attr_in_dict_or_throw_error("table_name", target_table, "target_table")
    check_attr_in_dict_or_throw_error("database_name", target_table, "target_table")

    response = glue_client.create_data_quality_ruleset(
        Name=name,
        Description=description,
        Ruleset=json.dumps(dqdl_rules),
        TargetTable={
            "TableName": target_table["table_name"],
            "DatabaseName": target_table["database_name"],
        },
        ClientToken=str(uuid.uuid4()),
    )

    return response
