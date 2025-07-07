import logging

import boto3

from botocore.exceptions import ClientError

# Import from utils
from utils.bedrock import generate_conversation, get_bedrock_client

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

system_prompt_content = """
You are a system responsible for generating ISO-aligned data contracts based on user input. A data contract defines the structure, semantics, quality, and terms of data exchange between a data provider and consumer. You must generate a valid YAML document conforming to the Data Contract Specification v1.2.0. The result must be platform-agnostic, precise, and aligned with common data governance standards (similar to OpenAPI and AsyncAPI).

Generate a `datacontract.yaml` file with the following sections:
- `dataContractSpecification`: must be set to "1.2.0"
- `id`: unique contract ID in slug format
- `info`: include title, description, version, status, owner, contact (name + email or URL)
- `servers`: define data location, environment, and access format (e.g. AWS S3, BigQuery, Snowflake, etc.)
- `terms`: usage terms, limitations, policies (privacy, licensing), billing, notice period
- `models`: tables or data structures, their fields (name, type, description, constraints), quality checks, primary keys, foreign key references
- `definitions`: reusable definitions of fields (e.g., order_id, SKU)
- `servicelevels`: retention, availability, latency, freshness, frequency, support, recovery
- `tags` and `links`: optional metadata and documentation references

Ensure:
- YAML format is clean and indented properly
- Field types follow specification types (e.g. text, timestamp, long)
- Quality sections contain validation logic using SQL where needed
- Sensitive fields (e.g., emails) are marked with `pii: true` and `classification: sensitive`
- Use ISO 8601 for timestamps (e.g., `2025-07-07T20:32:00Z`)
- Add at least one sample `model` with `examples` of data rows

Respond with the complete `datacontract.yaml` file only. Do not include explanations or commentary."""

region_name = "ap-southeast-1"


def generate_draft_datacontract(user_input: str):
    bedrock_client = get_bedrock_client()
    model_id = "anthropic.claude-3-haiku-20240307-v1:0"

    try:
        system_prompts = [{"text": system_prompt_content}]
        message = {
            "role": "user",
            "content": [{"text": user_input}],
        }
        messages = [message]

        response = generate_conversation(
            bedrock_client=bedrock_client,
            model_id=model_id,
            system_prompts=system_prompts,
            messages=messages,
        )
        output_message = response["output"]["message"]
        messages.append(output_message)

        return output_message["content"][0]["text"], messages

    except ClientError as err:
        message = err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        print(f"A client error occured: {message}")

    finally:
        print(f"Finished generating text with model {model_id}.")
