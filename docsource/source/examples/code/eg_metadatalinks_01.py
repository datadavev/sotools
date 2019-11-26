# Get links to metadata documents referenced from a SO:dataset
import sotools
import json
from pprint import pprint

# Note: in this case two entries are returned because the single
# link is recognized with two different encodingFormats
json_source = "examples/data/ds_m_subjectof.json"
g = sotools.loadSOGraph(filename=json_source)
links = sotools.getDatasetMetadataLinks(g)
print("The source graph:")
print(json.dumps(json.load(open(json_source, 'r')), indent=2))
print("\nThe links to external metadata:")
pprint(links, indent=2)
