# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
from pathlib import Path

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'pyMAVLinCS'
copyright = '2025-2026, Noah Redon'
author = 'Noah Redon'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',       # Automatic documentation generation from docstrings
    'sphinx.ext.napoleon',      # Support for Google and NumPy style docstrings
    'sphinx_autodoc_typehints'  # Display Python types in function signatures
]

# Add candidate directories to sys.path so Sphinx can locate pyMAVLinCS
current_dir = Path(__file__).resolve().parent
candidates = [
    current_dir.parent.parent / 'pyMAVLinCS',  # Sibling repo: ../pyMAVLinCS
    current_dir.parent / 'pyMAVLinCS',         # Local directory: ./pyMAVLinCS
    current_dir.parent,                        # Repository root
]

for candidate in candidates:
    if candidate.is_dir() and str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

templates_path = ['_templates']
exclude_patterns = []

language = 'en'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
