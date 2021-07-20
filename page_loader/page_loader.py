from pathlib import Path
from typing import Union

import requests

from page_loader.io import write
from page_loader.path import get_page_filename


def download(url: str, save_to: Union[str, Path] = None) -> str:
    save_to = Path.cwd() if save_to is None else Path(save_to)
    response = requests.get(url)
    page_filename = get_page_filename(url)
    write(
        directory=save_to,
        filename=page_filename,
        content=response.text,
    )
    return str(save_to / page_filename)
