from pathlib import Path
from typing import Union

from page_loader.logging import logger


def save(
    directory: Path, filename: str, content: Union[str, bytes]
) -> None:
    if not directory.exists():
        error_message = f"Directory {directory} does not exists."
        logger.error(error_message)
        raise RuntimeError(error_message)
    is_bytes = isinstance(content, bytes)
    with open(directory / filename, f"w{'b' if is_bytes else ''}") as file:
        file.write(content)
