# Get links to metadata documents referenced from a SO:dataset
import sotools
from pprint import pprint

json_source = "examples/data/ds_m_subjectof.json"
g = sotools.loadSOGraph(filename=json_source, publicID="https://my.server.net/data/")
links = sotools.getDatasetMetadataLinks(g)
pprint(links, indent=2)