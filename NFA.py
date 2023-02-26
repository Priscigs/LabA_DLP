class NFA:
    def __init__(self, initial_state, accept_states):
        # Initial state and accept state
        self.initial_state = initial_state
        self.accept_states = accept_states