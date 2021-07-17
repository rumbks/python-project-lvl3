from pathlib import Path
from string import ascii_letters, digits

from funcy import cut_prefix, merge, walk


def _without_schema(url: str) -> str:
    HTTP = 'http://'
    HTTPS = 'https://'
    if url.startswith(HTTP):
        return cut_prefix(url, HTTP)
    return cut_prefix(url, HTTPS)


def get_full_path(directory_path: Path, filename: str):
    return directory_path / filename


def get_filename_to_save(url: str) -> str:
    LETTERS_AND_DIGITS = ascii_letters + digits
    return merge(
        walk(
            lambda s: s if s in LETTERS_AND_DIGITS else '-',
            _without_schema(url),
        ),
        ".html",
    )
