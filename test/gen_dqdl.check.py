import sys
import os
import time

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(BASE_DIR, "src"))


from dotenv import load_dotenv
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage
from utils.aws_clients import get_bedrock_client

load_dotenv()

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from genai.quality_to_DQDL import quality_to_DQDL

quality_data_session = """
data_models:
  banking_marketing_data:
    description: thông tin khách hàng, mỗi record là 1 cá nhân
    fields:
      age:
        classification: null
        description: tuổi của khách hàng
        enum: null
        example: null
        fields: null
        pii: null
        primaryKey: null
        quality:
        - description: age phải lớn hơn 18
          dialect: null
          expectedResult: = 0
          query: SELECT COUNT(*) FROM banking_marketing_data WHERE age <= 18
          type: sql
        references: null
        required: null
        title: null
        type: int
        unique: null
      campaign:
        classification: null
        description: số lần tiếp xúc/liên lạc đã thực hiện trong chiến dịch hiện tại
          đối với 1 khách hàng cụ thể, bao gồm cả lần liên hệ cuối cùng
        enum: null
        example: null
        fields: null
        pii: null
        primaryKey: null
        quality: null
        references: null
        required: null
        title: null
        type: integer
        unique: null
      duration:
        classification: null
        description: tổng thời gian liên lạc gần nhất, tính bằng giây
        enum: null
        example: null
        fields: null
        pii: null
        primaryKey: null
        quality: null
        references: null
        required: null
        title: null
        type: integer
        unique: null
      job:
        classification: null
        description: nghề nghiệp của khách hàng
        enum: null
        example: null
        fields: null
        pii: null
        primaryKey: null
        quality: null
        references: null
        required: null
        title: null
        type: string
        unique: null
      pdays:
        classification: null
        description: số ngày trôi qua kể từ lần cuối cùng khách hàng được liên hệ
          trong chiến dịch trước đó. -1 được dùng để chỉ ra rằng khách hàng chưa từng
          được liên hệ trong các chiến dịch trước đó
        enum: null
        example: null
        fields: null
        pii: null
        primaryKey: null
        quality:
        - description: dữ liệu chỉ có thể lớn hơn 0 hoặc bằng -1
          dialect: null
          expectedResult: = 0
          query: SELECT COUNT(*) FROM banking_marketing_data WHERE pdays < -1
          type: sql
        references: null
        required: null
        title: null
        type: integer
        unique: null
      poutcome:
        classification: null
        description: kết quả của chiến dịch tiếp thị
        enum:
        - unknown
        - other
        - failure
        - success
        example: null
        fields: null
        pii: null
        primaryKey: null
        quality: null
        references: null
        required: null
        title: null
        type: string
        unique: null
      previous:
        classification: null
        description: số lượng liên hệ được thực hiện trước chiến dịch hiện tại
        enum: null
        example: null
        fields: null
        pii: null
        primaryKey: null
        quality: null
        references: null
        required: null
        title: null
        type: integer
        unique: null
    quality: []
    title: Banking Marketing
    type: table
"""


def main():
    """
    Entrypoint for Anthropic Claude 3 Sonnet example.
    """
    client = get_bedrock_client()
    model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"

    llm = ChatBedrock(client=client, model_id=model_id)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    response = quality_to_DQDL(quality_data_session, llm)
    print(response.content)
    time.sleep(30)


if __name__ == "__main__":
    main()
