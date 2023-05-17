from Automaton import Automata
from Thompson import Thompson
from State import State
from TokensReader import regexCreate

# Function to create automaton from a list of regular expressions
def create_automaton(regexes):
    afns = []

    for i in regexes:
        # Create a Thompson object for each regular expression
        afn = Thompson(i[1])  
        # Assign a token to the final state of the automaton
        afn.final[0].token = i[0]  
        # Add the automaton to the list of AFNs
        afns.append(afn)  

    starter = 1
    # Create a starting state for the NFA
    inicio = State('s0')  
    finals = []

    for i in afns:
        # Change the names of states in each automaton to avoid conflicts
        starter = i.changeNames(starter+1)  
        # Add the final state of each automaton to the list of final states
        finals.append(i.final[0])  
        # Add transitions from the starting state to the start state of each automaton
        inicio.AddTransition(i.start, 'ε')  

    return afns

# Function to simulate multiple automata on a given input string
def multisimul(afns, cadena):
    if afns:
        for i in afns:
            # Simulate the automaton on the input string
            ans = i.simulate2(cadena)  
            if ans[0] == True:
                # If a match is found, return the result
                return ans  
             # If no match is found in any automaton, return False
        return False 
    print("\n - No se pudo realizar la simulación")
    return

# Function to create automata from a regular expression file
def createReAfn(archivo):
    if regexCreate(archivo):
        # Create a list of regular expressions from the file
        afns = regexCreate(archivo)  
        # Create automata from the regular expressions
        return create_automaton(afns)  
    else:
        return
