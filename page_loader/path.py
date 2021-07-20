from string import ascii_letters, digits

from funcy import cut_prefix, merge, walk


def _without_schema(url: str) -> str:
    HTTP = 'http://'
    HTTPS = 'https://'
    if url.startswith(HTTP):
        return cut_prefix(url, HTTP)
    return cut_prefix(url, HTTPS)


def _build_name(url: str, postfix: ""):
    LETTERS_AND_DIGITS = ascii_letters + digits
    return merge(
        walk(
            lambda s: s if s in LETTERS_AND_DIGITS else '-',
            _without_schema(url),
        ),
        postfix,
    )


def get_page_filename(url: str) -> str:
    return _build_name(url, ".html")


def get_assets_folder_name(url: str) -> str:
    return _build_name(url, "_files")
