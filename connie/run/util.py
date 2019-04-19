from pathlib import Path
from typing import Sequence, Optional


def search_path(fname: Path, search_paths: Sequence[Path]) -> Optional[Path]:
    if fname.is_absolute():
        if fname.exists():
            return fname
    else:
        for base in search_paths:
            search = base / fname
            if search.is_file():
                return search
    return None

