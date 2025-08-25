# Import built-in packages
import json
import sys
import os
from typing import Union, Annotated

# Import the ./packages to sys path, because we need python recognize
# all of packages inside ./packages
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "packages"))
sys.path.insert(0, os.path.join(BASE_DIR, "..", "src"))


# Import external packages
from fastapi import FastAPI, HTTPException, Request, Body, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Import helper
from handler_executor import execute_handler
from fastapi_response import json_response
from lambda_params import create_lambda_event, add_claims_to_request_ctx
from openapi_config import create_custom_openapi_schema

# Import middlewares
from middlewares.auth import authorization_dependency

# Import handlers
from runtime.lambda_handlers import (
    generate_draft_datacontract,
    list_datacontracts,
    get_datacontract,
    get_datacontract_info,
    approve_draft_datacontract,
    reject_draft_datacontract,
    upload_draft_datacontract,
    generate_ruleset,
    list_rulesets,
    get_ruleset_info,
    activate_ruleset,
    inactivate_ruleset,
    upload_ruleset,
    sign_in,
    refresh_tokens,
    list_etl_jobs,
    list_etl_job_runs,
    get_etl_job,
    run_etl_job,
    get_job_run,
    update_inline_ruleset,
)

# Import services
from services.data_contract import get_datacontract
from services.ruleset import get_ruleset

# Import utils
from utils.roles import Roles
from utils.dc_state import DataContractState

load_dotenv()

tags_metadata = [
    {
        "name": "Data Contract",
        "description": "Các thao tác với data contract",
    },
    {
        "name": "Ruleset",
        "description": "Các thao tác liên quan tới ruleset",
    },
    {
        "name": "Glue ETL Job",
        "description": "Các thao tác liên quan tới Glue ETL Job",
    },
    {
        "name": "Auth",
        "description": "Các thao tác liên quan tới xác thực & uỷ quyền",
    },
]

app = FastAPI(
    openapi_tags=tags_metadata,
)
app.openapi = lambda: create_custom_openapi_schema(app)
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT", "8000"))

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    print("Exc:", exc)

    # Nếu detail là dict
    if isinstance(exc.detail, dict):
        return JSONResponse(
            status_code=exc.status_code, content=exc.detail, headers=exc.headers
        )

    # Nếu detail chỉ là string, wrap lại theo format chuẩn
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": str(exc.detail),
                "title": "Error",
                "code": "ERROR",
                "details": None,
            },
            "data": None,
            "meta": None,
        },
        headers=exc.headers,
    )


@app.get("/", tags=["Hello World"])
def read_root():
    return json_response(
        {
            "body": {
                "message": "Hello World !!! This is a lambda simulation of VP Bank Hackathon Challenge 23 from VSL Team."
            },
            "statusCode": 200,
        }
    )


@app.post(
    "/auth/sign-in",
    tags=["Auth"],
)
async def handle_sign_in(
    body: Annotated[dict, Body(example={"username": "string", "password": "string"})],
):
    # handler_name = "get_ruleset"

    # response = await execute_handler(
    #     handler_name, create_lambda_event(params={"ruleset_id": ruleset_id}), {}
    # )

    response = await sign_in.handler(create_lambda_event(data=body), {})

    response["body"] = json.loads(response["body"])

    return json_response(response)


@app.post(
    "/auth/refresh-tokens",
    tags=["Auth"],
)
async def handle_refresh_token(
    body: Annotated[dict, Body(example={"refreshToken": "string"})],
):
    # handler_name = "get_ruleset"

    # response = await execute_handler(
    #     handler_name, create_lambda_event(params={"ruleset_id": ruleset_id}), {}
    # )

    response = await refresh_tokens.handler(create_lambda_event(data=body), {})

    response["body"] = json.loads(response["body"])

    return json_response(response)


@app.post(
    "/data-contract",
    tags=["Data Contract"],
)
async def handle_generate_draft_datacontract(
    body: Annotated[dict, Body(example={"content": "string"})],
    claims: dict = authorization_dependency(Roles.Employee),
):
    # handler_name = "list_datacontracts"

    # response = await execute_handler(
    #     handler_name, create_lambda_event(params={"team_id": team_id}), {}
    # )

    response = await generate_draft_datacontract.handler(
        create_lambda_event(
            data=body, request_context=add_claims_to_request_ctx({}, claims)
        ),
        {},
    )

    response["body"] = json.loads(response["body"])

    return json_response(response)


@app.post(
    "/data-contract/upload",
    tags=["Data Contract"],
)
async def handle_upload_draft_datacontract(
    body: Annotated[dict, Body(example={"content": "yaml_string"})],
    claims: dict = authorization_dependency(Roles.Employee),
):
    # handler_name = "list_datacontracts"

    # response = await execute_handler(
    #     handler_name, create_lambda_event(params={"team_id": team_id}), {}
    # )

    response = await upload_draft_datacontract.handler(
        create_lambda_event(
            data=body, request_context=add_claims_to_request_ctx({}, claims)
        ),
        {},
    )

    response["body"] = json.loads(response["body"])

    return json_response(response)


@app.get(
    "/data-contracts",
    tags=["Data Contract"],
    # dependencies=[authorization_dependency(Roles.Employee)],
)
async def handle_list_datacontracts(
    state: str,
    limit: str = "10",
    startKey: str = "",
    claims: dict = authorization_dependency(Roles.Employee),
):
    # handler_name = "list_datacontracts"

    # response = await execute_handler(
    #     handler_name, create_lambda_event(params={"team_id": team_id}), {}
    # )

    response = await list_datacontracts.handler(
        create_lambda_event(
            query={"limit": limit, "start_key": startKey, "state": state},
            request_context=add_claims_to_request_ctx({}, claims),
        ),
        {},
    )

    response["body"] = json.loads(response["body"])

    return json_response(response)


@app.get(
    "/data-contracts/{datacontract_name}/info",
    tags=["Data Contract"],
    # dependencies=[authorization_dependency(Roles.Employee)],
)
async def handle_get_datacontract_info(
    datacontract_name: str, claims: dict = authorization_dependency(Roles.Employee)
):
    response = await get_datacontract_info.handler(
        create_lambda_event(
            params={"name": datacontract_name},
            request_context=add_claims_to_request_ctx({}, claims),
        ),
        {},
    )

    response["body"] = json.loads(response["body"])

    return json_response(response)


@app.get(
    "/data-contracts/{datacontract_name}",
    tags=["Data Contract"],
    # dependencies=[authorization_dependency(Roles.Employee)],
)
async def handle_get_datacontract(
    datacontract_name: str,
    state: str,
    claims: dict = authorization_dependency(Roles.Employee),
):
    # handler_name = "get_datacontract"

    # response = await execute_handler(
    #     handler_name,
    #     create_lambda_event(params={"name": datacontract_name}),
    #     {},
    # )

    response = get_datacontract(
        {
            "path_params": {"name": datacontract_name},
            "query": {"state": state},
            "meta": {"claims": claims},
        }
    )

    return StreamingResponse(response)


@app.post(
    "/data-contracts/{datacontract_name}/approval",
    tags=["Data Contract"],
    # dependencies=[authorization_dependency(Roles.Employee)],
)
async def handle_approve_datacontract(
    datacontract_name: str,
    body: Annotated[dict, Body(example={"version": "string"})],
    claims: dict = authorization_dependency(Roles.Employee),
):
    # handler_name = "get_datacontract"

    # response = await execute_handler(
    #     handler_name,
    #     create_lambda_event(params={"name": datacontract_name}),
    #     {},
    # )

    response = await approve_draft_datacontract.handler(
        create_lambda_event(
            params={"datacontract_name": datacontract_name},
            data=body,
            request_context=add_claims_to_request_ctx({}, claims),
        ),
        {},
    )

    response["body"] = json.loads(response["body"])

    return json_response(response)


@app.post(
    "/data-contracts/{datacontract_name}/rejection",
    tags=["Data Contract"],
    # dependencies=[authorization_dependency(Roles.Employee)],
)
async def handle_reject_datacontract(
    datacontract_name: str,
    body: Annotated[dict, Body(example={"version": "string"})],
    claims: dict = authorization_dependency(Roles.Employee),
):
    # handler_name = "get_datacontract"

    # response = await execute_handler(
    #     handler_name,
    #     create_lambda_event(params={"name": datacontract_name}),
    #     {},
    # )

    response = await reject_draft_datacontract.handler(
        create_lambda_event(
            params={"datacontract_name": datacontract_name},
            data=body,
            request_context=add_claims_to_request_ctx({}, claims),
        ),
        {},
    )

    response["body"] = json.loads(response["body"])

    return json_response(response)


@app.post(
    "/ruleset",
    tags=["Ruleset"],
)
async def handle_generate_ruleset(
    body: dict, claims: dict = authorization_dependency(Roles.Employee)
):
    # handler_name = "list_datacontracts"

    # response = await execute_handler(
    #     handler_name, create_lambda_event(params={"team_id": team_id}), {}
    # )

    response = await generate_ruleset.handler(
        create_lambda_event(
            data=body, request_context=add_claims_to_request_ctx({}, claims)
        ),
        {},
    )

    response["body"] = json.loads(response["body"])

    return json_response(response)


@app.post(
    "/ruleset/upload",
    tags=["Ruleset"],
)
async def handle_upload_ruleset(
    body: Annotated[
        dict, Body(example={"content": "string", "name": "string", "version": "string"})
    ],
    claims: dict = authorization_dependency(Roles.Employee),
):
    # handler_name = "list_datacontracts"

    # response = await execute_handler(
    #     handler_name, create_lambda_event(params={"team_id": team_id}), {}
    # )

    response = upload_ruleset.handler(
        create_lambda_event(
            data=body, request_context=add_claims_to_request_ctx({}, claims)
        ),
        {},
    )

    response["body"] = json.loads(response["body"])

    return json_response(response)


@app.get(
    "/rulesets",
    tags=["Ruleset"],
    # dependencies=[authorization_dependency(Roles.Employee)],
)
async def handle_list_rulesets(
    state: str,
    limit: str = "10",
    startKey: str = "",
    claims: dict = authorization_dependency(Roles.Employee),
):
    # handler_name = "list_rulesets"

    # response = await execute_handler(
    #     handler_name, create_lambda_event(params={"team_id": team_id}), {}
    # )

    response = list_rulesets.handler(
        create_lambda_event(
            query={"limit": limit, "start_key": startKey, "state": state},
            request_context=add_claims_to_request_ctx({}, claims),
        ),
        {},
    )

    response["body"] = json.loads(response["body"])

    return json_response(response)


@app.get(
    "/rulesets/{ruleset_name}/info",
    tags=["Ruleset"],
    # dependencies=[authorization_dependency(Roles.Employee)],
)
async def handle_get_ruleset_info(
    ruleset_name: str,
    claims: dict = authorization_dependency(Roles.Employee),
):
    # handler_name = "get_ruleset"

    # response = await execute_handler(
    #     handler_name, create_lambda_event(params={"ruleset_id": ruleset_id}), {}
    # )

    response = await get_ruleset_info.handler(
        create_lambda_event(
            params={"name": ruleset_name},
            request_context=add_claims_to_request_ctx({}, claims),
        ),
        {},
    )

    response["body"] = json.loads(response["body"])

    return json_response(response)


@app.get(
    "/rulesets/{ruleset_name}",
    tags=["Ruleset"],
    # dependencies=[authorization_dependency(Roles.Employee)],
)
async def handle_get_ruleset(
    ruleset_name: str,
    state: str,
    claims: dict = authorization_dependency(Roles.Employee),
):
    # handler_name = "get_datacontract"

    # response = await execute_handler(
    #     handler_name,
    #     create_lambda_event(params={"name": datacontract_name}),
    #     {},
    # )

    response = get_ruleset(
        {
            "path_params": {"name": ruleset_name},
            "query": {"state": state},
            "meta": {"claims": claims},
        }
    )

    return StreamingResponse(response)


@app.post(
    "/rulesets/{ruleset_name}/activation",
    tags=["Ruleset"],
    # dependencies=[authorization_dependency(Roles.Employee)],
)
async def handle_activate_ruleset(
    ruleset_name: str,
    body: Annotated[
        dict,
        Body(
            example={
                "jobName": "string",
                "version": "string",
                "currentActiveRulesetName": "string",
                "currentActiveRulesetVersion": "string",
            }
        ),
    ],
    claims: dict = authorization_dependency(Roles.Employee),
):
    # handler_name = "get_datacontract"

    # response = await execute_handler(
    #     handler_name,
    #     create_lambda_event(params={"name": datacontract_name}),
    #     {},
    # )

    response = await activate_ruleset.handler(
        create_lambda_event(
            params={"ruleset_name": ruleset_name},
            data=body,
            request_context=add_claims_to_request_ctx({}, claims),
        ),
        {},
    )

    response["body"] = json.loads(response["body"])

    return json_response(response)


@app.post(
    "/rulesets/{ruleset_name}/inactivation",
    tags=["Ruleset"],
    # dependencies=[authorization_dependency(Roles.Employee)],
)
async def handle_inactivate_ruleset(
    ruleset_name: str,
    body: Annotated[dict, Body(example={"version": "string"})],
    claims: dict = authorization_dependency(Roles.Employee),
):
    # handler_name = "get_datacontract"

    # response = await execute_handler(
    #     handler_name,
    #     create_lambda_event(params={"name": datacontract_name}),
    #     {},
    # )

    response = inactivate_ruleset.handler(
        create_lambda_event(
            params={"ruleset_name": ruleset_name},
            data=body,
            request_context=add_claims_to_request_ctx({}, claims),
        ),
        {},
    )

    response["body"] = json.loads(response["body"])

    return json_response(response)


@app.get("/glue-jobs", tags=["Glue ETL Job"])
async def handle_list_jobs(
    limit: str = "10",
    next_token: str | None = None,
    claims: dict = authorization_dependency(Roles.Employee),
):
    response = await list_etl_jobs.handler(
        create_lambda_event(
            query={"limit": limit, "next_token": next_token},
            request_context=add_claims_to_request_ctx({}, claims),
        ),
        {},
    )

    response["body"] = json.loads(response["body"])

    return json_response(response)


@app.get(
    "/glue-jobs/{job_name}",
    tags=["Glue ETL Job"],
)
async def handle_get_glue_job(
    job_name: str, claims: dict = authorization_dependency(Roles.Employee)
):
    # handler_name = "get_ruleset"

    # response = await execute_handler(
    #     handler_name, create_lambda_event(params={"ruleset_id": ruleset_id}), {}
    # )

    response = await get_etl_job.handler(
        create_lambda_event(
            params={"job_name": job_name},
            request_context=add_claims_to_request_ctx({}, claims),
        ),
        {},
    )

    response["body"] = json.loads(response["body"])

    return json_response(response)


@app.post(
    "/glue-jobs/{job_name}",
    tags=["Glue ETL Job"],
)
async def handle_start_run_glue_job(
    job_name: str,
    body: dict | None = None,
    claims: dict = authorization_dependency(Roles.Employee),
):
    # handler_name = "get_ruleset"

    # response = await execute_handler(
    #     handler_name, create_lambda_event(params={"ruleset_id": ruleset_id}), {}
    # )

    response = run_etl_job.handler(
        create_lambda_event(
            params={"job_name": job_name},
            data=body,
            request_context=add_claims_to_request_ctx({}, claims),
        ),
        {},
    )

    response["body"] = json.loads(response["body"])

    return json_response(response)


@app.patch(
    "/glue-jobs/{job_name}",
    tags=["Glue ETL Job"],
)
async def handle_update_inline_ruleset_in_job(
    job_name: str,
    body: Annotated[dict, Body(example={"content": "string"})],
    claims: dict = authorization_dependency(Roles.Employee),
):
    # handler_name = "get_ruleset"

    # response = await execute_handler(
    #     handler_name, create_lambda_event(params={"ruleset_id": ruleset_id}), {}
    # )

    response = update_inline_ruleset.handler(
        create_lambda_event(
            params={"job_name": job_name},
            data=body,
            request_context=add_claims_to_request_ctx({}, claims),
        ),
        {},
    )

    response["body"] = json.loads(response["body"])

    return json_response(response)


@app.get("/glue-jobs/{job_name}/run-status", tags=["Glue ETL Job"])
async def handle_get_job_runs(
    job_name: str,
    limit: str = "10",
    next_token: str | None = None,
    claims: dict = authorization_dependency(Roles.Employee),
):
    response = await list_etl_job_runs.handler(
        create_lambda_event(
            params={"job_name": job_name},
            query={"limit": limit, "next_token": next_token},
            request_context=add_claims_to_request_ctx({}, claims),
        ),
        {},
    )

    response["body"] = json.loads(response["body"])

    return json_response(response)


@app.get(
    "/glue-jobs/{job_name}/run-status/{job_run_id}",
    tags=["Glue ETL Job"],
)
async def handle_get_job_run(
    job_name: str,
    job_run_id: str,
    claims: dict = authorization_dependency(Roles.Employee),
):
    # handler_name = "get_ruleset"

    # response = await execute_handler(
    #     handler_name, create_lambda_event(params={"ruleset_id": ruleset_id}), {}
    # )

    response = await get_job_run.handler(
        create_lambda_event(
            params={"job_name": job_name, "job_run_id": job_run_id},
            request_context=add_claims_to_request_ctx({}, claims),
        ),
        {},
    )

    response["body"] = json.loads(response["body"])

    return json_response(response)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
