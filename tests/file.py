from pathlib import Path
from typing import Union


def get_content(
    path_to_file: Union[Path, str], *, bytes: bool = False
) -> Union[str, bytes]:
    with open(path_to_file, f'r{"b" if bytes else ""}') as f:
        return f.read()
