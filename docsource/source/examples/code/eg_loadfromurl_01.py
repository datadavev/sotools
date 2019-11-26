# Load graph from a URL and print the SO:Dataset.identifier values found
import sotools
from pprint import pprint

url = "https://www.bco-dmo.org/dataset/679374"
g = sotools.loadSOGraphFromUrl(url)
pprint(sotools.getDatasetIdentifiers(g), indent=2)
