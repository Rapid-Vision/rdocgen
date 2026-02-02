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
        file_doc = None
        if project.modules and project.modules[0].files:
            file_doc = project.modules[0].files[0]
        if file_doc is None:
            if Path(outdir).exists() and options.clean:
                from .exporter import _safe_clean

                _safe_clean(outdir, force=options.force, dry_run=options.dry_run)
            if options.dry_run:
                if not Path(outdir).exists():
                    print(f"[dry-run] create directory: {outdir}")
                out_path = Path(outdir) / f"index{options.render.extension}"
                print(f"[dry-run] write file: {out_path}")
            else:
                Path(outdir).mkdir(parents=True, exist_ok=True)
                out_path = Path(outdir) / f"index{options.render.extension}"
                out_path.write_text("_No content found._\n", encoding="utf-8")
        else:
            export_single_file(file_doc=file_doc, outdir=outdir, options=options)
        return
    export_project(project, outdir, options)
