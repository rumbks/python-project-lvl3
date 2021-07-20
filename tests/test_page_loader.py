import tempfile
from pathlib import Path

import pytest
from pytest import fixture

from page_loader import download
from tests.fixtures_paths import SIMPLE_HTML, IMAGE
from tests.file import is_same_content, get_content
from funcy import re_find

URL = "https://ru.hexlet.io/courses"

EXPECTED_PAGE_FILENAME = "ru-hexlet-io-courses.html"
EXPECTED_RESOURCES_DIR = "ru-hexlet-io-courses_files"

EXPECTED_IMAGE_FILENAME = "ru-hexlet-io-courses-resources-image.jpeg"
EXPECTED_IMAGE_PATH = f"{EXPECTED_RESOURCES_DIR}/{EXPECTED_IMAGE_FILENAME}"


@fixture
def simple_web_page_content():
    with open(SIMPLE_HTML) as f:
        return f.read()


@fixture
def temporary_directory():
    return tempfile.TemporaryDirectory()


def test_successful_download(
    requests_mock, temporary_directory, simple_web_page_content
):
    requests_mock.get(URL, text=simple_web_page_content)
    with temporary_directory as directory:
        path_to_page = Path(download(URL, directory))

        assert path_to_page.name == EXPECTED_PAGE_FILENAME
        assert is_same_content(path_to_page, SIMPLE_HTML)

        substituted_image_path = re_find('(?<=img src=").*(?=" alt=)', get_content(path_to_page))
        assert substituted_image_path == EXPECTED_IMAGE_PATH

        resources_dir = path_to_page.parent / EXPECTED_RESOURCES_DIR
        assert resources_dir.exists()
        assert is_same_content(resources_dir / EXPECTED_IMAGE_FILENAME, IMAGE)


def test_error_nonexistent_directory_to_save(
    requests_mock, temporary_directory, simple_web_page_content
):
    requests_mock.get(URL, text=simple_web_page_content)
    nonexistent_directory = "/nonexistent"
    with pytest.raises(RuntimeError) as error:
        download(URL, nonexistent_directory)
        assert str(error.value) == f"Directory {nonexistent_directory} does not exists."
