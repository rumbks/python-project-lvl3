import logging
from sys import stdout, stderr


def get_stream_logger(name: str, stream) -> logging.Logger:
    logger_ = logging.getLogger(name)
    logger_.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler(stream)
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logger_.addHandler(stream_handler)
    return logger_


logger = get_stream_logger("page_loader", stdout)
error_logger = get_stream_logger("page_loader_error", stderr)
