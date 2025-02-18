import logging

# Configuration basique du logger
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s - %(message)s")

logger = logging.getLogger(__name__)
