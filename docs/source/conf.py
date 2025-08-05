# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Python para estudiantes de computación'
copyright = '2025, José Mario García Valdez'
author = 'José Mario García Valdez'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinxcontrib.bibtex',]
bibtex_bibfiles = ['biblio.bib']

templates_path = ['_templates']
exclude_patterns = []

language = 'es'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_book_theme'
#html_theme = 'furo'
html_static_path = ['_static']
html_title = 'Python para estudiantes de computación'


rinoh_documents = [
        dict(
            doc='index',  # top-level file (e.g., index.rst)
            target='my-document',  # output file (e.g., my-document.pdf),
            template='rino.rtt'
        ),
    ]

latex_elements = {
    "releasename": "",
    "tableofcontents": "",
    "maketitle": "",
}