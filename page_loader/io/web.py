from typing import Union

import requests
from page_loader.logging import logger


def download(url: str, bytes=False) -> Union[str, bytes]:
    response = requests.get(url)
    response.raise_for_status()
    logger.info(f"Downloading page/resource from url {url}...")
    result = response.content if bytes else response.text
    logger.info("Download succeeded.")
    return result
