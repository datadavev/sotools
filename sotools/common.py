"""

"""

import io
from rdflib import ConjunctiveGraph, Namespace, plugin, URIRef
from rdflib.tools import rdf2dot
import graphviz

SPARQL_PREFIXES = """
    PREFIX rdf:      <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX schema:   <https://schema.org/>
    PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
    PREFIX datacite: <http://purl.org/spar/datacite/>
"""


def _normalizeTerm(t):
    """
    Hack the URIRefs to normalize schema.org to use "https://schema.org/"

    This is an ugly solution to the problem of variable representations of
    the schema.org namespace in the wild.

    Args:
        t: Graph term to process

    Returns:
        Graph term normalized to namespace <https://schema.org/>
    """
    if isinstance(t, URIRef):
        v = str(t)
        if v.startswith("http://schema.org"):
            v = v.replace("http://schema.org", "https://schema.org", 1)
            if v[18] != "/":
                v = "https://schema.org/" + v[18:]
                # rdflib will append a / to the end of terms where the predicate is rdf:type
                # when converting to a string even though internally it is treated as a
                # value without a trailing slash.
                if v[-1] == "/":
                    v = v[:-1]
            return URIRef(v)
        elif v.startswith("https://schema.org"):
            if v[18] != "/":
                v = "https://schema.org/" + v[18:]
                if v[-1] == "/":
                    v = v[:-1]
                return URIRef(v)
    return t


def loadJsonldGraph(filename=None, data=None, publicID=None):
    """
    Load json-ld string or file to an RDFLib ConjunctiveGraph

    Creates a ConjunctiveGraph from  the provided file or text. If both are
    provided then text is used.

    NOTE: Namespace use of <http://schema.org>, <https://schema.org>, or
    <http://schema.org/> is normalized to <https://schema.org/>.

    Args:
        filename: path to json-ld file on disk
        data: json-ld text
        publicID: (from rdflib) The logical URI to use as the document base. If None specified the document location is used.

    Returns:
        ConjunctiveGraph instance

    Example::

        >>> import sotools
        INFO:rdflib:RDFLib Version: 4.2.2
        >>> g = sotools.loadJsonldGraph(filename="sotools/data/data/ds_00.json")
        >>> g
        <Graph identifier=N3026433194a2427b840aea582bfba9e1 (<class 'rdflib.graph.ConjunctiveGraph'>)>
    """
    g = ConjunctiveGraph()
    if data is not None:
        g.parse(data=data, format="json-ld", publicID=publicID)
    elif filename is not None:
        g.parse(filename, format="json-ld", publicID=publicID)
    # Now normalize the graph namespace use to https://schema.org/
    g2 = ConjunctiveGraph()
    for s, p, o in g:
        g2.add((_normalizeTerm(s), _normalizeTerm(p), _normalizeTerm(o)))
    return g2


def renderGraph(g):
    """
    For rendering an rdflib graph in Jupyter notebooks

    Args:
        g: Graph or ConjunctiveGraph

    Returns:
        Output for rendering directly in the notebook
    """
    fp = io.StringIO()
    rdf2dot.rdf2dot(g, fp)
    return graphviz.Source(fp.getvalue())


def isDataset(g):
    """
    Evaluate if the Graph g is a SO:Dataset

    Args:
        g: ConjunctiveGraph

    Returns:
        boolean

    Example::

        >>> import sotools
        INFO:rdflib:RDFLib Version: 4.2.2
        >>> g = sotools.loadJsonldGraph(filename="sotools/data/data/ds_00.json")
        >>> sotools.isDataset(g)
        True
    """
    q = (
        SPARQL_PREFIXES
        + """
    SELECT ?x 
    { 
        ?x rdf:type schema:Dataset .        
    }
    """
    )
    qres = g.query(q)
    return len(qres) >= 1


def getLiteralIdentifiers(g):
    """
    Retrieve literal SO:Dataset.identifier entries

    Args:
        g: ConjunctiveGraph

    Returns:
        list of identifier strings
    """
    q = (
        SPARQL_PREFIXES
        + """
    SELECT ?y ?tt
    WHERE {
        ?x rdf:type schema:Dataset .
        ?x schema:identifier ?y.
        ?y rdf:type ?tt .
        FILTER (datatype(?y) = xsd:string)
    }
    """
    )
    res = []
    qres = g.query(q)
    for v in qres:
        res.append(str(v[0]))
    return res


def getStructuredIdentifiers(g):
    """
    Extract structured SO:Dataset.identifier entries

    Args:
        g: ConjunctiveGraph

    Returns:
        list: A list of ``{value:, url:, propertyId:}``
    """
    q = (
        SPARQL_PREFIXES
        + """
    SELECT DISTINCT ?value ?url ?propid
    WHERE {
        ?x rdf:type schema:Dataset .
        ?x schema:identifier ?y .
        ?y rdf:type ?tt .
        ?y schema:value ?value.
        ?y schema:url ?url .
        ?y schema:propertyID ?propid .
        FILTER (?tt = schema:PropertyValue || ?tt = datacite:ResourceIdentifier)
    }
    """
    )
    res = []
    qres = g.query(q)
    for v in qres:
        i = {"value": str(v[0]), "url": str(v[1]), "propertyId": str(v[2])}
        res.append(i)
    return res


def getIdentifiers(g):
    """
    Return a list of SO:Dataset.identifier entries from the provided Graph

    Args:
        g: ConjunctiveGraph

    Returns:
        list: A list of ``string`` or ``{value:, url:, propertyId:}``
    """
    # First get any identifiers that are literals with no additional context
    res = getLiteralIdentifiers(g)
    return res + getStructuredIdentifiers(g)


def getMetadataLinksFromEncoding(g):
    """
    Extract link to metadata from SO:Dataset.encoding

    Args:
        g: ConjunctiveGraph

    Returns:
        list: A list of ``{dateModified:, encodingFormat:, contentUrl:, description:, subjectOf:,}``
    """
    q = (
        SPARQL_PREFIXES
        + """
    SELECT ?dateModified ?encodingFormat ?contentUrl ?description ?x
    WHERE {
        ?x rdf:type schema:Dataset .
        ?x schema:encoding ?y .
        ?y schema:encodingFormat ?encodingFormat.
        ?y schema:dateModified ?dateModified .
        ?y schema:contentUrl ?contentUrl .
        ?y schema:description ?description .
    }
    """
    )
    res = []
    qres = g.query(q)
    for item in qres:
        entry = {
            "dateModified": item[0],
            "encodingFormat": str(item[1]),
            "contentUrl": str(item[2]),
            "description": str(item[3]),
            "subjectOf": str(item[4]),
        }
        res.append(entry)
    return res


def getMetadataLinksFromSubjectOf(g):
    """
    Extract list of metadata links from SO.Dataset.subjectOf

    Args:
        g: ConjunctiveGraph

    Returns:
        list: A list of ``{dateModified:, encodingFormat:, contentUrl:, description:, subjectOf:,}``
    """
    q = (
        SPARQL_PREFIXES
        + """
    SELECT ?dateModified ?encodingFormat ?url ?description ?about
    WHERE {
        ?about rdf:type schema:Dataset .
        ?about schema:subjectOf ?y .
        ?y schema:url ?url .
        ?y schema:encodingFormat ?encodingFormat .
        OPTIONAL {
          ?y schema:dateModified ?dateModified .
          ?y schema:description ?description .
        }    
    }
    """
    )
    res = []
    qres = g.query(q)
    for item in qres:
        entry = {
            "dateModified": item[0],
            "encodingFormat": str(item[1]),
            "contentUrl": str(item[2]),
            "description": str(item[3]),
            "subjectOf": str(item[4]),
        }
        res.append(entry)
    return res


def getMetadataLinksFromAbout(g):
    """
    Extract a list of metadata links SO:about(SO:Dataset)

    Args:
        g: ConjunctiveGraph

    Returns:
        list: A list of ``{dateModified:, encodingFormat:, contentUrl:, description:, subjectOf:,}``
    """
    q = (
        SPARQL_PREFIXES
        + """
    SELECT ?dateModified ?encodingFormat ?contentUrl ?description ?about
    WHERE {
        ?about rdf:type schema:Dataset .
        ?y schema:about ?about .
        ?y schema:contentUrl ?contentUrl .
        ?y schema:encodingFormat ?encodingFormat .
        OPTIONAL {
          ?y schema:dateModified ?dateModified .
          ?y schema:description ?description .
        }
    }
    """
    )
    res = []
    qres = g.query(q)
    for item in qres:
        entry = {
            "dateModified": item[0],
            "encodingFormat": str(item[1]),
            "contentUrl": str(item[2]),
            "description": str(item[3]),
            "subjectOf": str(item[4]),
        }
        res.append(entry)
    return res


def getMetadataLinks(g):
    """
    Extract links to metadata documents describing SO:Dataset

    Metadata docs can be referenced different ways
    * as SO:Dataset.subjectOf
    * the inverse of 1, SO:CreativeWork.about(SO:Dataset)
    * SO:Dataset.encoding

    Args:
        g: ConjunctiveGraph

    Returns:
        list: A list of ``{dateModified:, encodingFormat:, contentUrl:, description:, subjectOf:,}``

    Example::

        >>> from pprint import pprint
        >>> import sotools
        INFO:rdflib:RDFLib Version: 4.2.2
        >>> g = sotools.loadJsonldGraph(filename="sotools/data/data/ds_00.json")
        >>> links = sotools.getMetadataLinks(g)
        >>> pprint(links)
        [{'contentUrl': 'https://my.server.net/datasets/00.xml',
          'dateModified': rdflib.term.Literal('2019-10-10T12:43:11+00:00.000'),
          'description': 'ISO TC211 XML rendering of metadata',
          'encodingFormat': 'http://www.isotc211.org/2005/gmd',
          'subjectOf': 'file:///Users/vieglais/git/sotools/sotools/sotools/data/data/ds-00'}]
    """
    res = getMetadataLinksFromEncoding(g)
    res += getMetadataLinksFromSubjectOf(g)
    res += getMetadataLinksFromAbout(g)
    return res
