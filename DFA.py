from typing import Set, Tuple
from State import State
import networkx as nx
import matplotlib.pyplot as plt
from NFA import NFA

class DFA:
    def __init__(self, start_state: State, states: Set[State], accept_states: Set[State], 
                alphabet: Set[str], transitions: dict) -> None:
        self.start_state = start_state
        self.states = states
        self.accept_states = accept_states
        self.alphabet = alphabet
        self.transitions = transitions

    def to_graph(self):
        G = nx.DiGraph()
        G.add_nodes_from(self.states)
        G.add_edges_from(self.transitions.keys())
        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(self.states, pos)
        nx.draw_networkx_edges(G, pos)
        nx.draw_networkx_labels(self.states, pos)
        plt.show()

def epsilon_closure(state: State) -> Set[State]:
    closure = set()
    stack = [state]
    while stack:
        current_state = stack.pop()
        closure.add(current_state)
        for symbol, states in current_state.transitions.items():
            if symbol is None:
                for s in states:
                    if s not in closure:
                        stack.append(s)
    return closure

def move(states: Set[State], symbol: str) -> Set[State]:
    move_set = set()
    for state in states:
        if symbol in state.transitions:
            move_set |= set(state.transitions[symbol])
    return move_set

def nfa_to_dfa(nfa: NFA) -> DFA:
    alphabet = set()
    for state in nfa.states:
        alphabet |= set(state.transitions.keys())

    start_state = frozenset(epsilon_closure(nfa.initial_state))
    dfa_states = set()
    dfa_transitions = {}
    dfa_accept_states = set()

    unmarked_states = [start_state]
    while unmarked_states:
        current_state = unmarked_states.pop(0)
        dfa_states.add(current_state)

        for symbol in alphabet:
            next_state = frozenset(epsilon_closure(State.transitions_to_states(nfa.transitions, move(current_state, symbol))))
            dfa_transitions[(current_state, symbol)] = next_state

            if next_state not in dfa_states:
                unmarked_states.append(next_state)

        if any(state in nfa.accept_states for state in current_state):
            dfa_accept_states.add(current_state)

    dfa = DFA(start_state, dfa_states, dfa_accept_states, alphabet, dfa_transitions)

    return dfa
