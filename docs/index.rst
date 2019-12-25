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

.. graphviz::

   digraph foo {
      rankdir="BT";
      graph [fontname="avenir", fontsize=10];
      node [fontname="avenir", fontsize=10, target="_blank" shape=rectangle, style=filled, fillcolor=darkseagreen2];
      edge [fontname="avenir", fontsize=10, style=dashed, arrowhead=onormal];
      Thing [label="SO:Thing", href="https://schema.org/Thing"];
      CreativeWork [href="https://schema.org/CreativeWork"];
      Dataset [href="https://schema.org/Dataset"];
      MediaObject [href="https://schema.org/MediaObject"];
      DataDownload [href="https://schema.org/DataDownload"];
      Intangible [href="https://schema.org/Intangible"];
      PropertyValue [href="https://schema.org/PropertyValue"];
      Place [href="https://schema.org/Place", target="_blank"];
      Person [href="https://schema.org/Person", target="_blank"];
      Organization [href="https://schema.org/Organization"];

      CreativeWork -> Thing;
      Intangible -> Thing;
      Place -> Thing;
      Person -> Thing;
      Organization -> Thing;
      Dataset -> CreativeWork;
      MediaObject -> CreativeWork;
      DataDownload -> MediaObject;
      PropertyValue -> Intangible;
   }


.. toctree::
   :maxdepth: 1
   :caption: Contents:

   test_namespace
   ns_normalize
   external_metadata
   sotools.common
   sotools.shack
   sotools.rdf2dot
   changelog


.. note::

   Herein the term "``SO:``" refers to the ``https://schema.org/`` namespace or any equivalents.


Indices and tables
__________________

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
