import rdflib
import sotools.common
import sotools.shack

"""
Some simple tests for the SHACL validation tool
"""

PUBLICID = "https://example.net/"

prefix = """
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix SO: <https://schema.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix d1: <http://ns.dataone.org/schema/2019/08/SO/Dataset#> .
@prefix ms: <http://www.w3.org/2001/sw/DataAccess/tests/test-manifest#> .
@prefix sht: <http://www.w3.org/ns/shacl-test#> .
"""
prefix += f"@prefix ex: <{PUBLICID}> .\n"

valid_data_source = """{
    "@context":{ 
        "@vocab": "https://schema.org/"
    },
    "@id":"my_data",
    "@type": "Dataset",
    "encoding":{
        "@type": "MediaObject"
    }
}
"""

invalid_data_source = """{
    "@context":{ 
        "@vocab": "https://schema.org/"
    },
    "@id":"my_data",
    "@type": "Dataset",
    "encoding":{
        "@type": "MediaObjectX"
    }
}
"""

shape_graph_source = prefix + '''
d1:DatasetShape
    a sh:NodeShape ;
    sh:targetClass SO:Dataset ;
    sh:property [
        sh:path SO:encoding ;
        sh:class SO:MediaObject ;
        sh:minCount 1 ;
        sh:message "Expecting SO:MediaObject at encoding."@en ;
        sh:severity sh:Violation ;
    ] .
'''

expected_valid_source = prefix + """
[] a sh:ValidationReport ;
    sh:conforms true .
"""

expected_invalid_source = prefix + """
[] a sh:ValidationReport ;
    sh:conforms false ;
    sh:result [
        a sh:ValidationResult ;
        sh:focusNode ex:my_data ;
        sh:resultMessage "Expecting SO:MediaObject at encoding."@en ;
        sh:resultPath SO:encoding ;
        sh:resultSeverity sh:Violation ;
        sh:sourceConstraintComponent sh:ClassConstraintComponent ;
        sh:sourceShape [ 
            a rdfs:Resource ;
            sh:class SO:MediaObject ;
            sh:message "Expecting SO:MediaObject at encoding."@en ;
            sh:minCount 1 ;
            sh:path SO:encoding ;
            sh:severity sh:Violation 
        ] ;
        sh:value [ 
            a rdfs:Resource, SO:MediaObjectX
        ] ; 
    ] .
"""

validation_graph_source = prefix + """
d1:validation_test
    a sht:Validate ;
    mf:action [
        sht:shapesGraph <> ;
        sht:dataGraph <> ;
    ] ;
    mf:result [
        a sh:ValidationReport ;
        sh:conforms true .
    ] ;
    mf:status sht:approved .
"""

class TestSHACLTest:

    def _printResult(self, result):
        print(str(result))
        print("=== In Both:")
        print(result["diff"]["in_both"].serialize(format="turtle").decode())
        print("=== In Result:")
        print(result["diff"]["in_result"].serialize(format="turtle").decode())
        print("=== In Expected:")
        print(result["diff"]["in_expected"].serialize(format="turtle").decode())


    def test_valid(self):
        data_graph = rdflib.Graph()
        data_graph.parse(data=valid_data_source, format="json-ld", publicID=PUBLICID)
        shape_graph = rdflib.Graph()
        shape_graph.parse(data=shape_graph_source, format="turtle", publicID=PUBLICID)
        expected_graph = rdflib.Graph()
        expected_graph.parse(data=expected_valid_source, format="turtle", publicID=PUBLICID)
        result = sotools.shack.shaclTestCase(shape_graph, data_graph, expected_graph)
        #self._printResult(result)
        assert result["isomorphic"]
        assert result["similar"]


    def test_invalid(self):
        data_graph = rdflib.Graph()
        data_graph.parse(data=invalid_data_source, format="json-ld", publicID=PUBLICID)
        shape_graph = rdflib.Graph()
        shape_graph.parse(data=shape_graph_source, format="turtle", publicID=PUBLICID)
        expected_graph = rdflib.Graph()
        expected_graph.parse(data=expected_invalid_source, format="turtle", publicID=PUBLICID)
        result = sotools.shack.shaclTestCase(shape_graph, data_graph, expected_graph)
        #self._printResult(result)
        assert result["isomorphic"]
        assert result["similar"]
