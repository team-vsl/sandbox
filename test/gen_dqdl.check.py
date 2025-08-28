import sys
import os
import time

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(BASE_DIR, "src"))


from dotenv import load_dotenv
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage
from utils import get_bedrock_client

load_dotenv()

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from genai.quality_to_DQDL import quality_to_DQDL

quality_data_session = """
banking_marketing_data:
  type: table
  description: 'thông tin khách hàng, mỗi record là 1 cá nhân'
  title: banking_marketing_data
  fields:
    age:
      description: tuổi của khác hàng
      type: int
      quality:
        - type: sql
          description: age phải lớn hơn 18
          query: SELECT COUNT(*) FROM banking_marketing_data WHERE age <= 18
          expectedResult: = 0
    job:
      description: nghề nghiệp của khách hàng
      type: string
    duration:
      description: 'tổng thời gian liên lạc gần nhất, tính bằng giây'
      type: int
    campaign:
      description: >-
        số lần tiếp xúc/liên lạc đã thực hiện trong chiến dịch hiện tại đối với
        1 khách hàng cụ thể, bao gồm cả lần liên hệ cuối cùng
      type: int
    pdays:
      description: >-
        số ngày trôi qua kể từ lần cuối cùng khách hàng được liên hệ trong chiến
        dịch trước đó. -1 được dùng để chỉ ra rằng khách hàng chưa từng được
        liên hệ trong các chiến dịch trước đó
      type: int
      quality:
        - type: sql
          description: dữ liệu chỉ có thể lớn hơn 0 hoặc bằng -1
          query: SELECT COUNT(*) FROM banking_marketing_data WHERE pdays < -1
          expectedResult: = 0
    previous:
      description: số lượng liên hệ được thực hiện trước chiến dịch hiện tại
      type: int
    poutcome:
      description: kết quả của chiến dịch tiếp thị
      type: string
      enum:
        - unknown
        - other
        - failure
        - success
  quality: []
"""


def main():
    """
    Entrypoint for Anthropic Claude 3 Sonnet example.
    """
    client = get_bedrock_client()
    model_id = "anthropic.claude-3-haiku-20240307-v1:0"

    llm = ChatBedrock(client=client, model_id=model_id)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    response = quality_to_DQDL(quality_data_session, llm)
    print(response.content)
    time.sleep(30)


if __name__ == "__main__":
    main()
