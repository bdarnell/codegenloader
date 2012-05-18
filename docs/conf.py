# Ensure we get the local copy instead of what's on the standard path
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
import codegenloader

master_doc = "index"

project = "codegenloader"
copyright = "TODO"

version = release = codegenloader.version

extensions = ["sphinx.ext.autodoc", "sphinx.ext.viewcode"]

primary_domain = 'py'
default_role = 'py:obj'

autodoc_member_order = 'bysource'
autoclass_content = 'both'

