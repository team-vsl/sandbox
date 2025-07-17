import sys
from pathlib import Path
import json
import asyncio

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

from runtime.lambda_handlers.invoke_agent import handler, process_user_input


async def test_lambda_handler():
    """Test the Lambda handler function"""
    print("🚀 Testing Lambda Handler...")
    
    # Test case 1: Valid input
    test_event = {
        "body": json.dumps({
            "input": "Tạo data contract cho bảng khách hàng để lên chiến dịch marketing email và SMS, cần phân khúc theo độ tuổi, giới tính, và giá trị tài khoản"
        })
    }
    
    print("📝 Test Input:", test_event["body"])
    
    try:
        result = await handler(test_event, {})
        print("✅ Lambda Handler Response:")
        print(f"Status Code: {result['statusCode']}")
        
        # Parse and pretty print the response body
        if result.get('body'):
            body = json.loads(result['body'])
            print("Response Body:")
            print(json.dumps(body, indent=2, ensure_ascii=False))
            
            # Check if data contract was generated
            if body.get('success') and body.get('data'):
                print("\n🎉 Data Contract Generated Successfully!")
                data_contract = body['data']
                print(f"Contract ID: {data_contract.get('id')}")
                print(f"Info Title: {data_contract.get('info', {}).get('title', 'N/A')}")
                print(f"Server Count: {len(data_contract.get('server', {}))}")
                print(f"Data Models Count: {len(data_contract.get('data_models', {}))}")
            else:
                print("❌ Failed to generate data contract")
                
    except Exception as e:
        print(f"❌ Error testing Lambda handler: {e}")


async def test_process_user_input():
    """Test the core processing function directly"""
    print("\n🔧 Testing Core Processing Function...")
    
    user_inputs = [
        "Tạo data contract cho bảng sản phẩm e-commerce với thông tin giá, tồn kho, và danh mục",
        "Create data contract for customer analytics table with demographics and purchase history",
        "Tạo hợp đồng dữ liệu cho bảng giao dịch ngân hàng với thông tin bảo mật cao"
    ]
    
    for i, user_input in enumerate(user_inputs, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Input: {user_input}")
        
        try:
            result = await process_user_input(user_input)
            
            if result['success']:
                print("✅ Processing successful")
                data_contract = result['data']
                print(f"Generated Contract ID: {data_contract.get('id')}")
                
                # Validate required fields
                required_fields = ['id', 'info', 'server', 'terms', 'data_models', 'definitions', 'servicelevels']
                missing_fields = [field for field in required_fields if field not in data_contract]
                
                if missing_fields:
                    print(f"⚠️  Missing fields: {missing_fields}")
                else:
                    print("✅ All required fields present")
                    
            else:
                print(f"❌ Processing failed: {result.get('message', 'Unknown error')}")
                if 'error' in result:
                    print(f"Error details: {result['error']}")
                    
        except Exception as e:
            print(f"❌ Exception during processing: {e}")


async def test_invalid_inputs():
    """Test with invalid inputs"""
    print("\n🧪 Testing Invalid Inputs...")
    
    invalid_events = [
        # Missing body
        {},
        # Empty body
        {"body": "{}"},
        # Missing input field
        {"body": json.dumps({"message": "hello"})},
        # Empty input
        {"body": json.dumps({"input": ""})},
        # Invalid JSON body
        {"body": "invalid json"},
    ]
    
    for i, event in enumerate(invalid_events, 1):
        print(f"\n--- Invalid Test Case {i} ---")
        print(f"Event: {event}")
        
        try:
            result = await handler(event, {})
            print(f"Status Code: {result['statusCode']}")
            
            if result.get('body'):
                body = json.loads(result['body'])
                print(f"Response: {body.get('message', 'No message')}")
                
        except Exception as e:
            print(f"Exception (expected): {e}")


async def main():
    """Run all tests"""
    print("🎯 Starting Lambda Function Tests\n")
    
    await test_lambda_handler()
    await test_process_user_input()
    await test_invalid_inputs()
    
    print("\n🏁 All tests completed!")


if __name__ == "__main__":
    asyncio.run(main())