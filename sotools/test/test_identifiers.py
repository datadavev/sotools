"""
Tests for identifier identification in schema.org Datasets

Run with::

  $ pytest

"""
import os.path
import sotools.common

# References to test data
# These are located in the docsource folder
test_data_folder = os.path.join(
    os.path.dirname(__file__), "../../examples/data/"
)

test_data = {
    "literal": os.path.join(test_data_folder, "id_literal.json"),
    "structured_01": os.path.join(test_data_folder, "id_structured_01.json"),
    # multiple structured identifiers, one for a DOI, the other for a checksum as URN
    "structured_02": os.path.join(test_data_folder, "id_structured_02.json"),
    # Structured identifier, but no value for the identifier
    "structured_novalue": os.path.join(test_data_folder, "id_structured_novalue.json"),
}


class TestIdentifierIdentification:

    def test_literalDatasetIdentifier(self):
        g = sotools.loadSOGraph(filename=test_data["literal"])
        ids = sotools.getDatasetIdentifiers(g)
        assert len(ids) == 1
        assert ids[0]["value"] == "simple_literal_string"
        assert ids[0]["propertyId"] == "Literal"

    def test_structuredDatasetIdentifier(self):
        g = sotools.loadSOGraph(filename=test_data["structured_01"])
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

        g = sotools.loadSOGraph(filename=test_data["structured_02"])
        ids = sotools.getDatasetIdentifiers(g)
        assert len(ids) == 3
        idx = find_id(ids, "10.1575/1912/bco-dmo.665253")
        assert idx >= 0
        assert ids[idx]["propertyId"] == "DOI"
        idx = find_id(ids, "urn:hash:sha1:19E517D7BFD58A64225E258CFEA8E3550E94D742")
        assert idx >= 0
        assert ids[idx]["propertyId"] == "http://id.loc.gov/vocabulary/preservation/cryptographicHashFunctions/sha1"


    def test_badDatasetIdentifier(self):
        g = sotools.loadSOGraph(filename=test_data["structured_novalue"])
        ids = sotools.getDatasetIdentifiers(g)
        assert len(ids) == 0
