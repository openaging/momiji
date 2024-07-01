# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information


import os
import sys
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../momiji'))


project = 'momiji'
copyright = '2024, openaging'
author = 'openaging <open.aging.info@gmail.com>'
release = '0.1.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
    'nbsphinx',
    'sphinx.ext.mathjax',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
html_theme = 'pydata_sphinx_theme'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme_options = {
    "external_links": [
        {"name": "GitHub", "url": "https://github.com/openaging/momiji"}
    ],
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/openaging/momiji",
            "icon": "fab fa-github-square",
        }
    ],
}

html_static_path = ['_static']

# Add this line to set the favicon
html_favicon = '_static/momiji-favicon.ico'

# for notebook
nbsphinx_allow_errors = True
nbsphinx_execute = 'never'
