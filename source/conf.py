# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Networking Down Under'
copyright = '2024, Paul Vincent Craven'
author = 'Paul Vincent Craven'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx_sitemap', 'sphinx_copybutton']

templates_path = ['_templates']
exclude_patterns = []

# Sitemap configuration
html_baseurl = 'https://networking-down-under.readthedocs.io/en/latest/'
sitemap_url_scheme = "{link}"
# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']

numfig = True
html_title = "Networking Down Under"

def setup(app):
  app.add_css_file( "custom.css" )