import sys
from pathlib import Path
import json
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

# Load environment variables
load_dotenv(BASE_DIR / ".env")

from runtime.lambda_handlers import invoke_agent

async def detailed_test():
    event = {
        "body": json.dumps({
            "input": "Tạo data contract cho bảng khách hàng để lên chiến dịch marketing email và SMS, cần phân khúc theo độ tuổi, giới tính, và giá trị tài khoản"
        })
    }
    context = {}

    result = await invoke_agent.handler(event, context)
    
    if result.get('statusCode') == 200:
        # parse response body JSON string
        body_str = result.get('body', '{}')
        body = json.loads(body_str)
        
        data = body.get('data')
        # Nếu data vẫn là string JSON, parse tiếp
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except Exception:
                pass
        
        pretty_print_contract(data)
    else:
        print(f"Error: {result}")

def pretty_print_contract(data_contract):
    print("Complete Data Contract:")
    print(json.dumps(data_contract, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    import asyncio
    asyncio.run(detailed_test())
