"""
Tests for normalization of schema.org namespace.

Run with::

  $ pytest

"""
import sotools.common

class TestNamespaceNormalization:

    # Query to retrieve the graph that is of type https://schema.org/Dataset
    q_dataset = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX so:  <https://schema.org/>
        SELECT ?x 
        { 
            ?x rdf:type so:Dataset .
        }        
    """

    def test_http(self):
        """
        Check http://schema.org => https://schema.org/
        """
        j = """{
           "@context": {
              "@vocab": "http://schema.org/"
           },
           "@type":"Dataset"
        }"""
        g = sotools.common.loadJsonldGraph(data=j)
        qres = g.query(TestNamespaceNormalization.q_dataset)
        assert(len(qres) == 1)

    def test_noslash(self):
        """
        Check http://schema.org or https://schema.org => https://schema.org/
        """
        j = """{
           "@context": {
              "@vocab": "http://schema.org"
           },
           "@type":"Dataset"
        }"""
        g = sotools.common.loadJsonldGraph(data=j)
        qres = g.query(TestNamespaceNormalization.q_dataset)
        assert(len(qres) == 1)
        j = """{
           "@context": {
              "@vocab": "https://schema.org"
           },
           "@type":"Dataset"
        }"""
        g = sotools.common.loadJsonldGraph(data=j)
        qres = g.query(TestNamespaceNormalization.q_dataset)
        assert(len(qres) == 1)
