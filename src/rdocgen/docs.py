from __future__ import annotations

from .config import ExportOptions
from .exporter import export_project
from .project import build_project


def export_docs(codepath: str, outdir: str, options: ExportOptions) -> None:
    """High-level entrypoint: parse sources and export documentation."""
    project = build_project(codepath, options.parse)
    export_project(project, outdir, options)
