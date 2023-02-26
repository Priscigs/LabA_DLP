from graphviz import Digraph

def Simulation(nfa):

    # Create a new directed graph
    dot = Digraph()
    dot.node('start', shape='point')

    # Add a directed edge from the starting node to the initial state of the NFA
    dot.edge('start', str(id(nfa.initial_state)))

    # Add a double circle node for each accept state in the NFA
    for state in nfa.accept_states:
        dot.node(str(id(state)), shape='doublecircle')

    # Create a stack with the initial state of the NFA
    stack = [nfa.initial_state]
    # Create a set to keep track of visited states
    visited = set()
    # Traverse the NFA using depth-first search
    while stack:
        # Pop the top state from the stack
        state = stack.pop()
        # If the state has already been visited, skip it
        if state in visited:
            continue
        # Add the state to the set of visited states
        visited.add(state)
        # For each transition from the current state, add a directed edge to the next state
        for symbol, next_states in state.transitions.items():
            for next_state in next_states:
                dot.edge(str(id(state)), str(id(next_state)), label=symbol)
                # Add the next state to the stack
                stack.append(next_state)
    return dot