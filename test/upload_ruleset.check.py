import asyncio
import sys
import os
import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

from dotenv import load_dotenv
load_dotenv(dotenv_path=str(BASE_DIR / ".env"))

from utils.ruleset_s3 import upload_ruleset
from utils.aws_clients import get_s3_client

logging.basicConfig(
    level=logging.INFO,
    format="🔧 %(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)

async def main():
    logger.info("🚀 Bắt đầu upload ruleset lên S3 (pending)...")
    ruleset_id = "test_ruleset_1"
    content = {"field": "value", "status": "pending"}
    try:
        result = upload_ruleset(ruleset_id, content)
        if result:
            logger.info(f"✅ Đã upload ruleset '{ruleset_id}' vào trạng thái pending thành công!")
        else:
            logger.error(f"❌ Upload ruleset '{ruleset_id}' thất bại!")
    except Exception as err:
        logger.error(f"🔥 Lỗi khi upload ruleset: {str(err)}")

if __name__ == "__main__":
    asyncio.run(main()) 