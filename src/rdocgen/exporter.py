from __future__ import annotations

import os
import shutil

from .config import ExportOptions
from .model import ProjectDoc
from .render.markdown import MarkdownRenderer


def export_project(
    project: ProjectDoc,  # parsed project tree to export
    outdir: str,  # output directory
    options: ExportOptions,  # render/export configuration
) -> None:
    """Write a ProjectDoc to disk using the configured renderer."""
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

        if options.render.split != "off":
            class_dir = os.path.join(module_dir, "classes")
            func_dir = os.path.join(module_dir, "functions")
            enum_dir = os.path.join(module_dir, "enums")
            os.makedirs(class_dir, exist_ok=True)
            os.makedirs(func_dir, exist_ok=True)
            os.makedirs(enum_dir, exist_ok=True)

            for file_doc in module.files:
                for cls in renderer.filter_items(file_doc.classes, "class"):
                    rel = renderer.item_output_relpath(file_doc, module.name, cls.name)
                    out_path = os.path.join(
                        class_dir, f"{rel}{options.render.extension}"
                    )
                    os.makedirs(os.path.dirname(out_path), exist_ok=True)
                    with open(out_path, "w", encoding="utf-8") as fout:
                        fout.write(renderer.class_doc(cls))

                for func in renderer.filter_items(file_doc.functions, "function"):
                    rel = renderer.item_output_relpath(file_doc, module.name, func.name)
                    out_path = os.path.join(
                        func_dir, f"{rel}{options.render.extension}"
                    )
                    os.makedirs(os.path.dirname(out_path), exist_ok=True)
                    with open(out_path, "w", encoding="utf-8") as fout:
                        fout.write(renderer.function_doc(func))

                for enm in renderer.filter_items(file_doc.enums, "enum"):
                    rel = renderer.item_output_relpath(file_doc, module.name, enm.name)
                    out_path = os.path.join(
                        enum_dir, f"{rel}{options.render.extension}"
                    )
                    os.makedirs(os.path.dirname(out_path), exist_ok=True)
                    with open(out_path, "w", encoding="utf-8") as fout:
                        fout.write(renderer.enum_doc(enm))
            if options.render.split == "only":
                continue

        for file_doc in module.files:
            relpath = renderer.file_output_relpath(file_doc, module.name)
            file_path = os.path.join(
                module_dir,
                f"{relpath}{options.render.extension}",
            )
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as fout:
                fout.write(renderer.file_doc(file_doc))
