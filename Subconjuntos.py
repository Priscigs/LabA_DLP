from NFA import NFA
from State import State
from DFA import DFA

def epsilon_closure(states):
    """
    Computes the epsilon closure of a set of states.
    """
    closure = set(states)
    stack = list(states)
    
    while stack:
        state = stack.pop()
        for next_state, symbol in state.transitions.get("ε", []):
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)
    
    return closure

def move(states, symbol):
    """
    Computes the move of a set of states on a given symbol.
    """
    move = set()
    for state in states:
        for next_state, sym in state.transitions.get(symbol, []):
            move.add(next_state)
    
    return move

def construct_dfa(nfa):
    """
    Constructs the DFA equivalent to the given NFA.
    """
    initial_state = epsilon_closure([nfa.initial_state])
    dfa_states = {frozenset(initial_state): State()}
    unmarked = [initial_state]
    symbols = set(nfa.symbols)
    while unmarked:
        state_set = unmarked.pop(0)
        state = dfa_states[frozenset(state_set)]
        for symbol in symbols:
            next_set = epsilon_closure(move(state_set, symbol))
            if not next_set:
                continue
            if frozenset(next_set) not in dfa_states:
                dfa_states[frozenset(next_set)] = State()
                unmarked.append(next_set)
            next_state = dfa_states[frozenset(next_set)]
            state.add_transition(next_state, symbol)
    
    dfa = DFA(dfa_states[frozenset(initial_state)])
    for state_set, state in dfa_states.items():
        if nfa.accept_state in state_set:
            state.accept_state = True
    
    return dfa
