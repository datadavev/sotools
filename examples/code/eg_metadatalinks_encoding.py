# Get links to metadata documents referenced from a SO:dataset
import sotools
import json
from pprint import pprint

json_source = "examples/data/ds_m_encoding.json"
g = sotools.loadSOGraph(filename=json_source, publicID="https://my.server.net/data/")
links = sotools.getDatasetMetadataLinks(g)
print("The source graph:")
print(json.dumps(json.load(open(json_source, 'r')), indent=2))
print("\nThe links to external metadata:")
pprint(links, indent=2)