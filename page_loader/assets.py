from typing import List, NamedTuple, Optional
from urllib.parse import urlparse

from bs4 import BeautifulSoup, Tag
from funcy import lkeep


ASSET_TAG_NAMES = ('img', 'link', 'script')

Asset = NamedTuple(
    "Asset", [('tag', Tag), ('url', str)]
)


TAG_LINK_ATTR_NAME = {
    'img': 'src',
    'link': 'href',
    'script': 'src'
}


def in_same_domain(root_page_url: str, asset: Asset) -> bool:
    root_page_url = urlparse(root_page_url)
    asset_url = urlparse(asset.url)

    return not asset_url.netloc or asset_url.netloc == root_page_url.netloc


def get_asset(asset_tag: Tag) -> Optional[Asset]:
    """Returns None if tag contains inline script"""
    url = asset_tag.get(TAG_LINK_ATTR_NAME[asset_tag.name], None)
    if url is None:
        return None
    return Asset(asset_tag, url)


def get_assets(parsed_html: BeautifulSoup) -> List[Asset]:
    """
    :param parsed_html: parsed content of html page
    :return: tuple(asset_type, asset_tag, asset_url)
    """
    return lkeep(
        get_asset(asset_tag)
        for asset_tag in parsed_html.find_all(
            ASSET_TAG_NAMES
        )
    )
