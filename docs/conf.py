#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

import django

import sphinx_py3doc_enhanced_theme

sys.path.insert(0, os.path.abspath('../'))
sys.path.insert(0, os.path.abspath('.'))
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

# Extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
    'sphinxcontrib.blockdiag'
]

napoleon_google_docstring = True
napoleon_use_param = True
napoleon_use_ivar = False
napoleon_use_rtype = True
napoleon_include_special_with_doc = False
autosummary_generate = True

# RST support
source_suffix = '.rst'

# Name of master doc
master_doc = 'index'

# General information about the project.
project = 'MUSIC STORE EXERCISE'
copyright = '2017, Saritasa'

author = 'Saritasa'

version = '0.1'

release = '0.1'

language = None

exclude_patterns = []

todo_include_todos = False

# Read the docs theme
html_theme = 'sphinx_py3doc_enhanced_theme'
html_theme_path = [sphinx_py3doc_enhanced_theme.get_html_theme_path()]

html_static_path = []

htmlhelp_basename = 'music_store_exercisedoc'

latex_elements = {}


# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc,
     'Music Store Exercise',
     'MUSIC STORE EXERCISE Documentation',
     [author], 1)
]

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc,
     'Music Store Exercise',
     'MUSIC STORE EXERCISE Documentation',
     author,
     'Music Store Exercise', 'One line description of project.',
     'Miscellaneous'),
]

html_theme_options = {
    'githuburl': 'https://github.com/ionelmc/sphinx-py3doc-enhanced-theme/',
    'bodyfont': '"Lucida Grande",Arial,sans-serif',
    'headfont': '"Lucida Grande",Arial,sans-serif',
    'codefont': '"Deja Vu Sans Mono",consolas,monospace,sans-serif',
    'linkcolor': '#0072AA',
    'visitedlinkcolor': '#6363bb',
    'extrastyling': False,
    'sidebarwide': True

}
pygments_style = 'friendly'

html_context = {
    'css_files': ['_static/custom.css'],
}
