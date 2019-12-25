Testing for a bad namespace with SHACL
======================================

.. contents:: Contents
   :local:

Overview
--------

This is a brute force approach to using SHACL to report invalid use of a namespace. It
is only effective where there are limited combinations of the bad namespace and
matching classes [#targets]_ for testing.

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


Footnotes
---------

.. [#targets] The limitation of this approach stems from the need to identify a target node that the SHACL
  constraints are applied against. Adding checks for additional ``SO:`` types with this pattern requires
  a separate ``sh:targetClass`` rule for each combination of namespace and type. In this case, three entries for each
  type being tested would be required.


.. include:: includes/binder_activate.rst



