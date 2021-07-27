from typing import List, NamedTuple
from urllib.parse import urlparse

from bs4 import BeautifulSoup, Tag


def parse(page_content: str) -> BeautifulSoup:
    return BeautifulSoup(page_content, features='html.parser')


Resource = NamedTuple("Resource", [('tag', Tag), ('url', str)])

IMG_URL_ATTR = 'src'


def get_images(parsed_html: BeautifulSoup) -> List[Resource]:
    """
    :param parsed_html: parsed content of html page
    :return: tuple(img_tag, img_relative_url)
    """
    IMG = 'img'
    return [
        Resource(img_tag, img_tag[IMG_URL_ATTR])
        for img_tag in parsed_html.find_all(IMG)
    ]


def in_same_domain(root_page_url: str, resource: Resource) -> bool:
    root_page_url = urlparse(root_page_url)
    resource_url = urlparse(resource.url)

    return not resource_url.netloc or resource_url.netloc == root_page_url.netloc


def change_resource_url(img: Resource, new_url: str) -> None:
    img.tag[IMG_URL_ATTR] = new_url
