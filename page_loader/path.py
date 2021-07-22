from string import ascii_letters, digits

from funcy import merge, walk, cut_suffix

from page_loader.url import without_schema


def get_extension(path: str):
    return merge(".", path.split(".")[-1])


def _build_name(url: str, postfix: str = ""):
    LETTERS_AND_DIGITS = ascii_letters + digits
    return merge(
        walk(
            lambda s: s if s in LETTERS_AND_DIGITS else '-',
            without_schema(url),
        ),
        postfix,
    )


def get_page_filename(url: str) -> str:
    return _build_name(url, ".html")


def get_asset_filename(url: str):
    extension = get_extension(url)
    path = cut_suffix(url, extension)
    return _build_name(path, extension)


def get_assets_folder_name(url: str) -> str:
    return _build_name(url, "_files")
