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

# Import từ utils
from utils.constants import TEST_BUCKET_NAME
from utils.s3 import list_files
from utils.aws_clients import get_s3_client

logging.basicConfig(level=logging.INFO, format=" %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


async def main():
    logger.info(" Bắt đầu kiểm tra list_files() từ S3 bucket")

    bucket_name = TEST_BUCKET_NAME
    s3_client = get_s3_client()

    folders = ["pending"]

    for folder in folders:
        prefix = f"{folder}/"
        logger.info(f" Đang liệt kê file trong folder: {prefix}")

        try:
            files = list_files(
                s3_client=s3_client,
                bucket_name=bucket_name,
                prefix=prefix
            )

            # Lọc bỏ object là thư mục "prefix/"
            for f in files:
                if f == prefix:
                    continue
                print(f" {f}")

        except Exception as err:
            logger.error(f" Lỗi khi list files từ folder {prefix}: {str(err)}")


if __name__ == "__main__":
    asyncio.run(main())
