from ShuntingYard import ShuntingYard
from State import State
from NFA import NFA

# This function converts a regular expression in infix notation to an NFA using Thompson's construction algorithm and shunting yard
def Thompson(input_str):
    # Initialize an empty stack
    stack = []
    for c in input_str:
        # If the character is alphanumeric, create a new state for it and push it onto the stack
        if c.isalnum():
            state = State(c)
            stack.append(state)
        # If the character is '|', pop the top two states off the stack, create a new start state 
        # and accept state, and add ε-transitions from the start state to the two popped states 
        # and from the two popped states to the accept state. Then push the start state onto
        # the stack.
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
        # If the character is '.', pop the top two states off the stack and add an ε-transition 
        # from the second popped state to the first popped state. Then push the second popped 
        # state onto the stack.
        elif c == '.':
            state1 = stack.pop()
            state2 = stack.pop()
            state2.add_transition('ε', state1)
            stack.append(state2)
        # If the character is '*', pop the top state off the stack, create a new start state 
        # and accept state, and add ε-transitions from the start state to the popped state 
        # and from the popped state to the start and accept states. Then push the start 
        # state onto the stack.
        elif c == '*':
            state = stack.pop()
            start_state = State()
            accept_state = State()
            start_state.add_transition('ε', state)
            start_state.add_transition('ε', accept_state)
            state.add_transition('ε', start_state)
            state.add_transition('ε', accept_state)
            stack.append(start_state)
        # If the character is '+', pop the top state off the stack, create a new start state 
        # and accept state, and add ε-transitions from the start state to the popped state 
        # and from the popped state to the start and accept states. Then push the start 
        # state onto the stack.
        elif c == '+':
            state = stack.pop()
            start_state = State()
            accept_state = State()
            start_state.add_transition('ε', state)
            state.add_transition('ε', start_state)
            state.add_transition('ε', accept_state)
            stack.append(start_state)
        # If the character is '?', pop the top state off the stack, create a new start state 
        # and accept state, and add ε-transitions from the start state to the popped state 
        # and from the popped state to the accept state. Then push the start state onto 
        # the stack.
        elif c == '?':
            state = stack.pop()
            start_state = State()
            accept_state = State()
            start_state.add_transition('ε', state)
            start_state.add_transition('ε', accept_state)
            state.add_transition('ε', accept_state)
            stack.append(start_state)

    # The final state on the stack is the start state of the NFA, 
    # and we create a new accept state for the NFA
    nfa = NFA(stack[0], [State()])
    return nfa