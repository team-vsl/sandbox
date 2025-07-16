import asyncio
import sys
import os
import logging
from pathlib import Path

# Set up paths
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))
sys.path.insert(1, str(BASE_DIR / "venv"))

from dotenv import load_dotenv
load_dotenv(dotenv_path=str(BASE_DIR / ".env"))

# Import
from utils.constants import TEST_BUCKET_NAME
from utils.aws_clients import get_s3_client
from utils.s3 import move_file

# Logging setup
logging.basicConfig(level=logging.INFO, format="🔁 %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


async def main():
    logger.info("🚀 Bắt đầu di chuyển file từ pending → approved")

    file_name = "hello.txt"
    bucket_name = TEST_BUCKET_NAME
    source_key = f"pending/{file_name}"
    destination_prefix = "approved"
    destination_key = f"{destination_prefix}/{file_name}"  # 🔧 FIX: không dùng os.path.join

    s3_client = get_s3_client()

    try:
        logger.info(f"📤 Đang move: {source_key} → {destination_key}")

        success = move_file(
            s3_client=s3_client,
            bucket_name=bucket_name,
            source_key=source_key,
            destination_prefix=destination_prefix,  # hàm move_file sẽ build lại key
            metadata={"status": "approved"}
        )

        if success:
            region = s3_client.meta.region_name
            url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{destination_key}"
            logger.info(f"✅ Đã move thành công: {url}")
        else:
            logger.error(f"❌ Move thất bại: {source_key}")

    except Exception as err:
        logger.error(f"🔥 Lỗi khi thực hiện move: {str(err)}")


if __name__ == "__main__":
    asyncio.run(main())
