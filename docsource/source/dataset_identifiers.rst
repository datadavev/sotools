Identifiers for Datasets
========================

In the context of DataONE, a dataset has multiple components. Each component version is preserved,
and each component version has a persistent, globally unique identifier (PID). Each component may
also be assigned a globally unique identifier that always resolves to the most recent version
of a component (SeriesID).

That context is used in this document. The purpose of this document is to describe the behavior
of DataONE indexers when encountering identifiers in ``SO:Dataset`` instances.

