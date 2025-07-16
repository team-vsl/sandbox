import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

import logging
from dotenv import load_dotenv
from utils.ruleset_s3 import get_ruleset

# Setup
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

load_dotenv(dotenv_path=str(BASE_DIR / ".env"))

# Set ID bạn muốn get
RULESET_ID = "test_ruleset_1"
STATUS = "pending"  # hoặc approved/rejected

# Run
try:
    logger.info(f"🔍 Getting ruleset: {RULESET_ID} (status: {STATUS})")
    result = get_ruleset(RULESET_ID, status=STATUS)
    if result:
        print("📄 Ruleset content:")
        print(result)
    else:
        logger.warning("⚠️  Ruleset not found.")
except Exception as e:
    logger.error(f"🔥 Lỗi khi get ruleset: {e}")
