import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

from runtime.lambda_handlers import invoke_agent

# Giả lập event và context như AWS Lambda
event = {
    "body": '{"input": "Tạo data contract cho bảng khách hàng"}'
}
context = {}

import asyncio

async def main():
    result = await invoke_agent.handler(event, context)
    print("Kết quả trả về:")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())