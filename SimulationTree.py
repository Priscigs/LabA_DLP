from graphviz import Digraph
from DFA import *

def SimulationTree(self, name="graph", folder_path="./outputsLabs"):
    self.getInfo()
    dot = Digraph()
    for state in self.getStates():
        if state in self.accept_state:
            dot.node(str(state), shape="doublecircle")
        elif state == self.initial_state:
            dot.node(str(state), style="bold")
        else:
            dot.node(str(state), shape="circle")
    for edge in self.edges:
        dot.edge(str(edge[0]), str(edge[1]), label=str(self.trans_symbols[(edge[0], edge[1])]))
    file_path = f"{folder_path}/{name}"
    dot.render(file_path, format='png')
