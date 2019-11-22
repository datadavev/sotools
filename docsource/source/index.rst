.. SOtools documentation master file, created by
   sphinx-quickstart on Thu Nov 21 13:18:16 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Tools for Schema.org Datasets
=============================

.. image:: https://travis-ci.com/datadavev/sotools.svg?branch=master
    :target: https://travis-ci.com/datadavev/sotools

Collection of notes and tools on working with Schema.org Dataset structures, with particular emphasis
on crawling and indexing with DataONE infrastructure.

Topics include:

* Schema.org namespace normalization for efficient processing
* Dataset identification
* Handling references to external metadata
* Identifiers for Datasets and their components

.. note::

   Herein the term "``SO:``" refers to the ``https://schema.org/`` namespace or any equivalents.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   ns_normalize
   loading_jsonld
   sotools.common


Indices and tables
__________________

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
