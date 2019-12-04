Linking to metadata documents
=============================

A dataset may have associated metadata serialized in formats other than the ``SO:Dataset`` [#dataset]_ , and
it is beneficial to indicate how those metadata may be retrieved.

There are several options for providing links to resources associated with a ``SO:Dataset``. Each of these
must satisfy the criteria of providing a link to the resource, indicating the type of the linked resource, and
the relationship between the linked resource and the ``SO:Dataset`` and its components.

Three options for linking to external metadata documents are described here:

1. Using :ref:`subjectof-label` to indicate the ``SO:Dataset`` is the subject of an ``SO:CreativeWork`` of derivatives.
2. Using the inverse of 1, :ref:`about-label`
3. Using :ref:`encoding-label` to indicate the referenced ``SO:MediaObject`` is an alternative encoding of the
   ``SO:Dataset`` document.

These are more fully described below, with examples.

.. _subjectof-label:

`subjectOf` metadata links
--------------------------

The ``subjectOf`` [#subjectof]_ property indicates that the current ``SO:`` entity is the subject of the linked
property. In the following example, the ``SO:Dataset`` with id ``ds-02`` is the subject of the
``SO:CreativeWork`` [#creativework]_ document located at the url ``https://my.server.org/data/ds-02/metadata.xml``.

The type of the linked metadata document is indicated by the ``encodingFormat`` [#encodingformat]_ list. In this case,
the document has an ``encodingFormat`` of ``application/rdf+xml`` and also
``http://ns.dataone.org/metadata/schema/onedcx/v1.0``, which is a value from the DataONE vocabulary of object
formats [#objectformats]_.

.. literalinclude:: examples/data/ds_m_subjectof.json
   :language: JSON
   :linenos:

.. jupyter-execute::
   :hide-code:

   import binder_setup
   import sotools
   json_source = "examples/data/ds_m_subjectof.json"
   g = sotools.loadSOGraph(filename=json_source, publicID="https://my.server.net/data/")
   sotools.renderGraph(g)

Hence:

:link: ``https://my.server.org/data/ds-02/metadata.xml``
:type: Dublin Core in RDF-XML
:relationship: The ``SO:Dataset`` is the subject of the metadata

The links (and some other information) can be extracted using the SPARQL::

    PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX SO:   <https://schema.org/>

    SELECT ?dateModified ?encodingFormat ?url ?description ?about
    WHERE {
        ?about rdf:type SO:Dataset .
        ?about SO:subjectOf ?y .
        ?y SO:url ?url .
        ?y SO:encodingFormat ?encodingFormat .
        OPTIONAL {
          ?y SO:dateModified ?dateModified .
          ?y SO:description ?description .
        }
    }

Which is implemented in the method :func:`sotools.common.getDatasetMetadataLinksFromSubjectOf` .

For example:

.. jupyter-execute:: examples/code/eg_metadatalinks_subjectof_02.py

.. _about-label:

`about` metadata links
----------------------

The ``about`` [#about]_ property is the inverse of the ``subjectOf`` property and so asserts the linked property is about the
current ``SO:`` object.

In the following example, a composite dataset is described. The ``SO:MediaObject`` [#mediaobject]_ with
id ``./metadata.xml`` is ``about`` the ``SO:Dataset`` with id ``./`` and the ``SO:MediaObject`` with id
``./data_part_a.csv``.

The type of the metadata document as indicated by the ``encodingFormat`` property is ``http://www.isotc211.org/2005/gmd``,
a value which is drawn from the DataONE vocabulary of object formats.

.. literalinclude:: examples/data/ds_m_about.json
   :language: JSON
   :linenos:

.. jupyter-execute::
   :hide-code:

   import sotools
   json_source = "examples/data/ds_m_about.json"
   g = sotools.loadSOGraph(filename=json_source, publicID="https://my.server.net/data/")
   sotools.renderGraph(g)

Hence:

:link: ``https://example.org/my/data/1/metadata.xml``
:type: ISO TC211 XML Metadata
:relationship: The metadata is about the ``SO:Dataset``, and hence the ``SO:Dataset`` is the subject of the metadata

The links and other information can be extracted using the SPARQL::

    PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX SO:   <https://schema.org/>

    SELECT ?dateModified ?encodingFormat ?contentUrl ?description ?about
    WHERE {
        ?about rdf:type SO:Dataset .
        ?y SO:about ?about .
        ?y SO:contentUrl ?contentUrl .
        ?y SO:encodingFormat ?encodingFormat .
        OPTIONAL {
          ?y SO:dateModified ?dateModified .
          ?y SO:description ?description .
        }
    }

which is implemented in the :func:`sotools.common.getDatasetMetadataLinksFromAbout`.

For example:

.. jupyter-execute:: examples/code/eg_metadatalinks_about_02.py

.. _encoding-label:

`encoding` metadata links
-------------------------

The ``encoding`` property is defined [#encoding]_ as:

  A media object that encodes this CreativeWork. This property is a synonym for associatedMedia.

In this approach it is considered that the SO:Dataset document describes a dataset, as does the associated
metadata document (ISO or EML for example). As such, the XML and ``SO:Dataset`` are alternate encodings of the
same thing.

In the following example, the ``SO:Dataset`` with id ``ds_m_encoding`` has an ``encoding`` of type ``SO:MediaObject`` with
an id of ``ds_m_encoding#media-object`` and ``encodingFormat`` of ``http://www.isotc211.org/2005/gmd`` which is a value drawn
from the DataONE vocabulary of object formats. The media object is located at the
URL ``https://my.server.net/datasets/00.xml``

.. literalinclude:: examples/data/ds_m_encoding.json
   :language: JSON
   :linenos:

.. jupyter-execute::
   :hide-code:

   import sotools
   json_source = "examples/data/ds_m_encoding.json"
   g = sotools.loadSOGraph(filename=json_source, publicID="https://my.server.net/data/")
   sotools.renderGraph(g)

Hence:

:link: ``https://my.server.net/datasets/00.xml``
:type: ISO TC211 XML Metadata
:relationship: The metadata is an encoding of the ``SO:Dataset`` document

The links and other information can be extracted using the SPARQL::

    PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX SO:   <https://schema.org/>

    SELECT ?dateModified ?encodingFormat ?contentUrl ?description ?x
    WHERE {
        ?x rdf:type SO:Dataset .
        ?x SO:encoding ?y .
        ?y SO:encodingFormat ?encodingFormat.
        ?y SO:dateModified ?dateModified .
        ?y SO:contentUrl ?contentUrl .
        ?y SO:description ?description .
    }

which is implemented with the method :func:`sotools.common.getDatasetMetadataLinksFromEncoding`.

For example:

.. jupyter-execute:: examples/code/eg_metadatalinks_encoding_02.py

.. [#dataset] https://schema.org/Dataset
.. [#subjectof] https://schema.org/subjectOf
.. [#creativework] https://schema.org/CreativeWork
.. [#encodingformat] https://schema.org/encodingFormat
.. [#objectformats] https://cn.dataone.org/cn/v2/formats
.. [#about] https://schema.org/about
.. [#mediaobject] https://schema.org/MediaObject
.. [#encoding] https://schema.org/encoding