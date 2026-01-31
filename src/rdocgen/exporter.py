from __future__ import annotations

import os
import shutil

from .config import ExportOptions
from .model import ProjectDoc
from .render.markdown import MarkdownRenderer


def export_project(project: ProjectDoc, outdir: str, options: ExportOptions) -> None:
    renderer = MarkdownRenderer(options.render)

    if os.path.exists(outdir) and options.clean:
        shutil.rmtree(outdir)
    os.makedirs(outdir, exist_ok=True)

    index_path = os.path.join(outdir, f"index{options.render.extension}")
    with open(index_path, "w", encoding="utf-8") as fout:
        fout.write(renderer.project_index(project))

    if options.render.flatten:
        with open(index_path, "a", encoding="utf-8") as fout:
            for module in project.modules:
                fout.write(f"\n## Module: `{module.name}`\n\n")
                for file_doc in module.files:
                    fout.write(renderer.file_doc(file_doc, heading_level=3))
        return

    modules_dir = os.path.join(outdir, "modules")
    os.makedirs(modules_dir, exist_ok=True)

    for module in project.modules:
        module_dir = os.path.join(modules_dir, *module.name.split("."))
        os.makedirs(module_dir, exist_ok=True)
        module_index = os.path.join(module_dir, f"index{options.render.extension}")
        with open(module_index, "w", encoding="utf-8") as fout:
            fout.write(renderer.module_index(module))

        for file_doc in module.files:
            relpath = renderer.file_output_relpath(file_doc, module.name)
            file_path = os.path.join(
                module_dir,
                f"{relpath}{options.render.extension}",
            )
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as fout:
                fout.write(renderer.file_doc(file_doc))
