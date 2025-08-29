import logging

# Import from utils
from utils.aws_clients import get_bedrock_client
from langchain_aws import ChatBedrock

from genai.quality_to_DQDL import quality_to_DQDL

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def generate_ruleset(params):
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

    llm = ChatBedrock(client=bedrock_client, model_id=model_id)
    response = quality_to_DQDL(user_input, llm)

    return response.content

    messages = response.get("messages")
    data_contract_content = response.get("data_contract")

    return {
        "aiResponse": messages[-1].content,
        "dataContractContent": yaml.dump(data_contract_content),
    }
