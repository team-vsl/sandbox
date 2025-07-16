import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(BASE_DIR))

import logging
from dotenv import load_dotenv
from utils.ruleset_s3 import approve_ruleset, reject_ruleset, list_rulesets

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

load_dotenv()

def test_approve_ruleset(ruleset_id):
    logger.info(f"Test approve ruleset: {ruleset_id}")
    try:
        success = approve_ruleset(ruleset_id)
        if success:
            logger.info(f"✅ Approved ruleset {ruleset_id} successfully.")
        else:
            logger.error(f"❌ Failed to approve ruleset {ruleset_id}.")
    except Exception as e:
        logger.error(f"🔥 Error approving ruleset: {e}")

def test_reject_ruleset(ruleset_id):
    logger.info(f"Test reject ruleset: {ruleset_id}")
    try:
        success = reject_ruleset(ruleset_id)
        if success:
            logger.info(f"✅ Rejected ruleset {ruleset_id} successfully.")
        else:
            logger.error(f"❌ Failed to reject ruleset {ruleset_id}.")
    except Exception as e:
        logger.error(f"🔥 Error rejecting ruleset: {e}")

def test_list_rulesets():
    logger.info("Test list rulesets for all statuses")

    for status in ["pending", "approved", "rejected"]:
        try:
            rulesets = list_rulesets(status=status)
            logger.info(f"{status.capitalize()} rulesets: {rulesets}")
        except Exception as e:
            logger.error(f"🔥 Error listing {status} rulesets: {e}")

if __name__ == "__main__":
    RULESET_ID = "test_ruleset_1"

    test_list_rulesets()

    # Test approve: sẽ chuyển ruleset sample_ruleset_1 từ pending sang approved
    test_approve_ruleset(RULESET_ID)

    # Test reject: nếu muốn, có thể test reject (lưu ý ruleset phải nằm ở pending để reject)
    # test_reject_ruleset(RULESET_ID)
