from pathlib import Path

from page_loader.path import get_full_path


def write(directory: Path, filename: str, content: str) -> None:
    if not directory.exists():
        raise RuntimeError(f"Directory {directory} does not exists.")
    with open(get_full_path(directory, filename), "w") as file:
        file.write(content)
