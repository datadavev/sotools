"""

"""

import io
from rdflib import ConjunctiveGraph, Namespace, URIRef
from rdflib.namespace import NamespaceManager
from rdflib.tools import rdf2dot
import graphviz
import json
import requests
from extruct.jsonld import JsonLdExtractor
import logging
import re

SCHEMA_ORG = "https://schema.org/"
SO_PREFIX = "SO"

SPARQL_PREFIXES = """
    PREFIX rdf:      <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX SO:   <https://schema.org/>
    PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
    PREFIX datacite: <http://purl.org/spar/datacite/>
"""

# Mapping to undo case confusion
# For example, "propertyId" should be "propertyID"
# The LHS is the lowercase match to the correct RHS value
SO_TERMS = {"propertyid": "propertyID", "dataset": "Dataset"}

# Match variants of "https://schema.org/"
RE_SO = re.compile(r"^http.{0,1}://schema\.org/{0,1}")

logger = logging.getLogger(__name__)


def _desloppifyTerm(g, t):
    """
    Deal with sloppy case consistency in SO term use

    for example:
      SO:propertyId should be SO:propertyID

    Args:
        g: graph containing t
        t: term to de-slop

    Returns:
        term, de-slopped
    """
    if isinstance(t, URIRef):
        try:
            qname = g.namespace_manager.compute_qname(t)
            # 0 = prefix, 1 = namespace, 2 = term
            if qname[0] == SO_PREFIX:
                # Check the term value for case errors
                t_val = SO_TERMS.get(qname[2].lower(), qname[2])
                if t_val != qname[2]:
                    logger.info(f"replacing SO:{qname[2]} with {t_val}")
                # return the normalized term
                return URIRef(t_val, qname[1])
        # not a qname. Odd, but continue
        except Exception:
            pass
    return t


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
        so_match = RE_SO.match(v)
        if so_match is not None:
            v = v[so_match.end() :]
            if v[-1] == "/":
                v = v[:-1]
            return URIRef(v, SCHEMA_ORG)
    return t


def loadSOGraph(
    filename=None,
    data=None,
    publicID=None,
    normalize=True,
    deslop=True,
    format="json-ld",
):
    """
    Load RDF string or file to an RDFLib ConjunctiveGraph

    Creates a ConjunctiveGraph from  the provided file or text. If both are
    provided then text is used.

    NOTE: Namespace use of <http://schema.org>, <https://schema.org>, or
    <http://schema.org/> is normalized to <https://schema.org/> if ``normalize``
    is True.

    NOTE: Case of SO: properties in SO_TERMS is adjusted consistency if
    ``deslop`` is True

    Args:
        filename (string):  path to RDF file on disk
        data (string): RDF text
        publicID (string): (from rdflib) The logical URI to use as the document base. If None specified the document location is used.
        normalize (boolean): Normalize the use of schema.org namespace
        deslop (boolean): Adjust schema.org terms for case consistency
        format (string): The serialization format of the RDF to load

    Returns:
        ConjunctiveGraph instance

    Example::

        >>> import sotools
        INFO:rdflib:RDFLib Version: 4.2.2
        >>> g = sotools.loadJsonldGraph(filename=ds_m_encoding.jsonng.json")
        >>> g
        <Graph identifier=N3026433194a2427b840aea582bfba9e1 (<class 'rdflib.graph.ConjunctiveGraph'>)>
    """
    g = ConjunctiveGraph()
    ns = NamespaceManager(g)
    ns.bind(SO_PREFIX, SCHEMA_ORG, override=True)
    if data is not None:
        g.parse(data=data, format=format, publicID=publicID)
    elif filename is not None:
        g.parse(filename, format=format, publicID=publicID)
    if not (normalize or deslop):
        return g
    # Now normalize the graph namespace use to https://schema.org/
    g2 = ConjunctiveGraph()
    g2.namespace_manager = ns
    for s, p, o in g:
        trip = [s, p, o]
        if normalize:
            for i, t in enumerate(trip):
                trip[i] = _normalizeTerm(t)
        if deslop:
            for i, t in enumerate(trip):
                trip[i] = _desloppifyTerm(g, t)
        g2.add(trip)
    return g2


def loadSOGraphFromHtml(html, url):
    """
    Extract jsonld entries from provided HTML text

    Args:
        html: HTML text to be parsed

    Returns:
        ConjunctiveGraph instance

    """
    jslde = JsonLdExtractor()
    json_content = jslde.extract(html)
    g = ConjunctiveGraph()
    for json_data in json_content:
        g_data = loadSOGraph(data=json.dumps(json_data), publicID=url)
        g += g_data
    return g


def loadSOGraphFromUrl(url):
    """
    Loads graph from json-ld contained in a landing page.

    Args:
        url: String, url to process

    Returns:
        ConjunctiveGraph instance
    """
    response = requests.get(url)
    if response.status_code != requests.codes.ok:
        raise ValueError(
            f"GET request to {url} returned a status of {response.status_code}"
        )
    return loadSOGraphFromHtml(response.text, response.url)


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
        >>> g = sotools.loadSOGraph(filename="sotools/data/data/ds_m_encoding.json")
        >>> sotools.isDataset(g)
        True
    """
    q = (
        SPARQL_PREFIXES
        + """
    SELECT ?x 
    { 
        ?x rdf:type SO:Dataset .        
    }
    """
    )
    qres = g.query(q)
    return len(qres) >= 1


def getLiteralDatasetIdentifiers(g):
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
    SELECT ?y
    WHERE {
        ?x rdf:type SO:Dataset .
        ?x SO:identifier ?y .
        FILTER (isLiteral(?y)) .
    }
    """
    )
    res = []
    qres = g.query(q)
    for v in qres:
        res.append(str(v[0]))
    return res


def getStructuredDatasetIdentifiers(g):
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
        ?x rdf:type SO:Dataset .
        ?x SO:identifier ?y .
        ?y rdf:type ?tt .
        ?y SO:value ?value .
        ?y SO:propertyID ?propid .
        OPTIONAL { ?y SO:url ?url } .
        FILTER (?tt = SO:PropertyValue || ?tt = datacite:ResourceIdentifier)
    }
    """
    )
    res = []
    qres = g.query(q)
    for v in qres:
        i = {"value": str(v[0]), "url": str(v[1]), "propertyId": str(v[2])}
        res.append(i)
    return res


def getDatasetIdentifiers(g):
    """
    Return a list of SO:Dataset.identifier entries from the provided Graph

    Args:
        g: ConjunctiveGraph

    Returns:
        list: A list of ``string`` or ``{value:, url:, propertyId:}``
    """
    # First get any identifiers that are literals with no additional context
    res = getLiteralDatasetIdentifiers(g)
    return res + getStructuredDatasetIdentifiers(g)


def getDatasetMetadataLinksFromEncoding(g):
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
        ?x rdf:type SO:Dataset .
        ?x SO:encoding ?y .
        ?y SO:encodingFormat ?encodingFormat.
        ?y SO:dateModified ?dateModified .
        ?y SO:contentUrl ?contentUrl .
        ?y SO:description ?description .
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


def getDatasetMetadataLinksFromSubjectOf(g):
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
        ?about rdf:type SO:Dataset .
        ?about SO:subjectOf ?y .
        ?y SO:url ?url .
        ?y SO:encodingFormat ?encodingFormat .
        OPTIONAL {
          ?y SO:dateModified ?dateModified .
          ?y SO:description ?description .
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


def getDatasetMetadataLinksFromAbout(g):
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
        ?about rdf:type SO:Dataset .
        ?y SO:about ?about .
        ?y SO:contentUrl ?contentUrl .
        ?y SO:encodingFormat ?encodingFormat .
        OPTIONAL {
          ?y SO:dateModified ?dateModified .
          ?y SO:description ?description .
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


def getDatasetMetadataLinks(g):
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
        >>> g = sotools.loadSOGraph(filename=ds_m_encoding.json)ds_m_encoding.json>> links = sotools.getMetadataLinks(g)
        >>> pprint(links)
        [{'contentUrl': 'https://my.server.net/datasets/00.xml',
          'dateModified': rdflib.term.Literal('2019-10-10T12:43:11+00:00.000'),
          'description': 'ISO TC211 XML rendering of metadata',
          'encodingFormat': 'http://www.isotc211.org/2005/gmd',
          'subjectOf': 'file:///Users/vieglais/git/sotools/sotools/sotools/data/data/ds-00'}]
    """
    res = getDatasetMetadataLinksFromEncoding(g)
    res += getDatasetMetadataLinksFromSubjectOf(g)
    res += getDatasetMetadataLinksFromAbout(g)
    return res
