import logging

import boto3

from botocore.exceptions import ClientError

# Import from utils
from utils.aws_clients import get_bedrock_client
from dotenv import load_dotenv
from langchain_aws import ChatBedrock

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
from genai.contract_agent import ContractAgent

region_name = "ap-southeast-1"

def generate_draft_datacontract(params):
    path_params, query, body, headers, meta = (
        params.get("path_params"),
        params.get("query"),
        params.get("body"),
        params.get("headers"),
        params.get("meta", {}),
    )

    user_input = body.get("content")

    bedrock_client = get_bedrock_client()
    model_id = "anthropic.claude-3-haiku-20240307-v1:0"

    try:
        llm = ChatBedrock(client=bedrock_client, model_id=model_id)
        graph_agent = ContractAgent(llm_instance=llm)
        response = graph_agent.invoke(user_input)
        print(response)


    except ClientError as err:
        message = err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        print(f"A client error occured: {message}")
