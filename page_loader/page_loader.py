from pathlib import Path
from string import ascii_letters, digits
from typing import Union

import requests
from funcy import walk, cut_prefix, merge


def without_schema(url: str) -> str:
    HTTP = 'http://'
    HTTPS = 'https://'
    if url.startswith(HTTP):
        return cut_prefix(url, HTTP)
    return cut_prefix(url, HTTPS)


def get_filename(url: str) -> str:
    LETTERS_AND_DIGITS = ascii_letters + digits
    return merge(
        walk(
            lambda s: s if s in LETTERS_AND_DIGITS else '-',
            without_schema(url),
        ),
        ".html",
    )


def download(url: str, save_to: Union[str, Path] = None) -> str:
    save_to = Path.cwd() if save_to is None else Path(save_to)
    if not save_to.exists():
        raise RuntimeError(f"Directory {save_to} does not exists.")

    response = requests.get(url)
    path_to_page = save_to / get_filename(url)
    with open(path_to_page, "w") as file:
        file.write(response.text)
    return str(path_to_page)
