# Import built-in packages
import sys
import os
from typing import Union

# Import the ./packages to sys path, because we need python recognize
# all of packages inside ./packages
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "packages"))
sys.path.insert(0, os.path.join(BASE_DIR, "..", "src"))


# Import external packages
from fastapi import FastAPI
from dotenv import load_dotenv

# Import helper
from handler_executor import execute_handler
from fastapi_response import json_response
from lambda_params import create_lambda_event

params = {""}
load_dotenv()

app = FastAPI()
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))


@app.get("/")
def read_root():
    return {
        "message": "Hello World !!! This is a lambda simulation of VP Bank Hackathon Challenge 23 from VSL Team"
    }


@app.get("/teams/{team_id}/data-contracts")
async def list_datacontracts(team_id: str, q: Union[str, None] = None):
    handler_name = "list_datacontracts"

    response = await execute_handler(
        handler_name, create_lambda_event(params={"team_id": team_id}), {}
    )

    return json_response(response)


@app.get("/data-contracts/{datacontract_id}")
async def get_datacontract(datacontract_id: str, q: Union[str, None] = None):
    handler_name = "get_datacontract"

    response = await execute_handler(
        handler_name,
        create_lambda_event(params={"datacontract_id": datacontract_id}),
        {},
    )

    return json_response(response)


@app.get("/teams/{team_id}/rulesets")
async def list_rulesets(team_id: str, q: Union[str, None] = None):
    handler_name = "list_rulesets"

    response = await execute_handler(
        handler_name, create_lambda_event(params={"team_id": team_id}), {}
    )

    return json_response(response)


@app.get("/rulesets/{ruleset_id}")
async def get_ruleset(ruleset_id: str, q: Union[str, None] = None):
    handler_name = "get_ruleset"

    response = await execute_handler(
        handler_name, create_lambda_event(params={"ruleset_id": ruleset_id}), {}
    )

    return json_response(response)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
