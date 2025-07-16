import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

import logging
from dotenv import load_dotenv
from utils.ruleset_s3 import list_rulesets

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

load_dotenv(dotenv_path=str(BASE_DIR / ".env"))

STATUS = "pending"  # hoặc approved/rejected

try:
    logger.info(f"🔍 Listing rulesets with status: {STATUS}")
    rulesets = list_rulesets(status=STATUS)
    if rulesets:
        logger.info(f"Found rulesets: {rulesets}")
    else:
        logger.warning("⚠️ No rulesets found.")
except Exception as e:
    logger.error(f"🔥 Lỗi khi list rulesets: {e}")
