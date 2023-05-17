import State
import matplotlib.pyplot as plt
import networkx as nx
import pydot
from graphviz import Digraph

class Automata():
    def __init__(self, start: State, final:State) -> None:
        self.start: State = start
        self.final: list = [final]
        self.transitions = self.Transiciones()
        self.edges = []
        self.trans_symbols  = {}
        self.alphabet = []
        
    def show(self):
        # Display the transitions of the automaton
        stack = [self.start]
        visited = []
        while len(stack) != 0:
            afn = stack.pop()
            transiciones = afn.transitions.items()

            for key, value in transiciones:
                if afn not in visited:
                    stack.append(key)
                    print(afn.name, "-->",value,"-->", key.name)
            visited.append(afn)

    def Transiciones(self):
        # Compute the transition dictionary of the automaton
        stack = [self.start]
        visited = []
        trans = {}
        while len(stack) != 0:
            afn = stack.pop()
            transiciones = afn.transitions.items()
            for key, value in transiciones:
                if afn not in visited:
                    stack.append(key)
                    if afn.name in trans.keys():
                        if value is list:
                            trans[afn.name] = {tuple(value): [key.name, anterior]}
                        else:
                            trans[afn.name] = {value: [key.name, anterior]}
                    else:
                        if value is list:
                            trans[afn.name] = {tuple(value): key.name}
                        else:
                            trans[afn.name] = {value: key.name}
                anterior = key.name
                    
            visited.append(afn)
                
        return trans
    
    def getInfo(self):
        # Retrieve information about edges and transition symbols for visualization
        self.edges = []
        self.trans_symbols = {}
            
        for i in self.transitions:
            for j in self.transitions[i]:
                if self.transitions[i][j][0]=="s":
                    self.edges.append((i, self.transitions[i][j]))
                    self.trans_symbols[(i,self.transitions[i][j])] = j
                else:
                    for k in self.transitions[i][j]:
                        self.edges.append((i,k))
                        self.trans_symbols[(i,k)] = j
        
    def ShowGraph(self, name="graph.png"):
        # Display the automaton as a graph using networkx and pydot
        self.getInfo()
        G = nx.DiGraph()
        G.add_edges_from(self.edges)

        pydot_graph = nx.drawing.nx_pydot.to_pydot(G)

        for edge in G.edges():
            one,two = edge[0], edge[1]
            edge_label = str(self.trans_symbols[(one,two)])
            pydot_edge = pydot.Edge(str(edge[0]), str(edge[1]), label=edge_label)
            pydot_graph.add_edge(pydot_edge)
            
        pydot_graph.get_node(self.start.name)[0].set_style('filled')
        pydot_graph.get_node(self.start.name)[0].set('fillcolor','green')
        
        pydot_graph.get_node(self.final[0].name)[0].set_style('filled',)
        pydot_graph.get_node(self.final[0].name)[0].set('fillcolor','red')
        pydot_graph.write_png(name, encoding="utf-8")
        
    def ShowGraph2(self, name = "graph"):
        # Display the automaton as a graph using graphviz and Digraph
        self.getInfo()
        
        final_names = [i.name for i in self.final]
        dot = Digraph()
        for state in self.getStates():
            if state in final_names:
                dot.node(str(state), shape="doublecircle")
            else:
                dot.node(str(state), shape="circle")
        for edge in self.edges:
            dot.edge(str(edge[0]), str(edge[1]), label=str(self.trans_symbols[(edge[0],edge[1])]))
        dot.render(name, format='pdf', view=True, cleanup=True)

    def getAplhabet(self):
        # Get the alphabet of the automaton
        alphabet = []
        for transitions in self.transitions.values():
            for character in transitions.keys():
                if character not in alphabet and character!="ε":
                    alphabet.append(character)
        return alphabet
    
    def getStates(self):
        # Get the states of the automaton
        states = list(self.transitions.keys())
        states.extend(self.final.name)
        return states
            
    
    def subconjuntos(self):
        # Compute the subconjuntos of the automaton
        stack = []
        visited = []
        trans = {}

        while len(stack) != 0:
            afn = stack.pop()
            
            transiciones = afn.transitions.items()

            for key, value in transiciones:
                if afn not in visited:
                    stack.append(key)
                    if afn.name in trans.keys():
                        trans[afn.name] = {value: [key.name, anterior]}
                    else:
                        trans[afn.name] = {value: key.name}
                anterior = key.name
                    
            visited.append(afn)
                
        return trans
    
    def simulate(self, input_str):
        # Simulate the automaton for the given input string
        current_states = set(Closure(self.transitions, self.start.name))

        for symbol in input_str:
            next_states = set()
            
            for state in current_states:
                next_states.update(get_groups(self.transitions, state, symbol))

            current_states = set()
            for state in next_states:
                current_states.update(Closure(self.transitions, state))
        return  self.final[0].name in current_states
    
    def simulate2(self, input_str):
        # Simulate the automaton for the given input string
        input_str = input_str.replace("\\n", "↓").replace("\\t", "→").replace("\\r", "↕").replace("\\s", "↔").replace(".","▪").replace(" ", "□")
        input_str = input_str.replace("＋", "+")
        current_states = set(Closure(self.transitions, self.start.name))        

        for symbol in input_str:   
            next_states = set()
            next_states.update(multimove(self.transitions, current_states, symbol))
            current_states = set()
            for state in next_states:
                current_states.update(Closure(self.transitions, state))

        final_names = [i.name for i in self.final]

        for i in final_names:
            if i in current_states:
                idx = final_names.index(i)
                return True, self.final[idx].token
        return  False, None
        
    def changeNames(self, start):
        # Change the names of the automaton states
        stack = [self.start]
        visited = [self.start]
        counter = start
        while stack:
            lookat = stack.pop()
            estados = lookat.GetTransitionStates()
            if estados:
                for i in estados:
                    if i not in visited:
                        visited.append(i)
                        stack.append(i)
                lookat.name = f"s{counter}"
            counter+=1
        self.transitions = self.Transiciones()
        return counter

def Closure(transiciones: dict, state: str):
    # Compute the epsilon closure of a state in the automaton
    epsilon = "ε"
    visited = {state}
    stack = [state]
    
    while stack:
        estado = stack.pop()
        if estado in transiciones and epsilon in transiciones[estado]:
            epsilon_transitions = transiciones[estado][epsilon]
            if isinstance(epsilon_transitions, list):
                for t in epsilon_transitions:
                    if t not in visited:
                        stack.append(t)
                        visited.add(t)
            else:
                if epsilon_transitions not in visited:
                    stack.append(epsilon_transitions)
                    visited.add(epsilon_transitions)
    return visited

def multimove(transiciones: dict, estados:list, character: str):
    # Get the states that can be reached from a set of states with a given input character
    group = set()
    for i in estados:
        if i in transiciones and character in transiciones[i]:
            if isinstance(transiciones[i][character], list):
                group.update(transiciones[i][character])
            else:
                group.add(transiciones[i][character])
    return group

def get_groups(transiciones: dict, estados:list, character: str):
    # Get the epsilon closure of the states that can be reached from a set of states with a given input character
    group = set()
    for i in estados:
        if i in transiciones and character in transiciones[i]:
            if isinstance(transiciones[i][character], list):
                group.update(transiciones[i][character])
            else:
                group.add(transiciones[i][character])
    closure_states = set()
    for state in group:
        closure_states.update(Closure(transiciones, set(state)))
    return closure_states
