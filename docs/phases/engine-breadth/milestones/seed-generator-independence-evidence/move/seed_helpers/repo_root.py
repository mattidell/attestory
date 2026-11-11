"""Find the repository root without embedding a machine path."""

from __future__ import annotations

from pathlib import Path


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "packages" / "kernel" / "__init__.py").is_file() and (
            parent / "tests"
        ).is_dir():
            return parent
    raise RuntimeError("repository root not found")
