from bs4 import BeautifulSoup
from page_loader.assets import TAG_LINK_ATTR_NAME, Asset


def parse(page_content: str) -> BeautifulSoup:
    return BeautifulSoup(page_content, features='html.parser')


def change_asset_url(asset: Asset, new_url: str) -> None:
    asset.tag[TAG_LINK_ATTR_NAME[asset.tag.name]] = new_url
