# Load a graph and render the output (for jupyter notebooks)
import sotools
g = sotools.loadSOGraph(filename="source/examples/data/ds_m_subjectof.json")
sotools.renderGraph(g)
