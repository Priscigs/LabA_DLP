from Direct import Node, CreateSyntaxTree, printTree
from DFA import DFA

def Tree(regex):
    # Set the input regex
    s = regex
    # Create the syntax tree for the input regex
    root = CreateSyntaxTree(s)
    # Get the followpos table from the syntax tree
    followpos_table = root.getTable()    
    # Create the alphabet set from the followpos table
    alphabet = set([i[0] for i in followpos_table if i!="#"])
    # Initialize the transitions and states dictionaries
    transitions = {}  
    states = {} 
    # Create the start state as the set of positions for the first symbol in the input regex
    start_state = frozenset(followpos_table[0][2])
    # Set the start state as unprocessed in the states dictionary
    states[start_state] = False

    # Loop through the unprocessed states in the states dictionary
    while any(not processed for processed in states.values()):
        # Get the current unprocessed state
        current_state = None
        for state, processed in states.items():
            if not processed:
                current_state = state
                break

        # Mark the current state as processed in the states dictionary
        states[current_state] = True

        # Initialize the transitions for the current state
        transitions[current_state] = {}

        # Loop through the symbols in the alphabet
        for symbol in alphabet:
            # Initialize the set of next positions
            next_positions = set()
            # Loop through the positions in the current state
            for position in current_state:
                # Loop through the followpos entries in the followpos table
                for followpos_entry in followpos_table:
                    # If the followpos entry matches the current position and symbol,
                    # add the followpos entry's set of positions to the next positions set
                    if followpos_entry[1] == position and followpos_entry[0] == symbol:
                        next_positions |= followpos_entry[2]

            # If the next positions set is not empty, create a next state from it
            if next_positions:
                next_state = frozenset(next_positions)
                # If the next state is not already in the states dictionary, add it as unprocessed
                if next_state not in states:
                    states[next_state] = False
                # Add the transition from the current state with the symbol to the next state
                transitions[current_state][symbol] = next_state

    # Create a set of accepting states from the states dictionary
    accepting_states = set()
    for state in states.keys():
        # If the state contains the position at the end of the input regex, add it to the accepting states set
        if any(position == len(followpos_table) for position in state):
            accepting_states.add(state)
 
    # Initialize a count and contents dictionary for creating new state names
    count = 0
    contents = {}

    # Create new state names for each existing state and add them to the contents dictionary
    for key in set(transitions.keys()):
        contents[key] = f"q{count}"
        count+=1
        
    # Replace the next state in each transition with its new state name
    for key, value in transitions.items():
        for key2, value2 in value.items():
            transitions[key][key2] = contents[value2]
            
    # Make a copy of the transitions dictionary
    copy_keys = transitions.copy()
    
    for key in copy_keys.keys():
        transitions[contents[key]] = transitions[key]
        transitions.pop(key)

    # Updates the start state and accepting states with the new state names
    start_state = contents[start_state]
    new_accepting = set()
    for i in accepting_states:
        new_accepting.add(contents[i])
    accepting_states = new_accepting

    # Returns a DFA object with the updated start state, accepting states, and transitions
    return DFA(start_state, accepting_states, transitions)
