"""
Implements SHACL evaluation tools
"""

import rdflib
import rdflib.compare
import pyshacl

def validateSHACL(data_graph, shacl_graph=None, ont_graph=None):
    """
    Validate data against a SHACL shape using common options.

    Calls pyshacl.validate with the options:

    :inference: "rdfs"
    :meta_shacl: True
    :abort_on_error: True
    :debug: False
    :advanced: True

    When validating shapes that use subclass inference, it is necessary for the relationships to be provided in one
    of the graphs, or separately with the ``onto_graph`` property.

    Args:
        shape_graph (:class:`~rdflib.graph.Graph`): A SHACL shape graph
        data_graph (:class:`~rdflib.graph.Graph`): Data graph to be validated with shape_graph
        ontology_graph (:class:`~rdflib.graph.Graph`): Optional ontology graph to be added to the data graph

    Returns (tuple): Conformance (boolean), result graph (:class:`~rdflib.graph.Graph`) and result text

    Example:

    .. jupyter-execute:: ../examples/code/eg_validate_01.py

    """
    conforms, result_graph, result_text = pyshacl.validate(
        data_graph,
        shacl_graph=shacl_graph,
        ont_graph=ont_graph,
        inference="rdfs",
        meta_shacl=True,
        abort_on_error=False,
        debug=False,
        advanced=True,
    )
    return conforms, result_graph, result_text


def shaclTestCase(data_graph, shacl_graph, expected_graph, ont_graph=None):
    """
    Apply SHACL shape_graph to data_graph and compare with expected_graph.

    Result provides isomorphism, similarity, diff_graphs

    Args:
        data_graph (:class:`~rdflib.graph.Graph`): The data graph
        shacl_graph (:class:`~rdflib.graph.Graph`): The SHACL shapes graph
        expected_graph (:class:`~rdflib.graph.Graph`): Expected outcome of the evaluation
        onto_graph (:class:`~rdflib.graph.Graph`): Optional ontology or vocabulary graph

    Returns {boolean, boolean, (:class:`~rdflib.graph.Graph`, :class:`~rdflib.graph.Graph`, :class:`~rdflib.graph.Graph`)}:

    """
    conforms, result_graph, result_text = validateSHACL(data_graph, shacl_graph, ont_graph=ont_graph)
    # Convert to isomorphic form for comparison
    result_graph = rdflib.compare.to_isomorphic(result_graph)
    expected_graph = rdflib.compare.to_isomorphic(expected_graph)
    res = {"conforms":conforms, "result_text":result_text, "isomorphic":False, "similar": False, "diff":{} }
    res["isomorphic"] = result_graph == expected_graph
    res["similar"] = rdflib.compare.similar(result_graph, expected_graph)
    g12,g1,g2 = rdflib.compare.graph_diff(result_graph, expected_graph)
    res["diff"]["in_both"] = g12
    res["diff"]["in_result"] = g1
    res["diff"]["in_expected"] = g2
    return res
