Identifiers for Datasets
========================

The purpose of this document is to describe the behavior of DataONE indexers when encountering
identifiers in ``SO:Dataset`` [#dataset]_ instances.

In the context of DataONE, a dataset has multiple components. Each component version is preserved
and each component version has a persistent, globally unique identifier (PID). Each component may
also be assigned a globally unique identifier that always resolves to the most recent version
of a component (SeriesID or SID). That context is used in this document.

id and identifier
-----------------

The ``@id`` property in JSON-LD [#id]_ identifies a node in the RDF graph, and should be an IRI [#IRI]_.

Persistence
-----------

.. graphviz::

   digraph foo {
      "bar" -> "baz";
   }

References
----------

.. [#id] https://www.w3.org/TR/json-ld/#node-identifiers
.. [#IRI] An IRI (Internationalized Resource Identifier) is a string that conforms to the
          syntax defined in :rfc:`3987`
.. [#dataset] https://schema.org/Dataset
.. [#identifier] http://schema.org/docs/datamodel.html#identifierBg