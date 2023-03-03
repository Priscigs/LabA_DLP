class State:
    # The symbol class represents a symbol in a symbol machine, with a label and transitions to other symbols.

    # Initialize a new symbol with the given label (optional) and transitions (optional).
    def __init__(self, label: str = None, transitions: dict = None):
        # If no transitions are given, set transitions to an empty dictionary.
        self.transitions = transitions or {}
        
        # Set the label of the symbol.
        self.label = label
        
    # Add a new transition from this symbol to another symbol with a given state label.
    def add_transtition(self, symbol, state):
        # Check if there is already a transition to the given symbol.
        if symbol in self.transitions:
            # If there is, check if it's already a list of states or just a single state.
            if not isinstance(self.transitions[symbol], list):
                # If it's a single state, convert it to a list and append the new state.
                self.transitions[symbol] = [self.transitions[symbol]]
            self.transitions[symbol].append(state)
        else:
            # If there's no transition to the given symbol yet, add it with the given state label.
            self.transitions[symbol] = state
            
    def get_transitions(self):
        # Get all the transitions from this symbol as a dictionary of symbol labels to lists of state labels.
        return self.transitions
