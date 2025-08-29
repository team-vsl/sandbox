import logging

import yaml

# Import from utils
from utils.aws_clients import get_bedrock_client
from langchain_aws import ChatBedrock

from genai.contract_agent import DataContractAgent

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


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

    llm = ChatBedrock(client=bedrock_client, model_id=model_id)
    graph_agent = DataContractAgent(llm_instance=llm)
    response = graph_agent.invoke(user_input)

    messages = response.get("messages")
    data_contract_content = response.get("data_contract")

    return {
        "aiResponse": messages[-1].content,
        "dataContractContent": yaml.dump(data_contract_content, allow_unicode=True),
    }
