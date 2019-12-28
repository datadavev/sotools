import os
import pytest
import rdflib
from urllib.parse import urljoin
import sotools.common
import sotools.shack

D1 = "https://ns.dataone.org/schema/SO/1.0/SHACL/"

SOURCE_BASE = os.path.join(
    os.path.dirname(__file__), "../../examples/"
)

FORMAT_MAP = {
    ".ttl":"turtle",
    ".json":"json-ld",
    ".jsonld":"json-ld",
    ".js":"json-ld",
    ".html":"rdfa",
    ".n3":"n3"
}

ALL_SHAPES = {
    "so_no_slash": {
        "shape": "shapes/test_namespace.ttl",
        "data": "data/ds_bad_namespace.json",
        "data_id": D1+"so_no_slash",
        "result": {"conforms": False},
    },
    "so_http_no_slash": {
        "shape": "shapes/test_namespace.ttl",
        "data": "data/ds_bad_namespace.json",
        "data_id": "d1:so_http_no_slash",
        "result": {"conforms": False},
    },
    "so_http": {
        "shape": "shapes/test_namespace.ttl",
        "data": "data/ds_bad_namespace.json",
        "data_id": "d1:so_http",
        "result": {"conforms": False},
    },
    "so_ok": {
        "shape": "shapes/test_namespace.ttl",
        "data": "data/ds_bad_namespace.json",
        "data_id": "d1:so_ok",
        "result": {"conforms": True},
    }
}

def guessGraphFormat(filename):
    root,ext = os.path.splitext(filename)
    ext = ext.lower()
    return FORMAT_MAP.get(ext, None)


def expandQName(g, identifier):
    prefix, _id = rdflib.namespace.split_uri(identifier)
    ns = g.store.namespace(prefix.replace(":", "", 1))
    if not ns is None:
        return rdflib.URIRef(urljoin(ns, _id))
    return rdflib.URIRef(identifier)


def loadGraph(filename, publicID=None, identifier=None):
    g = rdflib.ConjunctiveGraph()
    g.parse(os.path.join(SOURCE_BASE, filename), format=guessGraphFormat(filename), publicID=publicID)
    if not identifier is None:
        identifier = expandQName(g, identifier)
        g2 = sotools.common.getSubgraph(g, identifier)
        return g2
    return g

def resolveGraph(uri, source_base=SOURCE_BASE):
    pass


class TestLocal:

    def test_guessGraphFormat(self):
        assert guessGraphFormat("a/b.json") == "json-ld"
        assert guessGraphFormat("a/b.ttl") == "turtle"
        assert not (guessGraphFormat("a/b.json") == "turtle")


class TestSHACLTest:

    @pytest.mark.parametrize("source", ALL_SHAPES.keys())
    def test_all_shapes(self, source):
        src = ALL_SHAPES[source]
        sg = loadGraph(src["shape"])
        dg = loadGraph(src["data"], publicID=D1, identifier=src.get("data_id", None))
        print("DG = ")
        print(dg.serialize(format="turtle").decode())
        og = None
        try:
            loadGraph(src["ontology"])
        except KeyError:
            pass
        conforms, result_graph, result_text = sotools.shack.validateSHACL(dg, shacl_graph=sg, ont_graph=og)
        assert conforms == src.get("result").get("conforms")

