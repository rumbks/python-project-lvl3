from pathlib import Path
from typing import Union


def save(
    directory: Path, filename: str, content: Union[str, bytes]
) -> None:
    if not directory.exists():
        raise RuntimeError(f"Directory {directory} does not exists.")
    is_bytes = isinstance(content, bytes)
    with open(directory / filename, f"w{'b' if is_bytes else ''}") as file:
        file.write(content)
