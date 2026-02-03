"""
Unit tests for exporter cleanup safety.
"""

import os
import pathlib

import pytest

from rdocgen.exporter import _find_protected_entries, _safe_clean


def test_find_protected_entries_marks_hidden_and_non_md(tmp_path: pathlib.Path) -> None:
    (tmp_path / ".git").mkdir()
    (tmp_path / "notes.txt").write_text("x", encoding="utf-8")
    (tmp_path / "ok.md").write_text("ok", encoding="utf-8")

    protected = _find_protected_entries(str(tmp_path))

    assert ".git" in protected
    assert "notes.txt" in protected
    assert "ok.md" not in protected


def test_safe_clean_blocks_protected_without_force(tmp_path: pathlib.Path) -> None:
    (tmp_path / ".hidden").write_text("x", encoding="utf-8")

    with pytest.raises(RuntimeError):
        _safe_clean(str(tmp_path), force=False, dry_run=False)


def test_safe_clean_deletes_only_contents(tmp_path: pathlib.Path) -> None:
    (tmp_path / "a.md").write_text("x", encoding="utf-8")
    (tmp_path / "b.mdx").write_text("y", encoding="utf-8")

    _safe_clean(str(tmp_path), force=False, dry_run=False)

    assert list(tmp_path.iterdir()) == []


def test_safe_clean_symlink_outdir(tmp_path: pathlib.Path) -> None:
    target = tmp_path / "target"
    target.mkdir()
    (target / "keep.md").write_text("x", encoding="utf-8")
    link = tmp_path / "out"

    try:
        os.symlink(target, link)
    except (OSError, NotImplementedError):  # pragma: no cover - platform-dependent
        pytest.skip("symlink not supported")

    with pytest.raises(RuntimeError):
        _safe_clean(str(link), force=False, dry_run=False)

    _safe_clean(str(link), force=True, dry_run=False)

    assert not link.exists()
    assert (target / "keep.md").exists()
