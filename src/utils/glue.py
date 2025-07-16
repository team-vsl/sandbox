# Import built-in libraries
import json
import uuid

# Import utils
import utils.exceptions as Exps
from utils.aws_clients import get_glue_client
from utils.helpers.other import (
    extract_kwargs,
    convert_keys_to_camel_case,
    convert_keys_and_values,
)
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

    sjr_params = {
        "JobName": job_name,
        "WorkerType": worker_type,
        "NumberOfWorkers": number_of_workers,
    }

    if prev_job_run_id:
        sjr_params["JobRunId"] = prev_job_run_id

    response = glue_client.start_job_run(**sjr_params)
    job_run_id = response.get("JobRunId")

    return {"jobRunId": job_run_id}


def get_job(**params):
    """Get job

    Returns:
        dict: response from get_job
    """
    glue_client = get_glue_client()

    job_name = extract_kwargs(params, "job_name")[0]

    response = glue_client.get_job(JobName=job_name)
    job = response.get("Job")

    return convert_keys_to_camel_case(convert_keys_and_values(job))


def get_job_run(**params):
    """Get runned or running job

    Returns:
        dict: response from start_job_run
    """
    glue_client = get_glue_client()

    job_name, job_run_id = extract_kwargs(params, "job_name", "job_run_id")

    check_empty_or_throw_error(job_name, "job_name")
    check_empty_or_throw_error(job_run_id, "job_run_id")

    response = glue_client.get_job_run(JobName=job_name, RunId=job_run_id)
    job_run = response.get("JobRun")

    return convert_keys_to_camel_case(convert_keys_and_values(job_run))


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
    check_empty_or_throw_error(role_arn, "role_arn")
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

    return convert_keys_to_camel_case(convert_keys_and_values(response))


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

    return convert_keys_to_camel_case(convert_keys_and_values(response))


def update_inline_ruleset_in_job(**params):
    """
    Cập nhật nội dung ruleset nội tuyến trong một Glue Job Visual.

    Args:
        job_name (str): Tên Glue Job.
        new_ruleset (str): Nội dung DQDL mới.
        dq_node_name (str): Tên node EvaluateDataQualityMultiFrame (ví dụ: "Evaluate Data Quality").

    Returns:
        dict: Phản hồi từ AWS Glue API.
    """
    glue_client = get_glue_client()

    job_name, new_ruleset, dq_node_name = extract_kwargs(
        params, "job_name", "new_ruleset", "dq_node_name"
    )

    check_empty_or_throw_error(job_name, "job_name")
    check_empty_or_throw_error(new_ruleset, "new_ruleset")

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
        raise ValueError(
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

    return convert_keys_to_camel_case(
        convert_keys_and_values({"jobName": response.get("JobName")})
    )
