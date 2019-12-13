import rdflib
import rdflib.compare
import sotools

expected_json = """{
    "@context": {
        "@vocab":"https://example.net/"
    },
    "@id":"./sub",
    "property_0": "literal_0",
    "property_1": ["literal_1-0", "literal_1-1"],
    "property_2": {
        "property_3":"Anonymous subgraph"
    }
}
"""

test_json = """{
    "@context": {
        "@vocab":"https://example.net/"
    },
    "@id":"./parent",
    "sub":""" + expected_json + """    
}
"""

# Load the full graph, setting the base to "https://example.net/"
g_full = rdflib.Graph()
g_full.parse(data=test_json, format="json-ld", publicID="https://example.net/")
print("### Full:")
print(g_full.serialize(format="turtle").decode())

g_expected = rdflib.ConjunctiveGraph()
g_expected.parse(data=expected_json, format="json-ld", publicID="https://example.net/")
print("### Expected:")
print(g_expected.serialize(format="turtle").decode())

#Extract the subgraph that is the object of the subject "https://example.net/sub"
g_sub = sotools.getSubgraph(g_full, rdflib.URIRef("https://example.net/sub"))
print("### Extracted:")
print(g_sub.serialize(format="turtle").decode())

#Direct comparison of the graphs, will fail if there are BNodes
print(f"Extracted subgraph is equal to the expected graph: {g_sub == g_expected}")

# Use isomorphic comparison. This operations can be very expensive if either of
# the grphs are poorly structured with lots of BNodes
print((f"Extracted subgraph is isomorphic with the expected: "
      f"{rdflib.compare.isomorphic(g_sub, g_expected)}"))