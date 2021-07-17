import tempfile
from pathlib import Path

import pytest
from pytest import fixture

from page_loader import download
from tests.fixtures_paths import SIMPLE_HTML

URL = "https://ru.hexlet.io/courses"

EXPECTED_FILENAME = "ru-hexlet-io-courses.html"

EXPECTED_CONTENT = ""


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
        assert path_to_page.name == EXPECTED_FILENAME
        with open(path_to_page) as f:
            loaded_page = f.read()
            assert loaded_page == simple_web_page_content


def test_error_nonexistent_directory_to_save(
    requests_mock, temporary_directory, simple_web_page_content
):
    requests_mock.get(URL, text=simple_web_page_content)
    nonexistent_directory = "/nonexistent"
    with pytest.raises(RuntimeError) as error:
        download(URL, nonexistent_directory)
        assert str(error.value) == f"Directory {nonexistent_directory} does not exists."
