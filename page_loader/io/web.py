from typing import Union

import requests
from page_loader.logging import logger


def download(url: str, bytes=False) -> Union[str, bytes]:
    logger.info(f"Downloading page/resource from url {url}...")
    response = requests.get(url)
    response.raise_for_status()
    logger.info("Download succeeded.")
    result = response.content if bytes else response.text
    return result
