import logging


logger = logging.getLogger(__file__)

if not logger.hasHandlers():
    # AWS sets a handler automatically, so this helps local
    logger.addHandler(logging.StreamHandler())
