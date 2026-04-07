"""
Unit tests for high-level export behavior.
"""

import pathlib

import pytest

from rdocgen.config import ExportOptions
from rdocgen.docs import export_docs
from rdocgen.parser import ParseError


def test_export_docs_raises_for_invalid_single_file(tmp_path: pathlib.Path) -> None:
    source_path = tmp_path / "broken.py"
    outdir = tmp_path / "out"
    source_path.write_text("def broken(:\n    pass\n", encoding="utf-8")

    with pytest.raises(ParseError, match=r"Failed to parse .*broken.py:1:12"):
        export_docs(str(source_path), str(outdir), ExportOptions())

    assert not outdir.exists()
