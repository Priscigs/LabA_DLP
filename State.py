class State:
    def __init__(self, label = None):
        # Transitions in a dictionary
        self.transitions = {}
        self.label = label
    
    def add_transition(self, symbol, state):
        if symbol in self.transitions:
            self.transitions[symbol].append(state)
        else:
            self.transitions[symbol] = [state]