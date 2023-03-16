import matplotlib.pyplot as plt 
import networkx as nx 
from graphviz import Digraph  

# define a function to create a visual representation of a DFA object
def SimulationDFA(self):
    
    # initialize an empty list to store the edges
    self.edges = []
    
    # initialize an empty dictionary to store the symbols for each edge
    self.trans_symbols = {}
    
    # iterate over each state and its transitions
    for i in self.transitions:
        for j in self.transitions[i]:
            
            # if the edge (i, j) already has a symbol, add the new symbol to the existing one
            if (i, self.transitions[i][j]) in self.trans_symbols.keys():
                self.trans_symbols[(i,self.transitions[i][j])] += ", " + j
            
            # otherwise, add the edge to the list of edges and set its symbol to the new symbol
            else:
                self.edges.append((i, self.transitions[i][j]))
                self.trans_symbols[(i,self.transitions[i][j])] = " " + j

    # create a new directed graph object
    G = nx.DiGraph()
    
    # add the edges to the graph object
    G.add_edges_from(self.edges)

    # add the symbols for each edge to the graph object
    for edge in G.edges():
        one, two = edge[0], edge[1]
        edge_label = str(self.trans_symbols[(one,two)])
        G.edges[(one,two)]['label'] = edge_label
           
    # convert the graph object to a PyDot object
    pydot_graph = nx.drawing.nx_pydot.to_pydot(G)

    # highlight the initial state node by filling it with yellow color
    pydot_graph.get_node(self.initial_state)[0].set_style('filled')
    pydot_graph.get_node(self.initial_state)[0].set('fillcolor','yellow')
    
    # set the peripheries (number of circles) of accepting state nodes to 2
    for i in self.accept_state:
        pydot_graph.get_node(i)[0].set('peripheries', '2')
        
    # if the initial state is also an accepting state, fill it with blue color
    if self.initial_state in self.accept_state:
        pydot_graph.get_node(self.initial_state)[0].set_style('filled')
        pydot_graph.get_node(self.initial_state)[0].set('fillcolor', 'blue')

    # Set the rank direction of the PyDot graph to left-to-right
    pydot_graph.set_rankdir('LR') 

    # save the PyDot graph as a PNG image
    pydot_graph.write_png('dfaSub.png', encoding="utf-8")
