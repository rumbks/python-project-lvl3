import os
import tempfile
from pathlib import Path

import pytest
import requests
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

URL_STATUS_400 = "https://ru.hexlet.io/400"
URL_STATUS_500 = "https://ru.hexlet.io/500"
URL_TIMEOUT = "https://ru.hexlet.io/timeout"
ERROR_REASON = 'reason'

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


@pytest.mark.usefixtures('set_up_requests_mocks')
def test_successful_download(temporary_directory):
    with temporary_directory as directory:
        path_to_page = Path(download(PAGE_URL, directory))

        assert path_to_page.name == EXPECTED_PAGE_FILENAME
        assert is_same(path_to_page, SIMPLE_HTML_WITH_LOCAL_URLS)

        resources_dir = path_to_page.parent / EXPECTED_RESOURCES_DIR
        assert ilen(resources_dir.iterdir()) == len(EXPECTED_RESOURCES)
        assert resources_dir.exists()
        for resource_filename, expected in EXPECTED_RESOURCES.items():
            assert is_same(resources_dir / resource_filename, expected)


@pytest.mark.usefixtures('set_up_requests_mocks')
def test_error_nonexistent_directory_to_save():
    nonexistent_directory = "/nonexistent"
    with pytest.raises(RuntimeError) as error:
        download(PAGE_URL, nonexistent_directory)
        assert (
            str(error.value)
            == f"Directory {nonexistent_directory} does not exists."
        )


@fixture
def set_up_requests_mocks_errors(requests_mock):
    requests_mock.get(URL_STATUS_400, status_code=400, reason=ERROR_REASON)
    requests_mock.get(URL_STATUS_500, status_code=500, reason=ERROR_REASON)
    requests_mock.get(URL_TIMEOUT, exc=requests.exceptions.Timeout(ERROR_REASON))


@pytest.mark.parametrize(
    ('url', 'exception', 'message'),
    [
        (
            URL_STATUS_400,
            requests.HTTPError,
            f'400 Client Error: {ERROR_REASON} for url: {URL_STATUS_400}',
        ),
        (
            URL_STATUS_500,
            requests.HTTPError,
            f'500 Server Error: {ERROR_REASON} for url: {URL_STATUS_500}',
        ),
        (URL_TIMEOUT, requests.Timeout, ERROR_REASON),
    ],
)
@pytest.mark.usefixtures('set_up_requests_mocks_errors')
def test_http_error(temporary_directory, url, exception, message, caplog):
    with temporary_directory as directory:
        with pytest.raises(exception) as error:
            download(url, directory)
        assert str(error.value) == message

@pytest.mark.usefixtures('set_up_requests_mocks')
def test_file_write_error(temporary_directory):
    with temporary_directory as directory:
        os.chmod(directory, 0o444)
        with pytest.raises(PermissionError) as error:
            download(PAGE_URL, directory)
        assert "Permission denied" in str(error.value)

