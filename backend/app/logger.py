import logging

# Configure logging (only console output, no file logs)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.StreamHandler()]  # Only print to console
)

logger = logging.getLogger(__name__)
