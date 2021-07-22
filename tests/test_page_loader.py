import tempfile
from pathlib import Path

import pytest
from pytest import fixture

from page_loader import download
from tests.fixtures_paths import SIMPLE_HTML, SIMPLE_HTML_WITH_RESOURCES, IMAGE
from tests.file import is_same, get_content
from funcy import re_find, ilen

PAGE_URL = "https://ru.hexlet.io/courses"
IMAGE_URL = "https://ru.hexlet.io/resources/image.jpeg"

EXPECTED_PAGE_FILENAME = "ru-hexlet-io-courses.html"
EXPECTED_RESOURCES_DIR = "ru-hexlet-io-courses_files"

EXPECTED_IMAGE_FILENAME = "ru-hexlet-io-resources-image.jpeg"
EXPECTED_IMAGE_PATH = f"{EXPECTED_RESOURCES_DIR}/{EXPECTED_IMAGE_FILENAME}"


@fixture
def simple_web_page_content():
    with open(SIMPLE_HTML) as f:
        return f.read()


@fixture
def image_file_content():
    with open(IMAGE, "rb") as f:
        return f.read()


@fixture
def temporary_directory():
    return tempfile.TemporaryDirectory()


def test_successful_download(
    requests_mock,
    temporary_directory,
    simple_web_page_content,
    image_file_content,
):
    requests_mock.get(PAGE_URL, text=simple_web_page_content)
    requests_mock.get(IMAGE_URL, content=image_file_content)
    with temporary_directory as directory:
        path_to_page = Path(download(PAGE_URL, directory))

        assert path_to_page.name == EXPECTED_PAGE_FILENAME
        assert is_same(path_to_page, SIMPLE_HTML_WITH_RESOURCES)

        substituted_image_path = re_find(
            '(?<=img).*src="(.*)(?=">)', get_content(path_to_page)
        )
        assert substituted_image_path == EXPECTED_IMAGE_PATH

        resources_dir = path_to_page.parent / EXPECTED_RESOURCES_DIR
        assert ilen(resources_dir.iterdir()) == 1
        assert resources_dir.exists()
        assert is_same(resources_dir / EXPECTED_IMAGE_FILENAME, IMAGE)


def test_error_nonexistent_directory_to_save(
    requests_mock, temporary_directory, simple_web_page_content
):
    requests_mock.get(PAGE_URL, text=simple_web_page_content)
    nonexistent_directory = "/nonexistent"
    with pytest.raises(RuntimeError) as error:
        download(PAGE_URL, nonexistent_directory)
        assert (
            str(error.value)
            == f"Directory {nonexistent_directory} does not exists."
        )
