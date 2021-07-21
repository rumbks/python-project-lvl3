from funcy import cut_prefix
from urllib.parse import urlparse


def without_schema(url: str) -> str:
    HTTP = 'http://'
    HTTPS = 'https://'
    if url.startswith(HTTP):
        return cut_prefix(url, HTTP)
    return cut_prefix(url, HTTPS)


def get_domain_name(url: str) -> str:
    parsed = urlparse(url)
    return parsed.netloc

