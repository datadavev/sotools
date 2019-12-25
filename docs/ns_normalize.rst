Normalizing schema.org namespace
================================

Consistent representation of namespaces simplifies programmatic processing of markup. For example, even though
conceptually it is clear the terms ``http://schema.org/Dataset`` and ``https://schema.org/Dataset`` (note the protocol
difference) are referring to https://schema.org/Dataset, these are programmatically treated as different
entities. The schema.org guidelines [#sofaq]_ are somewhat ambivalent on the topic, with some emphasis on "https" adoption.

The trailing slash (/) is also important. Without it, common RDF processing libraries such as rdflib [#rdflib]_ will construct
a term like "https://schema.orgDataset". For example given the three ``SO:Dataset`` entries:

.. literalinclude:: ../examples/data/ds_bad_namespace.json
   :language: JSON
   :linenos:

the resulting ``RDF:type`` values as recognized by rdflib are:

.. jupyter-execute::

   from rdflib import ConjunctiveGraph
   g = ConjunctiveGraph()
   g.parse(
       "examples/data/ds_bad_namespace.json",
       format="json-ld",
       publicID="https://my.server.net/data/"
   )
   sparql_types = """
     PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
     SELECT ?x ?y
     {
        ?x rdf:type ?y .
     } ORDER BY ASC(?x) """

   qres = g.query(sparql_types)
   for v in qres:
       print(f'{v[0].n3()} {v[1].n3()}')

None of these will match for a query that relies on the schema.org namespace of ``https://schema.org/``:

.. jupyter-execute::

   sparql = """
     PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
     PREFIX SO: <https://schema.org/>
     SELECT ?x
     {
        ?x rdf:type SO:Dataset .
     } """

   qres = g.query(sparql)
   print(f"Number of matches = {len(qres)}")

There are however, many real world examples of each use of the schema.org namespace variants.

In order to simplify tooling for extracting information from schema.org resources, ``sotools`` will normalize all
json-ld graphs to use the namespace ``https://schema.org/``. The normalization is performed when loading with the
:func:`sotools.common.loadSOGraph` method. For example, loading the same data with normalization and applying
the same queries:

.. jupyter-execute::

   import sotools

   g = sotools.loadSOGraph(
       filename="examples/data/ds_bad_namespace.json",
       publicID="https://my.server.net/data/"
   )

   qres = g.query(sparql_types)
   for v in qres:
       print(f'{v[0].n3()} {v[1].n3()}')

   qres = g.query(sparql)
   print(f"Number of matches = {len(qres)}")


Footnotes
---------

.. [#sofaq] https://schema.org/docs/faq.html#19
.. [#rdflib] https://github.com/RDFLib/rdflib

.. include:: includes/binder_activate.rst