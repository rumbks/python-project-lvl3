from funcy import cut_prefix
from urllib.parse import urlparse, urljoin


def to_absolute_url(root_page_url: str, relative_url: str) -> str:
    return urljoin(root_page_url, relative_url)


def without_schema(url: str) -> str:
    HTTP = 'http://'
    HTTPS = 'https://'
    if url.startswith(HTTP):
        return cut_prefix(url, HTTP)
    return cut_prefix(url, HTTPS)


def get_domain_name(url: str) -> str:
    parsed = urlparse(url)
    return parsed.netloc

