from bs4 import BeautifulSoup

from page_loader.assets import Asset, ASSET_ATTR


def parse(page_content: str) -> BeautifulSoup:
    return BeautifulSoup(page_content, features='html.parser')


def change_asset_url(asset: Asset, new_url: str) -> None:
    asset.tag[ASSET_ATTR[asset.type]] = new_url
