"""
Tests for normalization of schema.org namespace.

Run with::

  $ pytest

"""
import sotools.common

http_context_json = """
{
   "@context": {
      "@vocab": "http://schema.org/"
   },
   "@type":"Dataset"
}
"""

http_context_noslash_json = """
{
   "@context": {
      "@vocab": "http://schema.org"
   },
   "@type":"Dataset"
}
"""

https_context_noslash_json = """
{
   "@context": {
      "@vocab": "https://schema.org"
   },
   "@type":"Dataset"
}
"""


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
        g = sotools.common.loadSOGraph(data=http_context_json)
        qres = g.query(TestNamespaceNormalization.q_dataset)
        assert(len(qres) == 1)


    def test_noslash(self):
        """
        Check http://schema.org or https://schema.org => https://schema.org/
        """
        g = sotools.common.loadSOGraph(data=http_context_noslash_json)
        qres = g.query(TestNamespaceNormalization.q_dataset)
        assert(len(qres) == 1)
        g = sotools.common.loadSOGraph(data=https_context_noslash_json)
        qres = g.query(TestNamespaceNormalization.q_dataset)
        assert(len(qres) == 1)
