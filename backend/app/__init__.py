import logging

__version__ = "0.1.0"

# Configure a consistent logging format for the entire app
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)
logger.info(f"Starting Text2Video API (version {__version__})")
