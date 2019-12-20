# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

from pallets_sphinx_themes import get_version
from pallets_sphinx_themes import ProjectLink

# -- Project information -----------------------------------------------------

project = 'SOtools'
copyright = '2019, Dave Vieglais'
author = 'Dave Vieglais'

# The full version, including alpha/beta/rc tags
release, version = get_version("sotools", version_length=1)


# -- General configuration ---------------------------------------------------
master_doc = "index"

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    #"sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    #"sphinxcontrib.log_cabinet",
    #"sphinx_git",
    "sphinx_issues",
    "pallets_sphinx_themes",
    "sphinx.ext.napoleon",
    "jupyter_sphinx.execute",
    "sphinx.ext.viewcode",
    "sphinx.ext.graphviz",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

issues_github_path = "datadavev/sotools"

jupyter_sphinx_thebelab_config = {
    'requestKernel': True,
    'binderOptions': {
        'repo': "datadavev/sotools",
    },
}

graphviz_output_format = "svg"

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'click'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_theme_options = {"index_sidebar_logo": False}
html_context = {
    "project_links": [
        ProjectLink("Source on GitHub", "https://github.com/datadavev/sotools/"),
        ProjectLink("Issue Tracker", "https://github.com/datadavev/sotools/issues/"),
    ]
}
html_sidebars = {
    "index": ["project.html", "localtoc.html", "searchbox.html"],
    "**": ["localtoc.html", "relations.html", "searchbox.html"],
}
singlehtml_sidebars = {"index": ["project.html", "localtoc.html"]}
html_title = f"SOtools Documentation ({version})"
html_show_sourcelink = False

html_css_files = [
    "css/blf5grc.css",
    "css/custom.css",
]

html_js_files = [
    "js/thebe_status.js",
]

autoclass_content = 'both'

# try to exclude deprecated
def skip_deprecated(app, what, name, obj, skip, options):
    if hasattr(obj, "func_dict") and "__deprecated__" in obj.func_dict:
        print("skipping " + name)
        return True
    return skip or False

def setup(app):
    app.connect('autodoc-skip-member', skip_deprecated)
    try:

        from docutils.statemachine import StringList
        from sphinx.pycode import ModuleAnalyzer, PycodeError
        from sphinx.ext.autosummary import Autosummary
        from sphinx.ext.autosummary import get_documenter
        from docutils.parsers.rst import directives
        from sphinx.util.inspect import safe_getattr
        import re

        class AutoFuncSummary(Autosummary):
            """
            Based on https://github.com/markovmodel/PyEMMA/blob/devel/doc/source/conf.py
            Use it like::
              .. autofuncsummary:: MODULE_NAME
                 :functions:
            to generate a table of functions in a module.
            """

            #option_spec = {
            #    'functions': directives.unchanged,
            #}
            option_spec = Autosummary.option_spec
            option_spec["functions"] = directives.unchanged

            required_arguments = 1

            @staticmethod
            def get_members(obj, typ, include_public=None):
                if not include_public:
                    include_public = []
                items = []
                for name in dir(obj):
                    try:
                        documenter = get_documenter(app, safe_getattr(obj, name), obj)
                        #print(str(documenter))
                    except AttributeError:
                        continue
                    if documenter.objtype == typ:
                        items.append(name)
                public = [x for x in items if x in include_public or not x.startswith('_')]
                return public, items

            def run(self):
                module_name = self.arguments[0]
                from_list = module_name.split(".")[:-1]
                try:
                    m = __import__(module_name, globals(), locals(), [".".join(from_list)])
                    if 'functions' in self.options:
                        _, methods = self.get_members(m, 'function', ['__init__'])
                        self.content = ["~%s.%s" % (module_name, method) for method in methods if not method.startswith('_')]
                finally:
                    return super(AutoFuncSummary, self).run()


        app.add_directive('autofuncsummary', AutoFuncSummary)
    except BaseException as e:
        raise e