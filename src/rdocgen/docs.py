"""
High-level export API for rdocgen.
"""

from pathlib import Path

from .config import ExportOptions
from .exporter import export_project, export_single_file
from .project import build_project


def export_docs(
    codepath: str,  # file or directory path to parse
    outdir: str,  # output directory
    options: ExportOptions,  # parse/render/export configuration
) -> None:
    """High-level entrypoint: parse sources and export documentation."""
    project = build_project(codepath, options.parse)
    if Path(codepath).is_file():
        if not project.modules or not project.modules[0].files:
            raise RuntimeError(f"No documentation content found in {codepath}")
        file_doc = project.modules[0].files[0]
        export_single_file(file_doc=file_doc, outdir=outdir, options=options)
        return
    export_project(project, outdir, options)
