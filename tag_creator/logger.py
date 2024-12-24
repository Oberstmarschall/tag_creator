import logging

logging.basicConfig(
    level=logging.INFO,
    datefmt="%H:%M:%S",
    format="%(asctime)s %(module)s %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)
