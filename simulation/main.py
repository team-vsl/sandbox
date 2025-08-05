# Import built-in packages
import json
import sys
import os
from typing import Union

# Import the ./packages to sys path, because we need python recognize
# all of packages inside ./packages
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "packages"))
sys.path.insert(0, os.path.join(BASE_DIR, "..", "src"))


# Import external packages
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Import helper
from handler_executor import execute_handler
from fastapi_response import json_response
from lambda_params import create_lambda_event

# Import middlewares
from middlewares.auth import authorization_dependency

# Import handlers
from runtime.lambda_handlers import (
    list_datacontracts,
    get_datacontract,
    list_rulesets,
    get_ruleset,
    get_datacontract_info,
    sign_in,
    refresh_tokens,
    get_etl_job,
    run_job,
    get_job_run,
    update_inline_ruleset,
)

from utils.roles import Roles

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
    title="VP Bank Challenge #23 API Demo - VSL Team",
    description="Đây là API Demo của Challenge #23 VPBank Hackathon (Smart data contract with genai empowerment)",
    version="0.0.1",
    openapi_tags=tags_metadata,
)
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


@app.get("/")
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
async def handle_sign_in(body: dict):
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
async def handle_refresh_token(body: dict):
    # handler_name = "get_ruleset"

    # response = await execute_handler(
    #     handler_name, create_lambda_event(params={"ruleset_id": ruleset_id}), {}
    # )

    response = await refresh_tokens.handler(create_lambda_event(data=body), {})

    response["body"] = json.loads(response["body"])

    return json_response(response)


@app.get(
    "/data-contracts",
    tags=["Data Contract"],
    dependencies=[authorization_dependency(Roles.Employee)],
)
async def handle_list_datacontracts(state: str):
    # handler_name = "list_datacontracts"

    # response = await execute_handler(
    #     handler_name, create_lambda_event(params={"team_id": team_id}), {}
    # )

    response = await list_datacontracts.handler(
        create_lambda_event(query={"state": state}), {}
    )

    response["body"] = json.loads(response["body"])

    return json_response(response)


@app.get(
    "/data-contracts/{datacontract_name}/info",
    tags=["Data Contract"],
    # dependencies=[authorization_dependency(Roles.Employee)],
)
async def handle_get_datacontract_info(datacontract_name: str, state: str):
    response = await get_datacontract_info.handler(
        create_lambda_event(params={"name": datacontract_name}, query={"state": state}),
        {},
    )

    response["body"] = json.loads(response["body"])

    return json_response(response)


@app.get(
    "/data-contracts/{datacontract_name}",
    tags=["Data Contract"],
    dependencies=[authorization_dependency(Roles.Employee)],
)
async def handle_get_datacontract(datacontract_name: str, state: str):
    # handler_name = "get_datacontract"

    # response = await execute_handler(
    #     handler_name,
    #     create_lambda_event(params={"name": datacontract_name}),
    #     {},
    # )

    response = get_datacontract.get_datacontract(
        {"path_params": {"name": datacontract_name}, "query": {"state": state}}
    )

    return StreamingResponse(response)


@app.get(
    "/rulesets",
    tags=["Ruleset"],
    dependencies=[authorization_dependency(Roles.Employee)],
)
async def handle_list_rulesets(team_id: str, q: Union[str, None] = None):
    # handler_name = "list_rulesets"

    # response = await execute_handler(
    #     handler_name, create_lambda_event(params={"team_id": team_id}), {}
    # )

    response = await list_rulesets.handler(
        create_lambda_event(params={"team_id": team_id}), {}
    )

    response["body"] = json.loads(response["body"])

    return json_response(response)


@app.get(
    "/rulesets/{ruleset_id}",
    tags=["Ruleset"],
    dependencies=[authorization_dependency(Roles.Employee)],
)
async def handle_get_ruleset(ruleset_id: str, q: Union[str, None] = None):
    # handler_name = "get_ruleset"

    # response = await execute_handler(
    #     handler_name, create_lambda_event(params={"ruleset_id": ruleset_id}), {}
    # )

    response = await get_ruleset.handler(
        create_lambda_event(params={"ruleset_id": ruleset_id}), {}
    )

    response["body"] = json.loads(response["body"])

    return json_response(response)


@app.get(
    "/glue-jobs/{job_name}",
    tags=["Glue ETL Job"],
)
async def handle_get_glue_job(job_name: str):
    # handler_name = "get_ruleset"

    # response = await execute_handler(
    #     handler_name, create_lambda_event(params={"ruleset_id": ruleset_id}), {}
    # )

    response = await get_etl_job.handler(
        create_lambda_event(params={"job_name": job_name}), {}
    )

    response["body"] = json.loads(response["body"])

    return json_response(response)


@app.post(
    "/glue-jobs/{job_name}",
    tags=["Glue ETL Job"],
)
async def handle_start_run_glue_job(job_name: str, body: dict | None = None):
    # handler_name = "get_ruleset"

    # response = await execute_handler(
    #     handler_name, create_lambda_event(params={"ruleset_id": ruleset_id}), {}
    # )

    response = await run_job.handler(
        create_lambda_event(params={"job_name": job_name}, data=body), {}
    )

    response["body"] = json.loads(response["body"])

    return json_response(response)


@app.patch(
    "/glue-jobs/{job_name}",
    tags=["Glue ETL Job"],
)
async def handle_update_inline_ruleset_in_job(job_name: str, body: dict):
    # handler_name = "get_ruleset"

    # response = await execute_handler(
    #     handler_name, create_lambda_event(params={"ruleset_id": ruleset_id}), {}
    # )

    response = await update_inline_ruleset.handler(
        create_lambda_event(params={"job_name": job_name}, data=body), {}
    )

    response["body"] = json.loads(response["body"])

    return json_response(response)


@app.get(
    "/glue-jobs/{job_name}/run-status/{job_run_id}",
    tags=["Glue ETL Job"],
)
async def handle_get_job_run(job_name: str, job_run_id: str):
    # handler_name = "get_ruleset"

    # response = await execute_handler(
    #     handler_name, create_lambda_event(params={"ruleset_id": ruleset_id}), {}
    # )

    response = await get_job_run.handler(
        create_lambda_event(params={"job_name": job_name, "job_run_id": job_run_id}),
        {},
    )

    response["body"] = json.loads(response["body"])

    return json_response(response)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
