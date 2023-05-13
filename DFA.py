import State
import matplotlib.pyplot as plt
import networkx as nx
from pythomata import SimpleDFA
import pydot
from collections import deque
from queue import Queue
from graphviz import Digraph

class DFA():
    def __init__(self, initial_state: str, accept_state:list, transitions: dict) -> None:
        # Store the initial state, accept states, and transition function of the DFA
        self.initial_state: str = initial_state
        self.accept_state: set = accept_state
        self.transitions = transitions
        # Initialize the list of edges for graph visualization
        self.edges = []
        # Initialize the dictionary of transition symbols for graph visualization
        self.trans_symbols  = {}
        # Get the alphabet of the DFA
        self.alfabeto = self.getAlphabet()

    def getInfo(self):
        self.edges = []
        self.trans_symbols = {}
        for i in self.transitions:
            for j in self.transitions[i]:
                if (i, self.transitions[i][j]) in self.trans_symbols.keys():
                    self.trans_symbols[(i,self.transitions[i][j])] += ", " + j
                else:
                    self.edges.append((i, self.transitions[i][j]))
                    self.trans_symbols[(i,self.transitions[i][j])] = " " + j
        
    def SimulationTree(self, name = "graph"):
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
            dot.edge(str(edge[0]), str(edge[1]), label=str(self.trans_symbols[(edge[0],edge[1])]))
        dot.render(name, format='png', view=True)
    
    def getStates(self):
        # Get all states of the DFA
        states = set(self.transitions.keys())
        for value in self.transitions.values():
            states.update(value.values())
        return states
            
    def getAlphabet(self):
        # Get the alphabet of the DFA
        alphabet = set()
        for transitions in self.transitions.values():
            for character in transitions.keys():
                alphabet.update(character)
        return alphabet
    
    def count_instances(self, matrix):
        # Count the number of X's in the matrix
        count = 0
        for row in matrix:
            for element in row:
                if element == "X":
                    count +=1
        return count
    
    def check_transitions(self, matrix, states):
        # Check if the two given states can be marked in the matrix
        est1, est2  = states
        
        # Indices where the states can be marked
        idx1 = int(est1[1:])
        idx2 = int(est2[1:])
        
        # Get the alphabet of the DFA
        alfabeto = self.getAplhabet()
        
        # Find the states to which est1 and est2 transition for each symbol in the alphabet
        trans1 = self.transitions[est1]
        trans2 = self.transitions[est2]
        
        for i in alfabeto:
            if i in trans1.keys() and i in trans2.keys():
                # Find the indices of the states to which est1 and est2 transition for symbol i
                indice1 = int(trans1[i][1:])
                indice2 = int(trans2[i][1:])
                
                print(f"{est1} ==> {i} ==> {trans1[i]}")
                print(f"{est2} ==> {i} ==> {trans2[i]}\n")
                
                print(matrix[indice1])
                print(matrix[indice1][indice2])
                
                # If the cell in the matrix at row indice1 and column indice2 is already marked, 
                # mark the cell at row idx1 and column idx2
                if matrix[indice1][indice2]=="X":
                    matrix[idx1][idx2]="X"
                
    def simulate(self, regex):
        # Simulate the DFA on the given regex
        state = self.initial_state
        for char in regex:
            if char not in self.transitions[state].keys():
                return False
            state = self.transitions[state][char]
        return state in self.accept_state        
        
    def transition_function(self, state, symbol):
        # Get the state to which the DFA transitions from the given state on the given symbol
        if symbol in self.transitions[state].keys():
            return self.transitions[state][symbol]
        else:
            return None
