import sotools.shack
import rdflib

data_source = "examples/data/ds_bad_namespace.json"
data_graph = rdflib.ConjunctiveGraph()
data_graph.parse(data_source, format="json-ld", publicID="https://example.net/data/")
shape_source = "examples/shapes/test_namespace.ttl"
shacl_graph = rdflib.ConjunctiveGraph()
shacl_graph.parse(shape_source, format="turtle")
conforms, result_graph, result_text = sotools.shack.validateSHACL(data_graph, shacl_graph=shacl_graph)
print(f"Data shape conforms: {conforms}")
print(f"Results text: \n{result_text}")
print("Results graph:")
sotools.renderGraph(result_graph)
