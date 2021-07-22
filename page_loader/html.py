from typing import Tuple, List, NamedTuple

from bs4 import BeautifulSoup, Tag


def parse(page_content: str) -> BeautifulSoup:
    return BeautifulSoup(page_content, features='html.parser')


Image = NamedTuple("Image", [('tag', Tag), ('url', str)])

IMG_URL_ATTR = 'src'


def get_images(parsed_html: BeautifulSoup) -> List[Image]:
    """
    :param parsed_html: parsed content of html page
    :return: tuple(img_tag, img_relative_url)
    """
    IMG = 'img'
    return [
        Image(img_tag, img_tag[IMG_URL_ATTR])
        for img_tag in parsed_html.find_all(IMG)
    ]


def change_url(img: Image, new_url: str) -> None:
    img.tag[IMG_URL_ATTR] = new_url
