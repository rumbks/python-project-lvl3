from functools import partial
from pathlib import Path
from typing import List, Union

from funcy import select, walk
from page_loader import html
from page_loader.assets import AssetType, get_assets
from page_loader.assets import in_same_domain as is_asset_located_in_same_domain
from page_loader.html import Asset, change_asset_url
from page_loader.io import file, web
from page_loader.logging import logger
from page_loader.path import (
    get_asset_filename,
    get_assets_folder_name,
    get_page_filename,
)
from page_loader.url import to_absolute_url


def download(url: str, save_to: Union[str, Path] = None) -> str:
    save_to = Path.cwd() if save_to is None else Path(save_to)
    if not save_to.exists():
        error_message = f"Directory {save_to} does not exists."
        logger.error(error_message)
        raise RuntimeError(error_message)
    page_text = web.download(url)
    page_filename = get_page_filename(url)

    parsed_page = html.parse(page_text)

    assets = get_assets(parsed_page)
    logger.info(f"There's {len(assets)} asserts inside the page.")
    to_absolute = partial(to_absolute_url, url)
    assets: List[Asset] = walk(
        lambda asset: Asset(asset.type, asset.tag, to_absolute(asset.url)),
        assets,
    )
    in_same_domain = partial(is_asset_located_in_same_domain, url)
    local_assets = select(in_same_domain, assets)
    logger.info(f"{len(local_assets)} of them are local.")

    assets_directory = save_to / get_assets_folder_name(url)
    if local_assets:
        assets_directory.mkdir(exist_ok=True)

    for i, asset in enumerate(local_assets, 1):
        asset_filename = get_asset_filename(asset.url)
        logger.info(f"Downloading asset {i}. Tag is {asset.tag}.")
        asset_file_content = web.download(
            asset.url, bytes=asset.type is AssetType.IMAGE
        )
        file.save(
            directory=assets_directory,
            filename=asset_filename,
            content=asset_file_content,
        )
        logger.info(f"Asset {i} was successfully downloaded and saved.")
        change_asset_url(
            asset, str(Path(assets_directory.name) / asset_filename)
        )

    file.save(
        directory=save_to,
        filename=page_filename,
        content=parsed_page.prettify(formatter='html5'),
    )
    return str(save_to / page_filename)
