# Load a graph and render the output (for jupyter notebooks)
import sotools
g = sotools.loadSOGraph(filename="examples/data/ds_m_subjectof_01.json", publicID="https://example.net/")
sotools.renderGraph(g)
