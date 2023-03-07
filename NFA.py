import State
import matplotlib.pyplot as plt
import networkx as nx
import pydot
from graphviz import Digraph

class NFA(): 
    def __init__(self, initial_state:State, accept_state:State) -> None:
        self.initial_state: State = initial_state
        self.accept_state: State = accept_state
        # Store the transition function of the NFA
        self.transitions = self.Transiciones() 
        # Initialize the list of edges for graph visualization
        self.edges = [] 
        # Initialize the dictionary of transition symbols for graph visualization
        self.trans_symbols  = {} 

    def Transiciones(self):
        stack = [self.initial_state]
        visited = []
        trans = {}
        while len(stack) != 0:
            # Pop an NFA state from the stack
            afn = stack.pop() 
            # Get its transition function
            transiciones = afn.transitions.items() 
            for key, value in transiciones:
                # If the state has not been visited before
                if afn not in visited: 
                    # Add the destination state to the stack for future processing
                    stack.append(key) 
                    
                    # Update the transition function for the current state
                    if afn.label in trans.keys():
                        # If the transition symbol is a list of symbols
                        if value is list: 
                            trans[afn.label] = {tuple(value): [key.label, anterior]}
                        else:
                            trans[afn.label] = {value: [key.label, anterior]}
                    else:
                        if value is list:
                            trans[afn.label] = {tuple(value): key.label}
                        else:
                            trans[afn.label] = {value: key.label}
                    # Keep track of the previous state visited
                    anterior = key.label
            # Mark the current state as visited
            visited.append(afn) 
        # Return the final transition function dictionary
        return trans

