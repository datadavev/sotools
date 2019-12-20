# Load a graph and render the output (for jupyter notebooks)
import sotools
g = sotools.loadSOGraph(filename="examples/data/ds_m_subjectof.json", publicID="https://example.net/")
sotools.renderGraph(g)
