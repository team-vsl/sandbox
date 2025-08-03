import sys
from pathlib import Path

# 👉 Thêm dòng này để add thư mục src vào sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

import json
import logging
from dotenv import load_dotenv
from utils.ruleset_s3 import upload_ruleset

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Load env
load_dotenv(dotenv_path=str(Path(__file__).resolve().parent.parent / ".env"))

# Đọc file JSON
file_path = Path("sample_ruleset.json")

try:
    with open(file_path, "r") as f:
        content = json.load(f)
        ruleset_id = content.get("ruleset_id")
        if not ruleset_id:
            raise ValueError(" File JSON thiếu trường 'ruleset_id'")
        
        logger.info(f" Uploading ruleset: {ruleset_id}")
        upload_ruleset(ruleset_id, content)
        logger.info(" Upload thành công!")

except Exception as e:
    logger.error(f" Upload thất bại: {e}")
