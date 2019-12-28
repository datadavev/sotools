"""
Tests for external metadata document links in schema.org Datasets

Run with::

  $ pytest

"""
import os.path
import rdflib
import sotools.common
import sotools.shack

test_data_folder = os.path.join(
    os.path.dirname(__file__), "../../examples/"
)

test_data = {
    "encoding": os.path.join(test_data_folder, "data/ds_m_encoding.json"),
    "subjectof01": os.path.join(test_data_folder, "data/ds_m_subjectof_01.json"),
    "subjectof01bad": os.path.join(test_data_folder, "data/ds_m_subjectof_01_bad.json"),
    "subjectof02": os.path.join(test_data_folder, "data/ds_m_subjectof_02.json"),
    "subjectof02bad": os.path.join(test_data_folder, "data/ds_m_subjectof_02_bad.json"),
    "subjectof03": os.path.join(test_data_folder, "data/ds_m_subjectof_03.json"),
    "subjectof03bad": os.path.join(test_data_folder, "data/ds_m_subjectof_03_bad.json"),
    "about": os.path.join(test_data_folder, "data/ds_m_about.json"),
}

test_shapes = {
    "subjectof": os.path.join(test_data_folder, "shapes/test_dataset_subjectof.ttl"),
}


class TestMetadataLinks:
    def test_encodingPattern(self):
        g = sotools.common.loadSOGraph(test_data["encoding"])
        links = sotools.common.getDatasetMetadataLinks(g)
        assert len(links) == 1
        assert links[0]["contentUrl"] == "https://my.server.net/datasets/00.xml"

    def test_subjectOfPattern(self):
        g = sotools.common.loadSOGraph(test_data["subjectof01"])
        links = sotools.common.getDatasetMetadataLinks(g)
        assert len(links) >= 1
        assert links[0]["contentUrl"] == "https://my.server.org/data/ds_m_subjectof_01/metadata.xml"

    def test_aboutPattern(self):
        g = sotools.common.loadSOGraph(test_data["about"])
        links = sotools.common.getDatasetMetadataLinks(g)
        assert len(links) == 1
        assert links[0]["contentUrl"] == "https://example.org/my/data/1/metadata.xml"


class TestMetadataShapeSubjectOf:

    def test_CreativeWork(self):
        dg = sotools.common.loadSOGraph(test_data["subjectof01"])
        ds = rdflib.ConjunctiveGraph()
        ds.parse(test_shapes["subjectof"], format="turtle")
        conforms, result_graph, result_text = sotools.shack.validateSHACL(dg, shacl_graph=ds)
        print(result_text)
        assert conforms==True
        dg = sotools.common.loadSOGraph(test_data["subjectof01bad"])
        conforms, result_graph, result_text = sotools.shack.validateSHACL(dg, shacl_graph=ds)
        print(result_text)
        assert conforms==False


    def test_MediaObject(self):
        dg = sotools.common.loadSOGraph(test_data["subjectof02"])
        ds = rdflib.ConjunctiveGraph()
        ds.parse(test_shapes["subjectof"], format="turtle")
        conforms, result_graph, result_text = sotools.shack.validateSHACL(dg, shacl_graph=ds)
        print(result_text)
        assert conforms==True
        dg = sotools.common.loadSOGraph(test_data["subjectof02bad"])
        conforms, result_graph, result_text = sotools.shack.validateSHACL(dg, shacl_graph=ds)
        print(result_text)
        assert conforms==False


    def test_DataDownload(self):
        #schemag = rdflib.ConjunctiveGraph()
        #schemag.parse("../schema.org/schema_org.ttl", format="turtle", publicID="https://schema.org/")
        schemag = sotools.common.loadSOGraph(filename="../schema.org/schema_org.ttl", deslop=False, format="turtle")
        dg = sotools.common.loadSOGraph(test_data["subjectof03"])
        ds = rdflib.ConjunctiveGraph()
        ds.parse(test_shapes["subjectof"], format="turtle")
        conforms, result_graph, result_text = sotools.shack.validateSHACL(dg, shacl_graph=ds, ont_graph=schemag)
        print(result_text)
        assert conforms==True
        dg = sotools.common.loadSOGraph(test_data["subjectof03bad"])
        conforms, result_graph, result_text = sotools.shack.validateSHACL(dg, shacl_graph=ds, ont_graph=schemag)
        print(result_text)
        assert conforms==False
