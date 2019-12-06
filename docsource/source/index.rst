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

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   test_namespace
   ns_normalize
   external_metadata
   sotools.common


.. graphviz::

   digraph foo {
      rankdir="BT";
      graph [fontname="avenir", fontsize=10];
      node [fontname="avenir", fontsize=10];
      edge [fontname="avenir", fontsize=10];
      Thing [shape=rectangle, style=filled, fillcolor=darkseagreen2];
      CreativeWork [shape=rectangle, style=filled, fillcolor=darkseagreen2];
      Dataset [shape=rectangle, style=filled, fillcolor=darkseagreen2];
      MediaObject [shape=rectangle, style=filled, fillcolor=darkseagreen2];
      Intangible [shape=rectangle, style=filled, fillcolor=darkseagreen2];
      PropertyValue [shape=rectangle, style=filled, fillcolor=darkseagreen2];

      CreativeWork -> Thing [style=dashed, arrowhead=onormal];
      Intangible -> Thing  [style=dashed, arrowhead=onormal];
      Dataset -> CreativeWork  [style=dashed, arrowhead=onormal];
      MediaObject -> CreativeWork [style=dashed, arrowhead=onormal];
      PropertyValue -> Intangible [style=dashed, arrowhead=onormal];

   }



.. note::

   Herein the term "``SO:``" refers to the ``https://schema.org/`` namespace or any equivalents.


Indices and tables
__________________

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
