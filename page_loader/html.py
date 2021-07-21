from bs4 import BeautifulSoup


def parse(page_content: str) -> BeautifulSoup:
    return BeautifulSoup(page_content)
