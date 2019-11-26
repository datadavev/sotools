# Load graph and show SO:Dataset.identifier entries
import sotools
import json
from pprint import pprint

json_source = "examples/data/id_structured_01.json"
g = sotools.loadSOGraph(filename=json_source)
identifiers = sotools.getDatasetIdentifiers(g)
print("The json-ld source graph:")
print(json.dumps(json.load(open(json_source, 'r')), indent=2))
print("\nThe identifier(s) used in the dataset:")
pprint(identifiers, indent=2)