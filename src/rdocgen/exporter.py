"""
Filesystem exporter that writes rendered docs to disk.
"""

import os
import shutil

from .config import ExportOptions
from .model import FileDoc, ProjectDoc
from .render.markdown import MarkdownRenderer


def _safe_clean(
    outdir: str,  # directory to clean
    *,
    force: bool,  # allow deleting protected directories
    dry_run: bool,  # report without deleting
) -> None:
    if not os.path.exists(outdir):
        return
    protected = {".git", ".hg", ".svn"}
    if not force and not dry_run:
        for name in protected:
            if os.path.exists(os.path.join(outdir, name)):
                raise RuntimeError(
                    f"Refusing to delete protected directory {name} in {outdir}. "
                    "Re-run with --force to allow this."
                )
    if dry_run:
        print(f"[dry-run] delete directory: {outdir}")
        return
    shutil.rmtree(outdir)


def export_project(
    project: ProjectDoc,  # parsed project tree to export
    outdir: str,  # output directory
    options: ExportOptions,  # render/export configuration
) -> None:
    """Write a ProjectDoc to disk using the configured renderer."""
    renderer = MarkdownRenderer(options.render)

    if options.clean:
        _safe_clean(outdir, force=options.force, dry_run=options.dry_run)
    if options.dry_run:
        print(f"[dry-run] create directory: {outdir}")
        print(
            f"[dry-run] write file: {os.path.join(outdir, f'index{options.render.extension}')}"
        )
    else:
        os.makedirs(outdir, exist_ok=True)

    index_path = os.path.join(outdir, f"index{options.render.extension}")
    if not options.dry_run:
        with open(index_path, "w", encoding="utf-8") as fout:
            fout.write(
                renderer.project_index(
                    project,
                    include_module_links=not options.render.flatten,
                )
            )

    if options.render.flatten:
        if options.dry_run:
            print(f"[dry-run] append to file: {index_path}")
            return
        with open(index_path, "a", encoding="utf-8") as fout:
            for module in project.modules:
                fout.write(f"\n## Module: `{module.name}`\n\n")
                for file_doc in module.files:
                    fout.write(renderer.file_doc(file_doc, heading_level=3))
        return

    modules_dir = os.path.join(outdir, "modules")
    if options.dry_run:
        print(f"[dry-run] create directory: {modules_dir}")
    else:
        os.makedirs(modules_dir, exist_ok=True)

    for module in project.modules:
        module_dir = os.path.join(modules_dir, *module.name.split("."))
        if options.dry_run:
            print(f"[dry-run] create directory: {module_dir}")
        else:
            os.makedirs(module_dir, exist_ok=True)
        module_index = os.path.join(module_dir, f"index{options.render.extension}")
        if options.dry_run:
            print(f"[dry-run] write file: {module_index}")
        else:
            with open(module_index, "w", encoding="utf-8") as fout:
                fout.write(renderer.module_index(module))

        for file_doc in module.files:
            relpath = renderer.file_output_relpath(file_doc, module.name)
            file_path = os.path.join(
                module_dir,
                f"{relpath}{options.render.extension}",
            )
            if options.dry_run:
                print(f"[dry-run] create directory: {os.path.dirname(file_path)}")
                print(f"[dry-run] write file: {file_path}")
            else:
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "w", encoding="utf-8") as fout:
                    fout.write(renderer.file_doc(file_doc))


def export_single_file(
    file_doc: FileDoc,  # parsed file doc to export
    outdir: str,  # output directory
    options: ExportOptions,  # render/export configuration
) -> None:
    """Write a single FileDoc into one output file without indexes."""
    renderer = MarkdownRenderer(options.render)

    if options.clean:
        _safe_clean(outdir, force=options.force, dry_run=options.dry_run)
    if options.dry_run:
        print(f"[dry-run] create directory: {outdir}")
        print(
            f"[dry-run] write file: {os.path.join(outdir, f'index{options.render.extension}')}"
        )
    else:
        os.makedirs(outdir, exist_ok=True)

    out_path = os.path.join(outdir, f"index{options.render.extension}")
    if options.dry_run:
        return
    with open(out_path, "w", encoding="utf-8") as fout:
        fout.write(renderer.file_doc(file_doc))
