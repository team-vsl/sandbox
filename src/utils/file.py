from datetime import datetime
from pathlib import Path
import os


def write_to_file(filename: str, content: str, base_dir: str = ".") -> Path:
    """
    Writes the given content to a timestamped YAML file inside a draft folder.

    Args:
        filename (str): Desired filename without extension.
        content (str): Text content to write.
        base_dir (str): Base output directory (default is current directory).

    Returns:
        Path: Absolute path to the written file.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder = Path(base_dir)
    folder.mkdir(parents=True, exist_ok=True)

    file_path = folder / f"{filename}-{timestamp}.yaml"

    try:
        with file_path.open("w", encoding="utf-8") as file:
            file.write(content)
    except Exception as e:
        raise RuntimeError(f"Failed to write to {file_path}: {e}")

    return file_path.resolve()
