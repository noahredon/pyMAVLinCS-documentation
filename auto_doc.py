#!/usr/bin/env python3
"""
pyMAVLinCS Documentation Generator
==================================

Automates Sphinx documentation generation for pyMAVLinCS.

Key capabilities:
1. Merges class docstrings with their `__init__` docstrings (Args, Returns, Notes, etc.)
   so that class constructors are documented seamlessly in Sphinx.
2. Formats `Returns:` sections into Sphinx-compatible bold/italic markup.
3. Automatically locates the `pyMAVLinCS` source files across sibling or local paths.
4. Uses a safe in-memory context manager to guarantee original files are restored
   even if Sphinx encounters an error or is interrupted.
5. Invokes Sphinx build using the active Python environment.
6. Automatically creates the `.nojekyll` file required for GitHub Pages.
"""

from __future__ import annotations

import argparse
import ast
from contextlib import contextmanager
import os
from pathlib import Path
import re
import subprocess
import sys
import textwrap

BLOCK_KEYWORDS = ("Args:", "Returns:", "Raises:", "Note:", "Notes:", "Examples:")

TARGET_MODULE_FILES = (
    "__init__.py",
    "mavecstra.py",
    "mavtypes.py",
    "mission_control_code.py",
    "setup_logger.py",
)


def merge_class_and_init_docstrings(source_code: str) -> str:
    """
    Parses Python source code and merges class docstrings with their __init__ docstring.
    Transfers Args, Returns, Notes, and Examples blocks into the class header docstring.
    """
    tree = ast.parse(source_code)
    lines = source_code.split("\n")
    n_insert = 0

    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue

        class_doc = ast.get_docstring(node, clean=False)
        init_doc = None
        for item in node.body:
            if isinstance(item, ast.FunctionDef) and item.name == "__init__":
                init_doc = ast.get_docstring(item, clean=False)
                break

        if init_doc is None:
            continue

        if not class_doc:
            new_doc = init_doc.strip()
        else:
            class_main = textwrap.dedent(class_doc).rstrip()
            init_lines = textwrap.dedent(init_doc).splitlines()

            start_copy = False
            blocks_to_add = []
            for line in init_lines:
                stripped = line.lstrip()
                if not start_copy:
                    if any(stripped.startswith(k) for k in BLOCK_KEYWORDS):
                        start_copy = True
                if start_copy:
                    blocks_to_add.append(line[4:] if line.startswith("    ") else line)

            blocks_text = "\n".join(blocks_to_add).rstrip()
            new_doc = (class_main + "\n\n" + blocks_text).strip() if blocks_text else class_main.strip()

        # Replace existing class docstring or insert new docstring
        if (node.body and isinstance(node.body[0], ast.Expr)
                and isinstance(node.body[0].value, ast.Constant)
                and isinstance(node.body[0].value.value, str)):
            first_stmt = node.body[0]
            doc_lineno = first_stmt.lineno - 1 + n_insert
            doc_col = first_stmt.col_offset
            indent = " " * doc_col
            old_doc_lines = first_stmt.value.value.splitlines()

            new_doc_lines = [indent + '"""'] + [indent + l for l in new_doc.splitlines()] + [indent + '"""']
            corrected_lines = []
            for line in new_doc_lines:
                stripped_line = line.lstrip()
                actual_indent = len(line) - len(stripped_line)
                if actual_indent > len(indent):
                    line = line[4:]
                corrected_lines.append(line)

            lines[doc_lineno : doc_lineno + len(old_doc_lines)] = corrected_lines
            n_insert += len(corrected_lines) - len(old_doc_lines)
        else:
            class_line = lines[node.lineno - 1 + n_insert]
            indent = re.match(r"^(\s*)", class_line).group(1) + "    "
            new_doc_lines = [indent + '"""'] + [indent + l for l in new_doc.splitlines()] + [indent + '"""']
            corrected_lines = []
            for line in new_doc_lines:
                stripped_line = line.lstrip()
                actual_indent = len(line) - len(stripped_line)
                if actual_indent > len(indent):
                    line = line[8:]
                corrected_lines.append(line)

            lines[node.lineno + n_insert : node.lineno + n_insert] = corrected_lines
            n_insert += len(corrected_lines)

    return "\n".join(lines)


def format_returns_block(source_code: str) -> str:
    """
    Transforms lines in 'Returns:' docstring blocks:
    '- var (type): description' -> '- **var** (*type*) – description'
    """
    lines = source_code.split("\n")
    transformed_lines = []
    in_returns_block = False

    pattern = re.compile(r"^(\s*)- (\S+) \((.+?)\): (.+)")
    section_pattern = re.compile(r"^\s*(\w+):")

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("Returns:"):
            in_returns_block = True
            transformed_lines.append(line)
            continue

        if in_returns_block and section_pattern.match(stripped):
            in_returns_block = False

        if in_returns_block:
            match = pattern.match(line)
            if match:
                indent, var_name, var_type, description = match.groups()
                line = f"{indent}- **{var_name}** (*{var_type}*) – {description}"

        transformed_lines.append(line)

    return "\n".join(transformed_lines)


def transform_python_file_content(source_code: str) -> str:
    """
    Applies both docstring merging and returns block formatting.
    """
    with_merged_docstrings = merge_class_and_init_docstrings(source_code)
    return format_returns_block(with_merged_docstrings)


@contextmanager
def temporary_transform_files(files: list[Path]):
    """
    Temporarily applies docstring transformations to Python files in-memory,
    guaranteeing that the original content is safely restored upon exit.
    """
    backups: dict[Path, str] = {}
    try:
        print("[*] Backing up original files and applying docstring transformations...")
        for file_path in files:
            original_content = file_path.read_text(encoding="utf-8")
            backups[file_path] = original_content
            transformed_content = transform_python_file_content(original_content)
            file_path.write_text(transformed_content, encoding="utf-8")
            print(f"    - Transformed: {file_path.name}")
        yield
    finally:
        print("[*] Restoring original Python source files...")
        for file_path, original_content in backups.items():
            file_path.write_text(original_content, encoding="utf-8")
            print(f"    - Restored: {file_path.name}")
        print("[+] All original source files have been safely restored.")


def find_package_directory(custom_path: Path | None = None) -> Path:
    """
    Locates the pyMAVLinCS package directory.
    Checks custom path, local directory, sibling directory, or parent directory.
    """
    if custom_path:
        target = custom_path.resolve()
        if (target / "__init__.py").is_file():
            return target
        if (target / "pyMAVLinCS" / "__init__.py").is_file():
            return target / "pyMAVLinCS"
        raise FileNotFoundError(f"Could not locate pyMAVLinCS in specified path: {custom_path}")

    # Search candidate paths
    repo_root = Path(__file__).resolve().parent
    candidates = [
        repo_root / "pyMAVLinCS",
        repo_root.parent / "pyMAVLinCS" / "pyMAVLinCS",
        repo_root.parent / "pyMAVLinCS",
    ]

    for candidate in candidates:
        if (candidate / "__init__.py").is_file():
            return candidate.resolve()

    raise FileNotFoundError(
        "Could not automatically locate the pyMAVLinCS package directory.\n"
        "Please specify it with: python auto_doc.py --source-dir <path/to/pyMAVLinCS>"
    )


def build_sphinx_docs(docs_root: Path, builder: str = "html") -> None:
    """
    Runs the Sphinx build command using the current Python environment.
    """
    source_dir = docs_root / "source"
    build_dir = docs_root / "build" / builder

    print(f"[*] Building Sphinx documentation ({builder})...")
    cmd = [
        sys.executable,
        "-m",
        "sphinx",
        "-b",
        builder,
        str(source_dir),
        str(build_dir),
    ]

    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        raise RuntimeError(f"Sphinx build failed with exit code {result.returncode}")

    # Ensure .nojekyll exists for GitHub Pages compatibility
    nojekyll_file = docs_root / "build" / "html" / ".nojekyll"
    if not nojekyll_file.exists():
        nojekyll_file.touch()
        print("[+] Ensured .nojekyll exists in build/html")

    print(f"[SUCCESS] Documentation built successfully in: {build_dir}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="pyMAVLinCS Sphinx Documentation Generator with automatic docstring merging."
    )
    parser.add_argument(
        "-s", "--source-dir",
        type=Path,
        default=None,
        help="Path to the pyMAVLinCS package directory containing the Python source files."
    )
    parser.add_argument(
        "-b", "--builder",
        default="html",
        help="Sphinx builder to use (default: html)."
    )
    args = parser.parse_args()

    docs_root = Path(__file__).resolve().parent

    try:
        package_dir = find_package_directory(args.source_dir)
        print(f"[+] Located pyMAVLinCS package at: {package_dir}")

        target_files = [package_dir / filename for filename in TARGET_MODULE_FILES]
        existing_files = [f for f in target_files if f.is_file()]

        if not existing_files:
            print(f"[ERROR] No target Python files found in {package_dir}", file=sys.stderr)
            return 1

        with temporary_transform_files(existing_files):
            build_sphinx_docs(docs_root=docs_root, builder=args.builder)

        return 0

    except Exception as exc:
        print(f"\n[ERROR] Build interrupted: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
