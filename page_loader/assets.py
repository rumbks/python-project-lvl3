from enum import Enum
from pathlib import Path
from typing import NamedTuple, List
from urllib.parse import urlparse

from bs4 import BeautifulSoup, Tag

AssetType = Enum("AssetType", [("IMAGE", "img"), ("LINK", "link"), ("SCRIPT", "script")])

Asset = NamedTuple(
    "Asset", [('type', AssetType), ('tag', Tag), ('url', str)]
)

ASSET_ATTR = {
    AssetType.IMAGE: 'src',
    AssetType.LINK: 'href',
    AssetType.SCRIPT: 'src',
}


def get_asset_type(tag: Tag):
    if tag.name == 'link':
        type_ = AssetType.LINK
    elif tag.name == 'img':
        type_ = AssetType.IMAGE
    elif tag.name == 'script':
        type_ = AssetType.SCRIPT
    else:
        raise RuntimeError(f"Can't determine resource type for tag {tag}")
    return type_


def contains_file(asset: Asset) -> bool:
    url = urlparse(asset.url)
    path = Path(url.path)
    return bool(path.suffix)


def in_same_domain(root_page_url: str, asset: Asset) -> bool:
    root_page_url = urlparse(root_page_url)
    asset_url = urlparse(asset.url)

    return not asset_url.netloc or asset_url.netloc == root_page_url.netloc


def get_assets(parsed_html: BeautifulSoup) -> List[Asset]:
    """
    :param parsed_html: parsed content of html page
    :return: tuple(asset_type, asset_tag, asset_url)
    """
    return [
        Asset(
            get_asset_type(asset_tag),
            asset_tag,
            asset_tag[ASSET_ATTR[get_asset_type(asset_tag)]],
        )
        for asset_tag in parsed_html.find_all([asset_type.value for asset_type in AssetType])
    ]