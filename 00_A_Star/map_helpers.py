import time
import networkx as nx # networkx 1.11
import pickle
import plotly.plotly as py # plotly 2.0.15
import random

from IPython import display
from plotly.graph_objs import *
from plotly.offline import init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)

class Map:
    def __init__(self, file_path):
        self._graph = self.load_map_from(file_path)
        self.intersections = nx.get_node_attributes(self._graph, "pos")
        self.roads = [list(self._graph[node]) for node in self._graph.nodes()]

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self._graph, f)

    def load_map_from(self, file_path):
        with open(file_path, 'rb') as f:
            graph = pickle.load(f)
        return graph

class MapPlot():
    """docstring for MapPlot"""
    def __init__(self, Map):
        self._graph = Map._graph
        self.nodes_layer = None
        self.edges_layer = None
        self.fig = None

    def initialize_edges_layer(self):
        "Initializes scatter plot for edges"
        self.edges_layer = Scatter(
        x=[],
        y=[],
        line=Line(width=0.5,color='#888'),
        hoverinfo='none',
        mode='lines')

    def add_graph_edges_to_edges_layer(self):
        "Adds all edges from graph to scatter plot"
        for edge in self._graph.edges():
            x0, y0 = self._graph.node[edge[0]]['pos']
            x1, y1 = self._graph.node[edge[1]]['pos']
            self.edges_layer['x'] += [x0, x1, None]
            self.edges_layer['y'] += [y0, y1, None]

    def initialize_nodes_layer(self):
        "Initializes scatter plot for nodes"
        self.nodes_layer = Scatter(
            x=[],
            y=[],
            text=[],
            mode='markers',
            hoverinfo='text',
            marker=Marker(
                showscale=False,
                # colorscale options
                # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
                # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
                colorscale='Hot',
                reversescale=True,
                color=[],
                size=10,
                colorbar=dict(
                    thickness=15,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                ),
                line=dict(width=2)))

    def add_graph_nodes_to_nodes_layer(self):
        "Adds all nodes from graph to scatter plot"
        for node in self._graph.nodes():
            x, y = self._graph.node[node]['pos']
            self.nodes_layer['x'].append(x)
            self.nodes_layer['y'].append(y)
            color = 0
            self.nodes_layer['marker']['color'].append(color)
            node_info = "Intersection " + str(node)
            self.nodes_layer['text'].append(node_info)

    def update_node_colors(self, start, goal, path):
        for node, color in enumerate(self.nodes_layer['marker']['color']):
            if node == start:
                self.nodes_layer['marker']['color'][node] = 3
            elif node == goal:
                self.nodes_layer['marker']['color'][node] = 1
            elif path and node in path:
                self.nodes_layer['marker']['color'][node] = 2
            else:
                self.nodes_layer['marker']['color'][node] = 0

    def highlight_nodes(self, start, goal, path):
        self.update_node_colors(start, goal, path)
        self.compile_figure()

        display.clear_output(wait=True)
        display.display(iplot(self.fig))
        time.sleep(1.0)

    def compile_figure(self):
        self.fig = Figure(data=Data([self.edges_layer, self.nodes_layer]),
                     layout=Layout(
                        title='<br>Network graph made with Python',
                        titlefont=dict(size=16),
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                       
                        xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))

    def initialize_layers(self):
        #pos = nx.get_node_attributes(self._graph, 'pos')
        # Initialize edges layer
        self.initialize_edges_layer()
        self.add_graph_edges_to_edges_layer()
        # Initialize nodes layer
        self.initialize_nodes_layer()
        self.add_graph_nodes_to_nodes_layer()
        
    def show_map(self, start=None, goal=None, path=None):
        self.initialize_layers()
        self.compile_figure()
        display.clear_output(wait=True)
        display.display(iplot(self.fig))
        time.sleep(1.0)


