"""

"""

import io
from rdflib import ConjunctiveGraph, Namespace, plugin, URIRef
from rdflib.tools import rdf2dot
import graphviz

def _normalizeNode(t):
    """
    Hack the URIRefs to normalize schema.org to use "https://schema.org/"
    """
    if isinstance(t, URIRef):
        v = str(t)
        if v.startswith("http://schema.org"):
            v = v.replace("http://schema.org","https://schema.org",1)
            if v[18] != "/":
                v = "https://schema.org/" + v[18:]
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


def loadJsonldGraph(filename=None, data=None):
    """
    Load json-ld string or file to an RDFLib ConjunctiveGraph

    NOTE: Namespace use of <http://schema.org>, <https://schema.org>, or
    <http://schema.org/> is normalized to <https://schema.org/>.
    """
    g = ConjunctiveGraph()
    if data is not None:
        g.parse(data=data, format="json-ld")
    elif filename is not None:
        g.parse(filename, format="json-ld")
    # Now normalize the graph namespace use to https://schema.org/
    g2 = ConjunctiveGraph()
    for s, p, o in g:
        g2.add((
            _normalizeNode(s),
            _normalizeNode(p),
            _normalizeNode(o)
        ))
    return g2


def renderGraph(g):
    fp = io.StringIO()
    rdf2dot.rdf2dot(g, fp)
    return graphviz.Source(fp.getvalue())


def isDataset(g):
    """
    Return True if the provided data_graph is an instance of schema.org/Dataset
    """
    q = SPARQL_PREFIXES + """
    SELECT ?x 
    { 
        ?x rdf:type schema:Dataset .        
    }
    """
    qres = g.query(q)
    return len(qres) >= 1


def getLiteralIdentifiers(g):
    """
    Return a list of SO:Dataset.identifier entries that are simple strings
    """
    q = SPARQL_PREFIXES + """
    SELECT ?y ?tt
    WHERE {
        ?x rdf:type schema:Dataset .
        ?x schema:identifier ?y.
        ?y rdf:type ?tt .
        FILTER (datatype(?y) = xsd:string)
    }
    """
    res = []
    qres = g.query(q)
    for v in qres:
        res.append(str(v[0]))
    return res


def getStructuredIdentifiers(g):
    """
    Return a list of SO:Dataset.identifier entries that have structure
    like that suggested by science on schema.org.
    """
    q = SPARQL_PREFIXES + """
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
    res = []
    qres = g.query(q)
    for v in qres:
        i = {
            "value": str(v[0]),
            "url": str(v[1]),
            "propertyId": str(v[2])
        }
        res.append(i)
    return res


def getIdentifiers(g):
    """
    Return a list of SO:Dataset.identifier entries that can be either a string or
    a dictionary of
    """
    # First get any identifiers that are literals with no additional context
    res = getLiteralIdentifiers(g)
    return res + getStructuredIdentifiers(g)

def getMetadataLinksFromEncoding(g):
    """
    Return list of metadata encoding information
    """
    q = SPARQL_PREFIXES + """
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
    res = []
    qres = g.query(q)
    for item in qres:
        entry = {
            "dateModified" : item[0],
            "encodingFormat" : str(item[1]),
            "contentUrl" : str(item[2]),
            "description" : str(item[3]),
            "subjectOf" : str(item[4])
        }
        res.append(entry)
    return res


def getMetadataLinksFromSubjectOf(g):
    """
    return a list of metadata
    """
    q = SPARQL_PREFIXES + """
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
    res = []
    qres = g.query(q)
    for item in qres:
        entry = {
            "dateModified" : item[0],
            "encodingFormat" : str(item[1]),
            "contentUrl" : str(item[2]),
            "description" : str(item[3]),
            "subjectOf" : str(item[4])
        }
        res.append(entry)
    return res


def getMetadataLinksFromAbout(g):
    """
    return a list of metadata that describe this dataset, not necessarily the components.
    """
    q = SPARQL_PREFIXES + """
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
    res = []
    qres = g.query(q)
    for item in qres:
        entry = {
            "dateModified" : item[0],
            "encodingFormat" : str(item[1]),
            "contentUrl" : str(item[2]),
            "description" : str(item[3]),
            "subjectOf" : str(item[4])
        }
        res.append(entry)
    return res


def getMetadataLinks(g):
    """
    Metadata docs can be referenced  couple different ways
    1. as subjectOf
    2. The inverse of 1, about
    3. Encoding
    """
    res = getMetadataLinksFromEncoding(g)
    res += getMetadataLinksFromSubjectOf(g)
    res += getMetadataLinksFromAbout(g)
    return res

