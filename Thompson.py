import re
from State import State
from NFA import NFA

# This function converts a regular expression in infix notation to an NFA 
# using Thompson's construction algorithm and shunting yard
def Thompson(expression):

    # Initialize an empty stack
    stack = []

    # ++ to the name of the state.
    contador = 0
    
    for c in expression:
        
        # If the character is '|', pop the top two states off the stack, create a new initial_state state 
        # and accept state, and add ε-transitions from the initial_state state to the two popped states 
        # and from the two popped states to the accept state. Then push the initial_state state onto
        # the stack.
        if c == "|":
            start_state = State(label = f'q{contador}')
            contador+=1
            end = State(label = f'q{contador}')
            state1 = stack.pop()
            state2 = stack.pop()
            start_state.add_transtition(state1.initial_state, "ε")
            start_state.add_transtition(state2.initial_state, "ε") 
            state1.accept_state.add_transtition(end, "ε")  
            state2.accept_state.add_transtition(end, "ε")    
            afn = NFA(start_state, end)
            stack.append(afn)
            
        # If the character is '.', pop the top two states off the stack and add an ε-transition 
        # from the second popped state to the first popped state. Then push the second popped 
        # state onto the stack.
        elif c == ".":
            state1 = stack.pop()
            state2 = stack.pop()
            state2.accept_state.transitions = state1.initial_state.transitions
            afn = NFA(state2.initial_state, state1.accept_state)
            stack.append(afn)
        
        # If the character is '*', pop the top state off the stack, create a new initial_state state 
        # and accept state, and add ε-transitions from the initial_state state to the popped state 
        # and from the popped state to the initial_state and accept states. Then push the initial_state 
        # state onto the stack.
        elif c == "*":
            start_state = State(label = f'q{contador}')
            contador+=1
            end = State(label = f'q{contador}')
            state1 = stack.pop()
            start_state.add_transtition(state1.initial_state, "ε")
            state1.accept_state.add_transtition(state1.initial_state, "ε")
            state1.accept_state.add_transtition(end, "ε")
            start_state.add_transtition(end, "ε")
            afn = NFA(start_state, end)
            stack.append(afn)
            
        # If the character is '+', pop the top state off the stack, create a new initial_state state 
        # and accept state, and add ε-transitions from the initial_state state to the popped state 
        # and from the popped state to the initial_state and accept states. Then push the initial_state 
        # state onto the stack.
        elif c == "+":
            start_state = State(label = f'q{contador}')
            contador+=1
            end = State(label = f'q{contador}')
            state1 = stack.pop()
            start_state.add_transtition(state1.initial_state, "ε")
            state1.accept_state.add_transtition(state1.initial_state, "ε")
            state1.accept_state.add_transtition(end, "ε")
            afn = NFA(start_state, end)
            stack.append(afn)
            
        # If the character is '?', pop the top state off the stack, create a new initial_state state 
        # and accept state, and add ε-transitions from the initial_state state to the popped state 
        # and from the popped state to the accept state. Then push the initial_state state onto 
        # the stack.
        elif c == "?":
            start_state = State(label = f'q{contador}')
            contador+=1
            end = State(label = f'q{contador}')
            state1 = stack.pop()
            start_state.add_transtition(state1.initial_state, "ε")
            state1.accept_state.add_transtition(end, "ε")
            start_state.add_transtition(end, "ε")
            afn = NFA(start_state, end)
            stack.append(afn)

        # The accept_state state on the stack is the initial_state state of the NFA, 
        # and we create a new accept state for the NFA
        else:
            start_state = State(label = f'q{contador}')
            contador+=1
            end = State(label = f'q{contador}')
            start_state.add_transtition(end, c)

            afn = NFA(initial_state = start_state, accept_state = end)
            stack.append(afn)
        if c!=".":
            contador +=1
    return stack.pop()