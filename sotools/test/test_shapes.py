import rdflib
import sotools.common
import sotools.shack
import os

D1 = "http://ns.dataone.org/schema/SO/1.0/SHACL/"

SOURCE_BASE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../docsource/source/examples")
)

ALL_SHAPES = {
    "NS_01": {
        "shape": {
            "path": os.path.join(SOURCE_BASE, "shapes/test_namespace.ttl"),
            "format": "turtle",
            "identifier":"d1:DatasetBad1Shape",
        },
        "data": {
            "path": os.path.join(SOURCE_BASE, "data/ds_bad_namespace.json"),
            "format": "json-ld",
        },
        "expected": {"conforms": False},
    }
}


def resolveGraph(uri, source_base=SOURCE_BASE):
    pass


def load_and_evaluate_shape_test(src):
    sg = rdflib.ConjunctiveGraph()
    sg.parse(src["shape"]["path"], format=src["shape"]["format"])
    dg = rdflib.ConjunctiveGraph()
    dg.parse(src["data"]["path"], format=src["data"]["format"])



class TestSHACLTest:
    def test_all_shapes(self):
        pass
