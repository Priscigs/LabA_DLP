from shuntingYard import ShuntingY

class State:
    def __init__(self, label=None):
        self.transitions = {}
        self.label = label
    
    def add_transition(self, symbol, state):
        if symbol in self.transitions:
            self.transitions[symbol].append(state)
        else:
            self.transitions[symbol] = [state]
    
class NFA:
    def __init__(self, start_state, accept_states):
        self.start_state = start_state
        self.accept_states = accept_states

def thompson(input_str):
    stack = []
    for c in input_str:
        if c.isalnum():
            state = State(c)
            stack.append(state)
        elif c == '|':
            state1 = stack.pop()
            state2 = stack.pop()
            start_state = State()
            accept_state = State()
            start_state.add_transition('ε', state1)
            start_state.add_transition('ε', state2)
            state1.add_transition('ε', accept_state)
            state2.add_transition('ε', accept_state)
            stack.append(start_state)
        elif c == '.':
            state1 = stack.pop()
            state2 = stack.pop()
            state2.add_transition('ε', state1)
            stack.append(state2)
        elif c == '*':
            state = stack.pop()
            start_state = State()
            accept_state = State()
            start_state.add_transition('ε', state)
            start_state.add_transition('ε', accept_state)
            state.add_transition('ε', start_state)
            state.add_transition('ε', accept_state)
            stack.append(start_state)
        elif c == '+':
            state = stack.pop()
            start_state = State()
            accept_state = State()
            start_state.add_transition('ε', state)
            state.add_transition('ε', start_state)
            state.add_transition('ε', accept_state)
            stack.append(start_state)
        elif c == '?':
            state = stack.pop()
            start_state = State()
            accept_state = State()
            start_state.add_transition('ε', state)
            start_state.add_transition('ε', accept_state)
            state.add_transition('ε', accept_state)
            stack.append(start_state)
    nfa = NFA(stack[0], [State()])
    return nfa

def visualize_nfa(nfa):
    from graphviz import Digraph
    dot = Digraph()
    dot.node('start', shape='point')
    dot.edge('start', str(id(nfa.start_state)))
    for state in nfa.accept_states:
        dot.node(str(id(state)), shape='doublecircle')
    stack = [nfa.start_state]
    visited = set()
    while stack:
        state = stack.pop()
        if state in visited:
            continue
        visited.add(state)
        for symbol, next_states in state.transitions.items():
            for next_state in next_states:
                dot.edge(str(id(state)), str(id(next_state)), label=symbol)
                stack.append(next_state)
    return dot

# Ejemplo de uso
input_str = "(a*|b*).c"
postfix = ShuntingY(input_str)
print("Postfix:", postfix)
nfa = thompson(postfix)
dot = visualize_nfa(nfa)
dot.render('nfa.gv', view=True)
