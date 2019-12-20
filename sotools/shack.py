"""
Implements SHACL evaluation tools
"""

import rdflib
import rdflib.compare
import pyshacl


def validateSHACL(shape_graph, data_graph):
    """
    Validate data against a SHACL shape using common options.

    Args:
        shape_graph (ConjunctiveGraph): A SHACL shape graph
        data_graph (ConjunctiveGraph): Data graph to be validated with shape_graph

    Returns (tuple): Conformance (boolean), result graph (Graph) and result text

    Example:

    .. jupyter-execute:: examples/code/eg_validate_01.py

    """
    conforms, result_graph, result_text = pyshacl.validate(
        data_graph,
        shacl_graph=shape_graph,
        inference="rdfs",
        meta_shacl=True,
        abort_on_error=False,
        debug=False,
        advanced=True,
    )
    return conforms, result_graph, result_text


def shaclTestCase(shape_graph, data_graph, expected_graph):
    """
    Apply SHACL shape_graph to data_graph and compare with expected_graph.

    Result provides isomorphism, similarity, diff_graphs

    Args:
        shape_graph (Graph):
        data_graph (Graph):
        expected_graph (Graph):

    Returns {boolean, boolean, (Graph, Graph, Graph)}:

    """
    conforms, result_graph, result_text = validateSHACL(shape_graph, data_graph)
    # Convert to isomorphic form for comparison
    result_graph = rdflib.compare.to_isomorphic(result_graph)
    expected_graph = rdflib.compare.to_isomorphic(expected_graph)
    res = {"isomorphic":False, "similar": False, "diff":{} }
    res["isomorphic"] = result_graph == expected_graph
    res["similar"] = rdflib.compare.similar(result_graph, expected_graph)
    g12,g1,g2 = rdflib.compare.graph_diff(result_graph, expected_graph)
    res["diff"]["in_both"] = g12
    res["diff"]["in_result"] = g1
    res["diff"]["in_expected"] = g2
    return res
