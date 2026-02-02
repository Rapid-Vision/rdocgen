"""
Project builder that groups parsed files into modules.
"""

from pathlib import Path
from typing import List

from .config import ParseOptions
from .discovery import iter_python_files, module_name_from_path, path_allowed
from .model import ModuleDoc, ProjectDoc
from .parser import parse_file


def build_project(
    path: str,  # file path or directory root to parse
    options: ParseOptions,  # traversal and parse behavior
) -> ProjectDoc:
    """Build a ProjectDoc from a file path or a directory root."""
    target = Path(path)
    if target.is_file():
        project = ProjectDoc(name=target.stem, root_path=str(target.resolve()))
        if path_allowed(target, target.parent, options):
            module = ModuleDoc(name=target.stem, path=str(target))
            file_doc = parse_file(
                str(target),
                module_name=target.stem,
                fail_on_parse_error=options.fail_on_parse_error,
            )
            if file_doc is not None:
                module.files.append(file_doc)
                project.modules.append(module)
        return project

    if not target.is_dir():
        raise FileNotFoundError(f"Path not found: {path}")

    project = ProjectDoc(name=target.name, root_path=str(target.resolve()))
    for module in _discover_modules(target, options):
        project.modules.append(module)
    return project


def _discover_modules(
    root: Path,  # root directory being scanned
    options: ParseOptions,  # module grouping and parse behavior
) -> List[ModuleDoc]:
    """Group parsed files into ModuleDoc buckets by module depth."""
    modules: dict[str, ModuleDoc] = {}
    for file_path in iter_python_files(root, options):
        module_name = module_name_from_path(
            file_path, root=root, depth=options.module_depth
        )
        full_module_name = module_name_from_path(file_path, root=root, depth=None)
        group_name = module_name or file_path.stem
        if group_name not in modules:
            modules[group_name] = ModuleDoc(
                name=group_name, path=str(root / group_name)
            )
        file_doc = parse_file(
            str(file_path),
            module_name=full_module_name or file_path.stem,
            fail_on_parse_error=options.fail_on_parse_error,
        )
        if file_doc is None:
            continue
        modules[group_name].files.append(file_doc)
    return sorted(modules.values(), key=lambda m: m.name)
