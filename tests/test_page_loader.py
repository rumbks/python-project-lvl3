import tempfile
from pathlib import Path

import pytest
from funcy import ilen
from pytest import fixture

from page_loader import download
from tests.file import is_same, get_content
from tests.fixtures_paths import (
    SIMPLE_HTML,
    SIMPLE_HTML_WITH_LOCAL_URLS,
    IMAGE,
    SCRIPT,
    CSS,
)

PAGE_URL = "https://ru.hexlet.io/courses"
IMAGE_URL = "https://ru.hexlet.io/assets/image.jpeg"
CSS_URL = "https://ru.hexlet.io/assets/application.css"
SCRIPT_URL = "https://ru.hexlet.io/packs/js/runtime.js"

EXPECTED_RESOURCES_DIR = "ru-hexlet-io-courses_files"

EXPECTED_PAGE_FILENAME = "ru-hexlet-io-courses.html"
EXPECTED_IMAGE_FILENAME = "ru-hexlet-io-assets-image.jpeg"
EXPECTED_CSS_FILENAME = "ru-hexlet-io-assets-application.css"
EXPECTED_SCRIPT_FILENAME = "ru-hexlet-io-packs-js-runtime.js"

# mapping from expected resources filenames to paths to their expected content
EXPECTED_RESOURCES = {
    EXPECTED_IMAGE_FILENAME: IMAGE,
    EXPECTED_CSS_FILENAME: CSS,
    EXPECTED_SCRIPT_FILENAME: SCRIPT,
    EXPECTED_PAGE_FILENAME: SIMPLE_HTML
}


@fixture
def temporary_directory():
    return tempfile.TemporaryDirectory()


@fixture
def set_up_requests_mocks(requests_mock):
    requests_mock.get(PAGE_URL, text=get_content(SIMPLE_HTML))
    requests_mock.get(IMAGE_URL, content=get_content(IMAGE, bytes=True))
    requests_mock.get(CSS_URL, text=get_content(CSS))
    requests_mock.get(SCRIPT_URL, text=get_content(SCRIPT))


def test_successful_download(
    set_up_requests_mocks,
    temporary_directory,
):
    with temporary_directory as directory:
        path_to_page = Path(download(PAGE_URL, directory))

        assert path_to_page.name == EXPECTED_PAGE_FILENAME
        assert is_same(path_to_page, SIMPLE_HTML_WITH_LOCAL_URLS)

        resources_dir = path_to_page.parent / EXPECTED_RESOURCES_DIR
        assert ilen(resources_dir.iterdir()) == len(EXPECTED_RESOURCES)
        assert resources_dir.exists()
        for resource_filename, expected in EXPECTED_RESOURCES.items():
            assert is_same(resources_dir / resource_filename, expected)


def test_error_nonexistent_directory_to_save(set_up_requests_mocks):
    nonexistent_directory = "/nonexistent"
    with pytest.raises(RuntimeError) as error:
        download(PAGE_URL, nonexistent_directory)
        assert (
            str(error.value)
            == f"Directory {nonexistent_directory} does not exists."
        )
