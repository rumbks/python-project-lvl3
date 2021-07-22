from functools import partial
from pathlib import Path
from typing import Union, List

from funcy import walk, select

from page_loader import html
from page_loader.html import get_images, Resource, change_url, in_same_domain
from page_loader.io import web, file
from page_loader.path import (
    get_page_filename,
    get_assets_folder_name,
    get_asset_filename,
)
from page_loader.url import to_absolute_url


def download(url: str, save_to: Union[str, Path] = None) -> str:
    save_to = Path.cwd() if save_to is None else Path(save_to)
    if not save_to.exists():
        raise RuntimeError(f"Directory {save_to} does not exists.")
    page_text = web.download(url)
    page_filename = get_page_filename(url)

    parsed_page = html.parse(page_text)

    images = get_images(parsed_page)
    assets_directory = save_to / get_assets_folder_name(url)
    if images:
        assets_directory.mkdir(exist_ok=True)

    to_absolute = partial(to_absolute_url, url)
    images = select(in_same_domain, images)
    images: List[Resource] = walk(
        lambda img: Resource(img.tag, to_absolute(img.url)), images
    )

    for image in images:
        asset_filename = get_asset_filename(image.url)
        img_bytes = web.download(image.url, bytes=True)
        file.save(
            directory=assets_directory,
            filename=asset_filename,
            content=img_bytes,
        )
        change_url(image, str(Path(assets_directory.name) / asset_filename))

    file.save(
        directory=save_to,
        filename=page_filename,
        content=parsed_page.prettify(formatter='html5'),
    )
    return str(save_to / page_filename)
