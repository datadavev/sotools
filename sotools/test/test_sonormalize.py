"""
Tests for normalization of schema.org namespace.

Run with::

  $ pytest

"""
import os.path
import sotools.common

test_data_folder = os.path.join(
    os.path.dirname(__file__), "../../docsource/source/examples/data/"
)

test_data = {
    "http": os.path.join(test_data_folder, "ns_so_http.json"),
    "http_noslash": os.path.join(test_data_folder, "ns_so_http_noslash.json"),
    "https_noslash": os.path.join(test_data_folder, "ns_so_https_noslash.json"),
}


class TestNamespaceNormalization:

    # Query to retrieve the graph that is of type https://schema.org/Dataset
    q_dataset = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX SO:  <https://schema.org/>
        SELECT ?x 
        { 
            ?x rdf:type SO:Dataset .
        }        
    """

    def test_http(self):
        """
        Check http://schema.org => https://schema.org/
        """
        g = sotools.common.loadSOGraph(filename=test_data["http"])
        qres = g.query(TestNamespaceNormalization.q_dataset)
        assert(len(qres) == 1)


    def test_noslash(self):
        """
        Check http://schema.org or https://schema.org => https://schema.org/
        """
        g = sotools.common.loadSOGraph(filename=test_data["http_noslash"])
        qres = g.query(TestNamespaceNormalization.q_dataset)
        assert(len(qres) == 1)
        g = sotools.common.loadSOGraph(filename=test_data["https_noslash"])
        qres = g.query(TestNamespaceNormalization.q_dataset)
        assert(len(qres) == 1)
