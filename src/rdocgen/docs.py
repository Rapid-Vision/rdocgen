"""
High-level export API for rdocgen.
"""

from .config import ExportOptions
from .exporter import export_project
from .project import build_project


def export_docs(
    codepath: str,  # file or directory path to parse
    outdir: str,  # output directory
    options: ExportOptions,  # parse/render/export configuration
) -> None:
    """High-level entrypoint: parse sources and export documentation."""
    project = build_project(codepath, options.parse)
    export_project(project, outdir, options)
