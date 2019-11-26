# Load a graph and evaluate if it contains a SO:Dataset
import sotools
g = sotools.loadSOGraph(
    filename="source/examples/data/ds_bad_namespace.json",
    publicID="https://my.data.net/data/"
)
sotools.hasDataset(g)
