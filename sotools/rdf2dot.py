"""
Modified version of rdflib.tools.rdf2dot

"""

import collections
import textwrap
import rdflib

LABEL_PROPERTIES = [
    rdflib.RDFS.label,
    rdflib.URIRef("http://purl.org/dc/elements/1.1/title"),
    rdflib.URIRef("http://xmlns.com/foaf/0.1/name"),
    rdflib.URIRef("http://www.w3.org/2006/vcard/ns#fn"),
    rdflib.URIRef("http://www.w3.org/2006/vcard/ns#org"),
    rdflib.URIRef("https://schema.org/"),
]

XSDTERMS = [
    rdflib.XSD[x]
    for x in (
        "anyURI",
        "base64Binary",
        "boolean",
        "byte",
        "date",
        "dateTime",
        "decimal",
        "double",
        "duration",
        "float",
        "gDay",
        "gMonth",
        "gMonthDay",
        "gYear",
        "gYearMonth",
        "hexBinary",
        "ID",
        "IDREF",
        "IDREFS",
        "int",
        "integer",
        "language",
        "long",
        "Name",
        "NCName",
        "negativeInteger",
        "NMTOKEN",
        "NMTOKENS",
        "nonNegativeInteger",
        "nonPositiveInteger",
        "normalizedString",
        "positiveInteger",
        "QName",
        "short",
        "string",
        "time",
        "token",
        "unsignedByte",
        "unsignedInt",
        "unsignedLong",
        "unsignedShort",
    )
]

EDGECOLOR = "blue"
NODECOLOR = "black"
ISACOLOR = "black"
SOCOLOR = "darkseagreen2"
EDGELABELCOLOR = "#336633"


def rdf2dot(g, stream, opts={}):
    """
    Convert the RDF graph to DOT
    writes the dot output to the stream
    """

    fields = collections.defaultdict(set)
    nodes = {}

    def node(x):

        if x not in nodes:
            nodes[x] = f"node{len(nodes)}"
        return nodes[x]

    def label(x, g):

        for labelProp in LABEL_PROPERTIES:
            l = g.value(x, labelProp)
            if l:
                return l

        try:
            return g.namespace_manager.compute_qname(x)[2]
        except:
            return x

    def formatliteral(l, g):
        v = html.escape(l)
        v = "<br />".join(textwrap.wrap(v))
        if l.datatype:
            return f'&quot;{v}&quot;^^{qname(l.datatype, g)}<br align="left" />'
        elif l.language:
            return f'&quot;{v}&quot;@{l.language}<br align="left" />'
        return f'&quot;{v}&quot;<br align="left" />'

    def qname(x, g):
        try:
            q = g.compute_qname(x)
            return q[0] + ":" + q[2]
        except:
            return x

    def predicateColor(p):
        return "BLACK"

    def classColor(u):
        # if u.startswith("https://schema.org/"):
        #    return SOCOLOR
        return "#eeeeee"

    stream.write(
        """
digraph { 
    graph [fontname="avenir", fontsize=10];
    node [fontname="avenir", fontsize=10];
    edge [fontname="avenir", fontsize=10];

    """
    )

    for s, p, o in g:
        sn = node(s)
        if p == rdflib.RDFS.label:
            continue
        if isinstance(o, (rdflib.URIRef, rdflib.BNode)):
            on = node(o)
            opstr = (
                f"\t{sn} -> {on} [color={predicateColor(p)}, label=< <font point-size='10'"
                f" color='{EDGELABELCOLOR}'>{qname(p, g)}</font> > ];\n"
            )
            stream.write(opstr)
        else:
            fields[sn].add((qname(p, g), formatliteral(o, g)))

    for u, n in nodes.items():
        stream.write(f"# {u} {n}\n")
        f = [
            f"<tr><td align='left'>{x[0]}</td><td align='left'>{x[1]}</td></tr>"
            for x in sorted(fields[n])
        ]
        stream.write(
            (
                f"{n} [ shape=none, color={NODECOLOR} label=< <table align='left' color='#666666'"
                f" cellborder='0' cellspacing='0' border='1'><tr>"
                # f"<td colspan='2' bgcolor='#d5d5d5'><B>{label(u,g)}</B></td></tr><tr>"
                f"<td href='{u}' bgcolor='{classColor(u)}' colspan='2'>"
                f"<font point-size='10' color='BLACK'>{u}</font></td>"
                f"</tr>{''.join(f)}</table> > ] \n"
            )
        )
    stream.write("}\n")
