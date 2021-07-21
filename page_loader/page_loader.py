import shutil
from pathlib import Path
from typing import Union

import requests

from page_loader.io import write
from page_loader import html
from page_loader.path import (
    get_page_filename,
    get_assets_folder_name,
    get_asset_filename,
)
from page_loader.url import get_domain_name


def download(url: str, save_to: Union[str, Path] = None) -> str:
    save_to = Path.cwd() if save_to is None else Path(save_to)
    if not save_to.exists():
        raise RuntimeError(f"Directory {save_to} does not exists.")
    response = requests.get(url)
    page_filename = get_page_filename(url)
    assets_directory = save_to / get_assets_folder_name(url)
    assets_directory.mkdir(exist_ok=True)

    parsed_content = html.parse(response.text)

    domain_name = get_domain_name(url)
    for img_tag in parsed_content.find_all('img'):
        img_url = img_tag['src']
        img_full_url = f"https://{domain_name}{img_url}"
        img_response = requests.get(img_full_url)
        asset_filename = get_asset_filename(img_url, domain_name)
        with open(assets_directory / asset_filename, 'wb') as file:
            file.write(img_response.content)
        img_tag['src'] = str(Path(assets_directory.name) / asset_filename)

    write(
        directory=save_to,
        filename=page_filename,
        content=parsed_content.prettify(formatter='html5'),
    )
    return str(save_to / page_filename)
