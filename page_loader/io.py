from pathlib import Path


def write(directory: Path, filename: str, content: str) -> None:
    if not directory.exists():
        raise RuntimeError(f"Directory {directory} does not exists.")
    with open(directory / filename, "w") as file:
        file.write(content)
