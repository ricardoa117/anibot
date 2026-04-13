import logging
from config import LOG_LEVEL

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=LOG_LEVEL
)

logger = logging.getLogger(__name__)