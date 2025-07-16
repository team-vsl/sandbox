import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(BASE_DIR, "src"))


from dotenv import load_dotenv
from langchain_aws import ChatBedrock
from utils import get_bedrock_client 

from genai.contract_agent import ContractAgent

load_dotenv()

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

client = get_bedrock_client()
model_id = "anthropic.claude-3-haiku-20240307-v1:0"

llm = ChatBedrock(client=client, model_id=model_id)
graph_agent = ContractAgent(llm_instance=llm)


def main():
    """
    Entrypoint for Anthropic Claude 3 Sonnet example.
    """

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    user_input = input("Enter your question: ")

    while True:
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        
        response = graph_agent.invoke(user_input)
        print(response)
        user_input = input("User: ")

if __name__ == "__main__":
    main()

