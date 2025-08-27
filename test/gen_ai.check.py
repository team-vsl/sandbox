import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(BASE_DIR, "src"))


from dotenv import load_dotenv
from langchain_aws import ChatBedrock
from utils import get_bedrock_client 
from langchain_core.messages import HumanMessage

load_dotenv()

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

client = get_bedrock_client()
model_id = "anthropic.claude-3-haiku-20240307-v1:0"

sample_data_contract = {
  "id": "auto-generated-id",
  "metainfo": {
    "title": "Orders Data Product",
    "description": "Data product chứa thông tin các đơn hàng từ hệ thống bán hàng",
    "owner": "Sales Analytics Team",
    "contact": {
      "name": "Nguyễn Văn A",
      "email": "nguyen.a@company.com",
      "url": None   
    }
  },
  "server": {
    "redshift": {
      "type": "redshift",
      "description": None,
      "environment": None,
      "roles": None,
      "account": None,
      "database": None,
      "redshift_schema": None,
      "clusterIdentifier": None,
      "host": None,
      "port": None,
      "endpoint": None
    }
  },
  "terms": {
    "usage": "Dữ liệu dùng cho báo cáo nội bộ và phân tích",
    "limitations": "Không dùng cho truy vấn real-time hoặc mục đích cá nhân",
    "policy": [
      "privacy-policy"
    ],
    "noticePeriod": "P1M"
  },
  "data_models": {
    "models": {
      "orders": {
        "type": "table",
        "description": "Thông tin đơn hàng, mỗi record là một đơn",
        "title": None,
        "fields": {
          "sample_data_fields": {
            "description": "sample data",
            "type": "text",
            "title": None,
            "enum": None,
            "required": None,
            "primaryKey": None,
            "references": None,
            "unique": None,
            "example": None,
            "pii": None,
            "classification": None,
            "fields": None,
            "quality": None
          }
        },
        "quality": {
          "quality": [
            {
              "type": "sql",
              "description": "Phải có ít nhất 1 bản ghi (row_count >= 1)",
              "query": "SELECT COUNT(*) FROM orders",
              "expectedResult": "row_count >= 1",
              "dialect": None
            },
            {
              "type": "sql",
              "description": "Trường id không được null và phải là duy nhất",
              "query": "SELECT COUNT(DISTINCT id) FROM orders",
              "expectedResult": "row_count = (SELECT COUNT(*) FROM orders)",
              "dialect": None
            }
          ]
        }
      }
    }
  },
  "servicelevels": {}
}

llm = ChatBedrock(client=client, model_id=model_id)

def check_agent(agent_name):
    if agent_name == "info":
        from genai.sub_agent.info import InfoAgent
        agent = InfoAgent(llm_instance=llm)
    elif agent_name == "data_model":
        from genai.sub_agent.data_model import DataModelAgent
        agent = DataModelAgent(llm_instance=llm)

    elif agent_name == "root":
        from genai.contract_agent import DataContractAgent
        agent = DataContractAgent(llm_instance=llm, data_contract=sample_data_contract)
        agent = DataContractAgent(llm_instance=llm)

    elif agent_name == "server":
        from genai.sub_agent.server import ServerAgent
        agent = ServerAgent(llm_instance=llm)

    elif agent_name == "terms":
        from genai.sub_agent.terms import TermsAgent
        agent = TermsAgent(llm_instance=llm)

    elif agent_name == "sl":
        from genai.sub_agent.servicelevels import ServiceLevelsAgent
        agent = ServiceLevelsAgent(llm_instance=llm)

    return agent



def main():
    """
    Entrypoint for Anthropic Claude 3 Sonnet example.
    """

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    user_input = input("Enter your question: ")

    agent = check_agent("root")

    while True:
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
    

        response = agent.invoke(user_input)
        print(response)
        user_input = input("User: ")

if __name__ == "__main__":
    main()

