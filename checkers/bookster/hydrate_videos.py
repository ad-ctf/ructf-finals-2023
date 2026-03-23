#!/usr/bin/env python3

from pathlib import Path
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parent
VIDEOS_DIR = ROOT / "videos"
UPSTREAM = "https://media.githubusercontent.com/media/HackerDom/ructf-finals-2023/master/checkers/bookster/videos"


def is_lfs_pointer(path: Path) -> bool:
    try:
        with path.open("rb") as fh:
            return fh.readline().startswith(b"version https://git-lfs.github.com/spec/v1")
    except OSError:
        return False


def hydrate(path: Path) -> None:
    target = VIDEOS_DIR / path.name
    if target.exists() and not is_lfs_pointer(target):
        return

    with urlopen(f"{UPSTREAM}/{path.name}") as response:
        data = response.read()

    tmp = target.with_suffix(target.suffix + ".tmp")
    tmp.write_bytes(data)
    tmp.replace(target)


def main() -> int:
    for sample in sorted(VIDEOS_DIR.glob("sample_*.avi")):
        hydrate(sample)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
