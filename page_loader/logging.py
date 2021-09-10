import logging
from sys import stdout

logger = logging.getLogger("page_loader")
logger.setLevel(logging.DEBUG)
log_formatter = logging.Formatter("%(levelname)s: %(message)s")
console_handler = logging.StreamHandler(stdout)
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)