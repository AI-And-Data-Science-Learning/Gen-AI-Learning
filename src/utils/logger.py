import logging
from pathlib import Path

# Create logs directory
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_DIR / "app.log", encoding="utf-8")
    ]
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.debug("Debug message")
    logger.info("Logger initialized successfully")
    logger.warning("Warning message")
    logger.error("Error message")