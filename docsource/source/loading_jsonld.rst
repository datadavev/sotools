Loading JSON LD
===============

.. literalinclude:: examples/data/ds_m_encoding.json
   :language: JSON

.. jupyter-execute::

    import sotools
    g = sotools.loadSOGraph(filename="examples/data/ds_m_encoding.json", publicID="https://my.data/")
    sotools.renderGraph(g)



.. note::

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
