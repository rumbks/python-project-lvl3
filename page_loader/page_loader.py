from functools import partial
from pathlib import Path
from typing import Union, List

from funcy import walk, select, all_fn

from page_loader import html
from page_loader.assets import (
    get_assets,
    AssetType,
    in_same_domain as is_asset_located_in_same_domain,
    contains_file,
)
from page_loader.html import Asset, change_asset_url
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

    assets = get_assets(parsed_page)
    to_absolute = partial(to_absolute_url, url)
    assets: List[Asset] = walk(
        lambda asset: Asset(asset.type, asset.tag, to_absolute(asset.url)),
        assets,
    )
    in_same_domain = partial(is_asset_located_in_same_domain, url)
    is_local_asset = all_fn(in_same_domain, contains_file)
    local_assets = select(is_local_asset, assets)

    assets_directory = save_to / get_assets_folder_name(url)
    if local_assets:
        assets_directory.mkdir(exist_ok=True)

    for asset in local_assets:
        asset_filename = get_asset_filename(asset.url)
        asset_file_content = web.download(
            asset.url, bytes=asset.type is AssetType.IMAGE
        )
        file.save(
            directory=assets_directory,
            filename=asset_filename,
            content=asset_file_content,
        )
        change_asset_url(
            asset, str(Path(assets_directory.name) / asset_filename)
        )

    file.save(
        directory=save_to,
        filename=page_filename,
        content=parsed_page.prettify(formatter='html5'),
    )
    return str(save_to / page_filename)
