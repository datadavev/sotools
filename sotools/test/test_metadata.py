"""
Tests for external metadata document links in schema.org Datasets

Run with::

  $ pytest

"""
import sotools.common
import os.path

test_data_folder = os.path.join(
    os.path.dirname(__file__), "../../docsource/source/examples/data/"
)

test_data = {
    "encoding": os.path.join(test_data_folder, "ds_m_encoding.json"),
    "subjectof": os.path.join(test_data_folder, "ds_m_subjectof.json"),
    "about": os.path.join(test_data_folder, "ds_m_about.json"),
}


class TestMetadataLinks:
    def test_encodingPattern(self):
        g = sotools.common.loadSOGraph(test_data["encoding"])
        links = sotools.common.getDatasetMetadataLinks(g)
        assert len(links) == 1
        assert links[0]["contentUrl"] == "https://my.server.net/datasets/00.xml"

    def test_subjectOfPattern(self):
        g = sotools.common.loadSOGraph(test_data["subjectof"])
        links = sotools.common.getDatasetMetadataLinks(g)
        assert len(links) >= 1
        assert links[0]["contentUrl"] == "https://my.server.org/data/ds-02/metadata.xml"

    def test_aboutPattern(self):
        g = sotools.common.loadSOGraph(test_data["about"])
        links = sotools.common.getDatasetMetadataLinks(g)
        assert len(links) == 1
        assert links[0]["contentUrl"] == "https://example.org/my/data/1/metadata.xml"
