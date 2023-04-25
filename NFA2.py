from pyformlang.regular_expression import Regex
from graphviz import Digraph

# Convert a regular expression string to an ENFA
def regex_to_enfa(regex_str):
    regex = Regex(regex_str)
    return regex.to_epsilon_nfa()

# Convert an ENFA to a Graphviz graph
# The identifier parameter is used to label final states with an identifier (e.g., a category)
def Simulate_epsilonNFA(enfa, identifier=None):
    # Create a new graph with the name "ENFA"
    graph = Digraph("ENFA", format="png")
    # Set the layout direction of the graph
    graph.attr(rankdir="LR")

    # Add a circle node for each state in the ENFA
    graph.attr("node", shape="circle")
    for state in enfa.states:
        graph.node(str(state))

    # Add a filled circle node for the start state
    graph.attr("node", shape="circle", style="filled", fillcolor="yellow")
    graph.node(str(enfa._start_state))

    # Add a double circle node for each final state
    graph.attr("node", shape="doublecircle")
    for final_state in enfa.final_states:
        if identifier is not None:
            label = f"{final_state} ({identifier})"
        else:
            label = str(final_state)
        graph.node(str(final_state), label=label)

    # Add an edge for each transition in the ENFA
    for from_state, to_dict in enfa._transition_function._transitions.items():
        for symbol, to_states in to_dict.items():
            for to_state in to_states:
                graph.edge(str(from_state), str(to_state), label=str(symbol))

    return graph

# Generate a graph of multiple ENFAs combined into one
# The identifiers parameter is used to label final states with an identifier (e.g., a category)
def Simulate_megautomata(enfas, identifiers=None):
    # Create a new graph with the name "Combined_ENFA"
    mega_graph = Digraph("Combined_ENFA", format="png")
    # Add a filled circle node for the starting state
    mega_start_state = "MegaStart"
    mega_graph.attr(rankdir="LR")
    mega_graph.attr("node", shape="circle", style="filled", fillcolor="yellow")
    mega_graph.node(str(mega_start_state))

    # Initialize the state mapping with the current maximum state
    current_max_state = 0

    for idx, enfa in enumerate(enfas):
        # Increment the maximum state for each ENFA
        current_max_state += 1
        # Set the offset for the current ENFA
        offset = current_max_state

        # Create a mapping of old states to new states
        state_mapping = {}

        # Add a circle node for each state in the current ENFA
        for state in enfa.states:
            new_state = current_max_state
            state_mapping[state] = new_state
            mega_graph.node(str(new_state))
            current_max_state += 1

        # Add an edge for each transition in the current ENFA
        for from_state, to_dict in enfa._transition_function._transitions.items():
            for symbol, to_states in to_dict.items():
                for to_state in to_states:
                    mega_graph.edge(str(state_mapping[from_state]), str(state_mapping[to_state]), label=str(symbol))

        # Add a double circle node for each final state in the current ENFA
        mega_graph.attr("node", shape="doublecircle")
        for final_state in enfa.final_states:
            if identifiers is not None:
                label = f"{state_mapping[final_state]} ({identifiers[idx]})"
            else:
                label = str(state_mapping[final_state])
            mega_graph.node(str(state_mapping[final_state]), label=label)

        for start_state in enfa._start_state:
            mega_graph.edge(str(mega_start_state), str(state_mapping[start_state]), label="ε")

    return mega_graph
