import networkx as nx 

from bokeh.io import output_file, show
from bokeh.models import (BoxZoomTool, Circle, HoverTool,
                          MultiLine, Plot, Range1d, ResetTool,)
from bokeh.palettes import Spectral4
from bokeh.plotting import from_networkx
from bokeh.models.graphs import EdgesAndLinkedNodes

def plot_graph (G):
    """
    Given a graph, plot it
    """

    plot = Plot(plot_width=3000, plot_height=3000, x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
    plot.title.text = "Lightning Network Graph"

    node_hover_tool = HoverTool(tooltips=[("pubkey", "@index"),("alias", "@alias"),("degree","@degree"),("capacity","@capacity")])
    plot.add_tools(node_hover_tool, BoxZoomTool(), ResetTool())

    graph_renderer = from_networkx(G, nx.spring_layout, scale=1, center=(0, 0))
    # graph_renderer = from_networkx(nx.subgraph(G,list(G.nodes)[:1000]), nx.spring_layout, scale=1, center=(0, 0))

    graph_renderer.node_renderer.glyph = Circle(size=15, fill_color='color')
    # graph_renderer.edge_renderer.glyph = MultiLine(line_color = "#CCCCCC", line_alpha = 0.8, line_width = 5)
    # graph_renderer.edge_renderer.selection_glyph = MultiLine(line_color = Spectral4[2], line_width = 5)
    # graph_renderer.edge_renderer.hover_glyph = MultiLine(line_color = Spectral4[1], line_width = 5)
    # graph_renderer.selection_policy = EdgesAndLinkedNodes()
    # graph_renderer.inspection_policy = EdgesAndLinkedNodes()
    plot.renderers.append(graph_renderer)

    output_file("lightning_network_visualization.html")
    show(plot)

def set_graph_color (G):
    """
    Set attribute 'color' for every node in G
    """
    nx.set_node_attributes(G, Spectral4[0], 'color')

def set_node_color (G, nodes, color):
    """
    For the given nodes, set the color attribute to the value supplied in color parameter
    """
    for node in nodes:
        G.nodes[node]['color'] = color
