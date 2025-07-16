import asyncio
import sys
import os
import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))
sys.path.insert(1, str(BASE_DIR / "venv"))

from dotenv import load_dotenv
load_dotenv(dotenv_path=str(BASE_DIR / ".env"))

# Import từ services và utils
from services.data_contract import generate_draft_datacontract
from utils.constants import TEST_DIR, TEST_BUCKET_NAME
from utils.s3 import upload_file
from utils.aws_clients import get_s3_client

# Cấu hình logging rõ ràng hơn
logging.basicConfig(
    level=logging.INFO,
    format="🔧 %(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    logger.info("🚀 Bắt đầu upload file lên S3...")

    file_name = "hello.txt"
    folder_in_s3 = "pending"
    bucket_name = TEST_BUCKET_NAME
    file_path = Path(TEST_DIR) / file_name
    object_name = f"{folder_in_s3}/{file_name}"

    # Kiểm tra file tồn tại
    if not file_path.exists():
        logger.error(f"❌ File không tồn tại: {file_path}")
        return

    # Lấy S3 client
    s3_client = get_s3_client()

    try:
        logger.info(f"📤 Upload: {file_path} → bucket: {bucket_name} → object: {object_name}")

        upload_file(
            s3_client=s3_client,
            file_name=str(file_path),
            bucket_name=bucket_name,
            object_name=object_name,
            metadata={"status": "pending"}
        )

        region = s3_client.meta.region_name
        url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{object_name}"
        logger.info(f"✅ File đã upload thành công: {url}")

    except Exception as err:
        logger.error(f"🔥 Lỗi khi upload file: {str(err)}")


if __name__ == "__main__":
    asyncio.run(main())
