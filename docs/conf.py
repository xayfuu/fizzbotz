#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.abspath(".."))
import fizzbotz

master_doc = 'index'

project = 'Fizzbotz'
copyright = '2016, Matthew Martens'

version = release = fizzbotz.version

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.napoleon',
              'sphinx.ext.viewcode'
              ]

primary_domain = 'py'
default_role = 'py:obj'

autodoc_member_order = 'bysource'
autoclass_content = 'both'

autodoc_docstring_signature = False

latex_documents = [
    ('index', 'fizzbotz.tex', u'Fizzbotz Documentation', u'Matthew Martens', 'manual'),
]

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

# On RTD we can't import sphinx_rtd_theme, but it will be applied by
# default anyway.  This block will use the same theme when building locally
# as on RTD.
if not on_rtd:
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
