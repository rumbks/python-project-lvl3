from pathlib import Path
from string import ascii_letters, digits
from urllib.parse import urljoin, urlparse

from funcy import merge, walk, cut_suffix


def to_absolute_url(root_page_url: str, relative_url: str) -> str:
    return urljoin(root_page_url, relative_url)


def without_schema(url: str) -> str:
    parsed = urlparse(url)
    return merge(parsed.netloc, parsed.path)


def get_domain_name(url: str) -> str:
    parsed = urlparse(url)
    return parsed.netloc


def get_extension(path: str):
    """
    Returns extension with "." if it presents
    Otherwise returns ""
    """
    return Path(path).suffix


def _build_name(url: str, postfix: str = ""):
    LETTERS_AND_DIGITS = ascii_letters + digits
    return merge(
        walk(
            lambda s: s if s in LETTERS_AND_DIGITS else '-',
            without_schema(url),
        ),
        postfix,
    )


def to_page_filename(url: str) -> str:
    return _build_name(url, ".html")


def to_asset_filename(url: str):
    extension = get_extension(url) or ".html"
    path = cut_suffix(url, extension)
    return _build_name(path, extension)


def to_assets_folder_name(url: str) -> str:
    return _build_name(url, "_files")
