"""
Tests for identifier identification in schema.org Datasets

Run with::

  $ pytest

"""
import sotools.common

literal_identifier_json = """
{
   "@context": {
      "@vocab": "http://schema.org"
   },
   "@type":"Dataset",
   "identifier":"simple_literal_string"
}
"""

structured_identifier_json = """
{
   "@context": {
      "@vocab": "http://schema.org",
      "datacite": "http://purl.org/spar/datacite/"
   },
   "@type":"Dataset",
   "identifier": {
       "@type": ["PropertyValue", "datacite:ResourceIdentifier"],
       "datacite:usesIdentifierScheme": { 
            "@id": "datacite:doi" 
       },
       "propertyID": "DOI",
       "url": "https://doi.org/10.1575/1912/bco-dmo.665253",
       "value": "10.1575/1912/bco-dmo.665253"
   }       
}
"""

# multiple structured identifiers, one for a DOI, the other for a checksum as URN
structured_identifier_json_multiple = """
{
   "@context": {
      "@vocab": "http://schema.org",
      "datacite": "http://purl.org/spar/datacite/"
   },
   "@type":"Dataset",
   "identifier": [
       {
           "@type": ["PropertyValue", "datacite:ResourceIdentifier"],
           "datacite:usesIdentifierScheme": { 
                "@id": "datacite:doi" 
           },
           "propertyID": "DOI",
           "url": "https://doi.org/10.1575/1912/bco-dmo.665253",
           "value": "10.1575/1912/bco-dmo.665253"
       },
       {
           "@type":["PropertyValue", "datacite:ResourceIdentifier"],
           "datacite:usesIdentifierScheme": { 
               "@id": "datacite:urn" 
           },
           "propertyID": "http://id.loc.gov/vocabulary/preservation/cryptographicHashFunctions/sha1",
           "value": "urn:hash:sha1:19E517D7BFD58A64225E258CFEA8E3550E94D742"
       }
   ]
}
"""

# Structured identifier, but no value for the identifier
structured_identifier_json_no_value = """
{
   "@context": {
      "@vocab": "http://schema.org",
      "datacite": "http://purl.org/spar/datacite/"
   },
   "@type":"Dataset",
   "identifier": {
       "@type": ["PropertyValue", "datacite:ResourceIdentifier"],
       "datacite:usesIdentifierScheme": { 
            "@id": "datacite:doi" 
       },
       "propertyID": "DOI",
       "url": "https://doi.org/10.1575/1912/bco-dmo.665253"
   }       
}
"""

class TestIdentifierIdentification:

    def test_literalDatasetIdentifier(self):
        g = sotools.loadJsonldGraph(data=literal_identifier_json)
        ids = sotools.getDatasetIdentifiers(g)
        assert len(ids) == 1
        assert ids[0] == "simple_literal_string"

    def test_structuredDatasetIdentifier(self):
        g = sotools.loadJsonldGraph(data=structured_identifier_json)
        ids = sotools.getDatasetIdentifiers(g)
        assert len(ids) == 1
        assert ids[0]["value"] == "10.1575/1912/bco-dmo.665253"
        assert ids[0]["propertyId"] == "DOI"

    def test_structuredDatasetIdentifierMultiple(self):
        # returned identifiers can be randomly ordered...
        def find_id(entries, value):
            i = 0
            for e in entries:
                v = e.get("value", None)
                if v == value:
                    return i
                i += 1
            return -1

        g = sotools.loadJsonldGraph(data=structured_identifier_json_multiple)
        ids = sotools.getDatasetIdentifiers(g)
        assert len(ids) == 2
        idx = find_id(ids, "10.1575/1912/bco-dmo.665253")
        assert idx >= 0
        assert ids[idx]["propertyId"] == "DOI"
        idx = find_id(ids, "urn:hash:sha1:19E517D7BFD58A64225E258CFEA8E3550E94D742")
        assert idx >= 0
        assert ids[idx]["propertyId"] == "http://id.loc.gov/vocabulary/preservation/cryptographicHashFunctions/sha1"


    def test_badDatasetIdentifier(self):
        g = sotools.loadJsonldGraph(data=structured_identifier_json_no_value)
        ids = sotools.getDatasetIdentifiers(g)
        assert len(ids) == 0
