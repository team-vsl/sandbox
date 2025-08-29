# Import built-in libraries
import json
import uuid

# Import utils
import utils.exceptions as Exps
from utils.aws_clients import get_glue_client
from utils.helpers.other import (
    extract_kwargs,
    convert_keys_to_camel_case,
)
from utils.helpers.boolean import (
    check_empty_or_throw_error,
    check_attr_in_dict_or_throw_error,
)


def start_job(**params):
    """Run a job (create a job run)

    Args:
        **params: Dictionary of optional parameters:
            - client (boto3.client, optional): AWS Glue client instance. If not provided, a default client will be created
            - job_name (str): Name of the AWS Glue job to run. This is required
            - prev_job_run_id (str, optional): ID of a previous job run to resume or reference
            - worker_type (str, optional): Type of worker to use for the job. Default is "G.1X"
            - number_of_workers (int, optional): Number of workers to allocate. Default is 2

    Returns:
        dict: id of new job run
    """
    glue_client = params.get("client", get_glue_client())

    job_name = params.get("job_name", "")
    prev_job_run_id = params.get("prev_job_run_id", "")
    worker_type = params.get("worker_type", "G.1X")
    number_of_workers = params.get("number_of_workers", 2)

    check_empty_or_throw_error(job_name, "job_name")

    # Prepare params for start_job_run
    _params = {
        "JobName": job_name,
        "WorkerType": worker_type,
        "NumberOfWorkers": number_of_workers,
    }

    if prev_job_run_id:
        _params["JobRunId"] = prev_job_run_id

    response = glue_client.start_job_run(**_params)
    job_run_id = response.get("JobRunId")

    return job_run_id


def list_jobs(**params):
    """List available jobs on Amazon Glue

    Args:
        **params: Dictionary of optional parameters:
            - client (boto3.client, optional): AWS Glue client instance. If not provided, a default client will be created
            - next_token (str, optional): Token for paginated results. Used to retrieve the next set of jobs
            - limit (int, optional): Maximum number of jobs to return. Default is 5

    Returns:
        dict: modified response from get_jobs
    """

    glue_client = params.get("client", get_glue_client())

    next_token = params.get("next_token", None)
    limit = params.get("limit", 10)

    # Prepare params for get_jobs
    _params = {"MaxResults": limit}

    if next_token is not None:
        _params["NextToken"] = next_token

    response = glue_client.get_jobs(**_params)
    jobs = response.get("Jobs", [])

    return {
        "jobs": convert_keys_to_camel_case(jobs),
        "meta": {"next_token": response.get("NextToken")},
    }


def get_job(**params):
    """Get job

    Args:
        **params: Dictionary of parameters:
            - client (boto3.client, optional): AWS Glue client instance. If not provided, a default client will be created
            - job_name (str): Name of the AWS Glue job to retrieve. This is required

    Returns:
        dict: Job from response from get_job
    """
    glue_client = params.get("client", get_glue_client())

    job_name = params.get("job_name", "")

    check_empty_or_throw_error(job_name, "job_name")

    response = glue_client.get_job(JobName=job_name)
    job = response.get("Job")

    return convert_keys_to_camel_case(job)


def list_job_runs(**params):
    """List available job runs of a job on Amazon Glue

    Args:
        **params: Dictionary of parameters:
            - client (boto3.client, optional): AWS Glue client instance. If not provided, a default client will be created
            - job_name (str): Name of the AWS Glue job whose runs are to be listed. This is required
            - next_token (str, optional): Token for paginated results. Used to retrieve the next set of job runs
            - limit (int, optional): Maximum number of job runs to return. Default is 5

    Returns:
        dict: modified response from get_job_runs
    """
    glue_client = params.get("client", get_glue_client())

    next_token = params.get("next_token", None)
    limit = params.get("limit", 10)
    job_name = params.get("job_name", "")

    check_empty_or_throw_error(job_name, "job_name")

    _params = {"MaxResults": limit}

    if next_token is not None:
        _params["NextToken"] = next_token

    response = glue_client.get_job_runs(JobName=job_name, **_params)
    job_runs = response.get("JobRuns")

    return {
        "job_runs": convert_keys_to_camel_case(job_runs),
        "meta": {"next_token": response.get("NextToken")},
    }


def get_job_run(**params):
    """Get runned or running job

    Args:
        **params: Dictionary of parameters:
            - client (boto3.client, optional): AWS Glue client instance. If not provided, a default client will be created
            - job_name (str): Name of the AWS Glue job. This is required
            - job_run_id (str): ID of the specific job run to retrieve. This is required

    Returns:
        dict: JobRun from response from start_job_run
    """
    glue_client = params.get("client", get_glue_client())

    job_name = params.get("job_name", "")
    job_run_id = params.get("job_run_id", "")

    check_empty_or_throw_error(job_name, "job_name")
    check_empty_or_throw_error(job_run_id, "job_run_id")

    response = glue_client.get_job_run(JobName=job_name, RunId=job_run_id)
    job_run = response.get("JobRun")

    return convert_keys_to_camel_case(job_run)


def start_data_quality_evaluation(**params):
    """Evaluate data quality

    Args:
        **params: Dictionary of parameters:
            - client (boto3.client, optional): AWS Glue client instance. If not provided, a default client will be created
            - target_table (dict): Dictionary containing table metadata. Must include:
                - database_name (str): Name of the database
                - table_name (str): Name of the table
            - role_arn (str): ARN of the IAM role used to run the evaluation. This is required
            - ruleset_name (str): Name of the data quality ruleset to evaluate. This is required

    Returns:
        dict: response from start_data_quality_ruleset_evaluation_run
    """
    glue_client = params.get("client", get_glue_client())

    target_table = params.get("target_table", "")
    role_arn = params.get("role_arn", "")
    ruleset_name = params.get("ruleset_name", "")

    check_empty_or_throw_error(target_table, "target_table")
    check_empty_or_throw_error(role_arn, "role_arn")
    check_empty_or_throw_error(ruleset_name, "ruleset_name")

    check_attr_in_dict_or_throw_error("database_name", target_table, "target_table")
    check_attr_in_dict_or_throw_error("table_name", target_table, "target_table")

    response = glue_client.start_data_quality_ruleset_evaluation_run(
        DataSource={
            "GlueTable": {
                "DatabaseName": target_table.get("database_name"),
                "TableName": target_table.get("table_name"),
            }
        },
        Role="string",
        ClientToken=str(uuid.uuid4()),
        RulesetNames=[
            "string",
        ],
    )

    return convert_keys_to_camel_case(response)


def create_ruleset(**params):
    """Create new ruleset

    Args:
        **params: Dictionary of parameters:
            - client (boto3.client, optional): AWS Glue client instance. If not provided, a default client will be created
            - name (str): Name of the data quality ruleset to create. This is required
            - description (str, optional): Description of the ruleset
            - dqdl_rules (dict): Dictionary containing DQDL rules. Must include:
                - Rules (list): List of rule definitions in DQDL format
            - target_table (dict): Dictionary specifying the target table. Must include:
                - database_name (str): Name of the database
                - table_name (str): Name of the table

    Returns:
        dict: response from create_data_quality_ruleset
    """
    glue_client = params.get("client", get_glue_client())

    name = params.get("name", "")
    description = params.get("description", "")
    dqdl_rules = params.get("dqdl_rules", {})
    target_table = params.get("target_table", {})

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

    return convert_keys_to_camel_case(response)


def update_inline_ruleset_in_job(**params):
    """Update a ruleset of a job (standard job)

    Args:
        **params: Dictionary of parameters:
            - client (boto3.client, optional): AWS Glue client instance. If not provided, a default client will be created.
            - job_name (str): Name of the AWS Glue job to update. This is required.
            - new_ruleset (str): New DQDL ruleset content to apply. This is required.
            - dq_node_name (str, optional): Name of the DataQuality node within the job. Default is "Evaluate Data Quality".

    Returns:
        dict: name of job
    """
    glue_client = params.get("client", get_glue_client())

    job_name = params.get("job_name", "")
    new_ruleset = params.get("new_ruleset", "")
    dq_node_name = params.get("dq_node_name", "")

    check_empty_or_throw_error(job_name, "job_name")

    if not dq_node_name:
        dq_node_name = "Evaluate Data Quality"

    # Lấy định nghĩa job hiện tại
    response = glue_client.get_job(JobName=job_name)
    job = response.get("Job")
    nodes = job.get("CodeGenConfigurationNodes", {})

    # Tìm node EvaluateDataQualityMultiFrame theo tên
    dq_node_id = None
    for node_id, node_def in nodes.items():
        edq = node_def.get("EvaluateDataQualityMultiFrame")
        if edq and edq.get("Name") == dq_node_name:
            dq_node_id = node_id
            break

    if not dq_node_id:
        raise Exps.NotFoundException(
            f"Cannot find EvaluateDataQualityMultiFrame with the name '{dq_node_name}' in job '{job_name}'"
        )

    # Cập nhật ruleset
    nodes[dq_node_id]["EvaluateDataQualityMultiFrame"]["Ruleset"] = new_ruleset

    job_update = {
        "Role": job.get("Role"),
        "Command": job.get("Command"),
        "DefaultArguments": job.get("DefaultArguments", {}),
        "Connections": job.get("Connections", {}),
        "MaxRetries": job.get("MaxRetries", 0),
        "GlueVersion": job.get("GlueVersion", "5.0"),
        "NumberOfWorkers": job.get("NumberOfWorkers", 2),
        "WorkerType": job.get("WorkerType", "G.1X"),
        "ExecutionProperty": job.get("ExecutionProperty", {}),
        "ExecutionClass": job.get("ExecutionClass", "STANDARD"),
        "JobMode": job.get("JobMode", "VISUAL"),
        "CodeGenConfigurationNodes": nodes,
    }

    # Gọi UpdateJob để cập nhật
    response = glue_client.update_job(JobName=job_name, JobUpdate=job_update)

    return response.get("JobName", "")
