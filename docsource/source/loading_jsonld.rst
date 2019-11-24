Loading JSON LD
===============

.. literalinclude:: examples/data/ds_m_encoding.json
   :language: JSON

.. jupyter-execute::

    import sotools
    g = sotools.loadJsonldGraph(filename="source/examples/data/ds_m_encoding.json", publicID="https://my.data/")
    sotools.renderGraph(g)

