import logging
from datetime import datetime
from pathlib import Path
import os

import boto3

from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_bedrock_client(profile_name: str = "vsl", region_name: str = "ap-southeat-1"):
    # Create a session using the named profile 'vsl'
    session = boto3.Session(profile_name="vsl")

    # Create a Bedrock Runtime client from the session
    bedrock_client = session.client(
        service_name="bedrock-runtime", region_name=region_name
    )  # adjust region as needed
    return


def generate_conversation(bedrock_client, model_id, system_prompts, messages):
    """
    Sends messages to a model.
    Args:
        bedrock_client: The Boto3 Bedrock runtime client.
        model_id (str): The model ID to use.
        system_prompts (JSON) : The system prompts for the model to use.
        messages (JSON) : The messages to send to the model.

    Returns:
        response (JSON): The conversation that the model generated.

    """

    logger.info("Generating message with model %s", model_id)

    # Inference parameters to use.
    temperature = 0.5
    top_k = 200

    # Base inference parameters to use.
    inference_config = {"temperature": temperature}
    # Additional inference parameters to use.
    additional_model_fields = {"top_k": top_k}

    # Send the message.
    response = bedrock_client.converse(
        modelId=model_id,
        messages=messages,
        system=system_prompts,
        inferenceConfig=inference_config,
        additionalModelRequestFields=additional_model_fields,
    )

    # Log token usage.
    token_usage = response["usage"]
    logger.info("Input tokens: %s", token_usage["inputTokens"])
    logger.info("Output tokens: %s", token_usage["outputTokens"])
    logger.info("Total tokens: %s", token_usage["totalTokens"])
    logger.info("Stop reason: %s", response["stopReason"])

    return response
