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
    
    def getAplhabet(self):
        alphabet = []
        for transitions in self.transitions.values():
            for character in transitions.keys():
                if character not in alphabet and character!="ε":
                    alphabet.append(character)
        return alphabet
    
    def simulate2(self, input_str):
        # Replace special characters with corresponding symbols
        input_str = input_str.replace("\\n", "↓").replace("\\t", "→").replace("\\r", "↕").replace("\\s", "↔").replace(".", "▪").replace(" ", "□")
        input_str = input_str.replace("＋", "+")
        
        # Initialize current states with the closure of the initial state
        current_states = set(Closure(self.transitions, self.initial_state.label))

        # Process each symbol in the input string
        for symbol in input_str:
            next_states = set()
            # Perform multimove for each current state and symbol
            next_states.update(multimove(self.transitions, current_states, symbol))
            current_states = set()
            # Update current states with the closure of the next states
            for state in next_states:
                current_states.update(Closure(self.transitions, state))

        final_names = [i.label for i in self.accept_state]

        # Check if any of the current states is a final state
        for i in final_names:
            if i in current_states:
                idx = final_names.index(i)
                return True, self.accept_state[idx].token
        return False, None

    def changeNames(self, initial_state):
        stack = [self.initial_state]
        visited = [self.initial_state]
        counter = initial_state

        # Perform depth-first search to change state names
        while stack:
            lookat = stack.pop()

            estados = lookat.GetTransitionStates()

            if estados:
                for i in estados:
                    if i not in visited:
                        visited.append(i)
                        stack.append(i)
                # Change state name to s[counter]
                lookat.label = f"s{counter}"
            counter += 1

        self.transitions = self.Transiciones()
        return counter

def Closure(transiciones: dict, state: str):
    epsilon = "ε"
    visited = {state}
    stack = [state]

    # Compute the closure of the given state using epsilon transitions
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

def multimove(transiciones: dict, estados: list, character: str):
    group = set()
    # Perform multimove for each state in the given list of states and symbol
    for i in estados:
        if i in transiciones and character in transiciones[i]:
            if isinstance(transiciones[i][character], list):
                group.update(transiciones[i][character])
            else:
                group.add(transiciones[i][character])
    return group
