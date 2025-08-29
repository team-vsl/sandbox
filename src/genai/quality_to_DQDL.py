from langchain_core.messages import SystemMessage, HumanMessage


def quality_to_DQDL(quality_data_session, llm_instance):

    system_prompt = """
You are a converter that transforms session-defined data model into AWS Glue Data Quality Definition Language (DQDL) format.

Your task is to:
1. Convert each check into a corresponding DQDL rule using AWS Glue's declarative syntax.
2. Use `Rules:` section syntax in DQDL.
3. Only return the DQDL query. Do not provide explanations or other responses.
4. Only transform data fields that have a "quality" property.

Output only the DQDL result (no extra explanation).

Example Input:
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


Expected Output (DQDL):
Rules = [
    IsComplete "age",
    ColumnValues "age" > 18,
    IsComplete "pdays",
    ColumnValues "pdays" >= -1
]
  """
    message = [SystemMessage(content=system_prompt), HumanMessage(content=quality_data_session)]
    dqdl_data = llm_instance.invoke(message)

    return dqdl_data