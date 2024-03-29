import matplotlib.pyplot as plt
import networkx as nx
import pydot
from graphviz import Digraph
import os

def SimulationNFA(self): 
    # Initialize a list to store the edges
    self.edges = [] 
    # Initialize a dictionary to store the transition symbols
    self.trans_symbols = {} 
    
    # Loop over the transitions and their keys to extract the edges and their symbols
    for i in self.transitions:
        for j in self.transitions[i]:
            # If the transition leads to a state
            if self.transitions[i][j][0]=="q": 
                self.edges.append((i, self.transitions[i][j]))
                self.trans_symbols[(i,self.transitions[i][j])] = j
            # If the transition leads to multiple states
            else: 
                for k in self.transitions[i][j]:
                    self.edges.append((i,k))
                    self.trans_symbols[(i,k)] = j
    # Initialize a directed graph using NetworkX with left-to-right orientation                  
    G = nx.DiGraph(rankdir='LR') 
    # Add the edges to the graph
    G.add_edges_from(self.edges) 
    
    # Convert the graph to a PyDot graph
    pydot_graph = nx.drawing.nx_pydot.to_pydot(G) 
    
    # Loop over the nodes in the PyDot graph
    for node in pydot_graph.get_nodes(): 
        # Set the shape of each node to a circle
        node.set_shape('circle') 
        
    # Loop over the edges in the NetworkX graph
    for edge in G.edges():
        # Extract the two vertices of each edge
        one,two = edge[0], edge[1] 
        # Get the transition symbol associated with the edge
        edge_label = str(self.trans_symbols[(one,two)]) 
        # Create a PyDot edge with the transition symbol as the label
        pydot_edge = pydot.Edge(str(edge[0]), str(edge[1]), label=edge_label) 
        # Add the PyDot edge to the graph
        pydot_graph.add_edge(pydot_edge) 
        
    # Set some properties for specific nodes
    pydot_graph.get_node(self.initial_state.label)[0].set_style('filled')
    pydot_graph.get_node(self.initial_state.label)[0].set('fillcolor','yellow')
    pydot_graph.get_node(self.initial_state.label)[0].set('arrowhead','normal')
    pydot_graph.get_node(self.accept_state.label)[0].set('peripheries', '2')
    
    # Set the rank direction of the PyDot graph to left-to-right
    pydot_graph.set_rankdir('LR') 

    # Ruta completa de la carpeta donde deseas guardar el archivo
    folder_path = './outputsLabs'

    # Nombre del archivo
    file_name = 'nfaThompson.png'

    # Ruta completa del archivo
    file_path = os.path.join(folder_path, file_name)

    # Escribir el archivo PNG en la carpeta especificada
    pydot_graph.write_png(file_path, encoding='utf-8')

class Match:
    def __init__(self, nfa):
        self.nfa = nfa

    def match(self, input_string):
        current_states = set([self.nfa.initial_state])

        for symbol in input_string:
            next_states = set()

            for state in current_states:
                transitions = self.nfa.get_transitions(state)

                if transitions is not None and symbol in transitions:
                    next_states.update(transitions[symbol])

            if not next_states:
                return False

            current_states = next_states

        return any(state in self.nfa.accept_states for state in current_states)

