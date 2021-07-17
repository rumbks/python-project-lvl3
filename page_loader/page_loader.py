from pathlib import Path
from typing import Union

import requests

from page_loader.io import write
from page_loader.path import get_filename_to_save, get_full_path


def download(url: str, save_to: Union[str, Path] = None) -> str:
    save_to = Path.cwd() if save_to is None else Path(save_to)
    response = requests.get(url)
    filename = get_filename_to_save(url)
    write(
        directory=save_to,
        filename=filename,
        content=response.text,
    )
    return str(get_full_path(save_to, filename))
