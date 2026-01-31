from __future__ import annotations

import fnmatch
import os
from pathlib import Path
from typing import Iterable, Optional

from .config import ParseOptions


def iter_python_files(root: Path, options: ParseOptions) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root, followlinks=options.follow_symlinks):
        dir_path = Path(dirpath)
        if any(part.startswith(".") for part in dir_path.parts):
            dirnames[:] = []
            continue
        if "__pycache__" in dir_path.parts:
            dirnames[:] = []
            continue
        if ".venv" in dir_path.parts or "venv" in dir_path.parts:
            dirnames[:] = []
            continue
        if "dist" in dir_path.parts or "build" in dir_path.parts:
            dirnames[:] = []
            continue

        for filename in filenames:
            if not filename.endswith(".py"):
                continue
            path = dir_path / filename
            if not path_allowed(path, root, options):
                continue
            yield path


def module_name_from_path(
    path: Path, root: Optional[Path] = None, depth: Optional[int] = None
) -> str:
    base = path
    if root is not None:
        try:
            base = path.relative_to(root)
        except ValueError:
            base = path
    parts = list(base.with_suffix("").parts)
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    if depth is not None and depth > 0:
        parts = parts[:depth]
    return ".".join(parts)


def path_allowed(path: Path, root: Path, options: ParseOptions) -> bool:
    relative = path
    try:
        relative = path.relative_to(root)
    except ValueError:
        relative = path
    rel_str = relative.as_posix()
    if options.include_paths:
        if not any(fnmatch.fnmatch(rel_str, pattern) for pattern in options.include_paths):
            return False
    if options.exclude_paths:
        if any(fnmatch.fnmatch(rel_str, pattern) for pattern in options.exclude_paths):
            return False
    return True
