Testing for a bad namespace with SHACL
======================================

.. contents:: Contents
   :local:

Overview
--------

This is a brute force approach to using SHACL to report invalid use of a namespace. It
is only effective where there are limited combinations of the bad namespace and
matching classes for testing.

Using the SHACL shapes:

.. literalinclude:: examples/shapes/test_namespace.ttl

and a graph with three ``SO:Dataset`` sub-graphs that use invalid namespaces:

.. literalinclude:: examples/data/ds_bad_namespace.json

The SHACL tests are applied and results printed:

.. jupyter-execute::

    import rdflib
    import pyshacl
    shape_graph = rdflib.Graph()
    shape_graph.parse("examples/shapes/test_namespace.ttl", format="turtle")
    data_graphs = rdflib.ConjunctiveGraph()
    data_graphs.parse("examples/data/ds_bad_namespace.json", format="json-ld", publicID="https://example.net/")
    conforms, results_graph, results_text = pyshacl.validate(
        data_graphs,
        shacl_graph=shape_graph,
        inference="rdfs",
        meta_shacl=True,
        abort_on_error=False,
        debug=False
    )
    print(results_text)

For comparison, a valid ``SO:Dataset``:

.. literalinclude:: examples/data/ds_m_about.json

Does not match any of the bad namespace tests and so conforms.

.. jupyter-execute::

    data_graphs.parse("examples/data/ds_m_about.json", format="json-ld", publicID="https://example.net/")
    conforms, results_graph, results_text = pyshacl.validate(
        data_graphs,
        shacl_graph=shape_graph,
        inference="rdfs",
        meta_shacl=True,
        abort_on_error=False,
        debug=False
    )
    print(results_text)


Running code on this page
-------------------------

All examples on this page can be run live in Binder. To do so:

1. Click on the "Activate Binder" button
2. Wait for Binder to be active. This can take a while, you can watch progress in your
   browser's `javascript console`_. When a line like ``Kernel: connected (89dfd3c8...`` appears,
   Binder should be ready to go.
3. Run the following **before** any other script on the page. This sets the right
   path context for loading examples etc.

.. thebe-button:: Activate Binder

.. jupyter-execute::
   :hide-code:
   :hide-output:

   import os
   try:
       os.chdir("docsource/source")
   except:
       pass
   print("Page is ready. You can now run other code blocks on this page.")

.. _javascript console: https://webmasters.stackexchange.com/questions/8525/how-do-i-open-the-javascript-console-in-different-browsers
