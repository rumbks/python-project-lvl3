from typing import Union

import requests


def download(url: str, bytes=False) -> Union[str, bytes]:
    response = requests.get(url)
    return response.content if bytes else response.text
