from pathlib import Path
from typing import Union


def get_extension(path_to_file: Union[Path, str]):
    return Path(path_to_file).suffix


def is_img(path_to_file: Union[Path, str]):
    IMG_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif']
    return get_extension(path_to_file) in IMG_EXTENSIONS


def get_content(path_to_file, bytes=False):
    with open(path_to_file, f'r{"b" if bytes else ""}') as f:
        return f.read()


def is_same(path_to_file1, path_to_file2):
    if not get_extension(path_to_file1) == get_extension(path_to_file2):
        return False
    are_images = is_img(path_to_file1)
    # page = get_content(path_to_file1)
    # expected = get_content(path_to_file2)
    return get_content(path_to_file1, bytes=are_images) == get_content(
        path_to_file2, bytes=are_images
    )
