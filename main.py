from Thompson import Thompson
from ShuntingYard import ShuntingYard
from Simulation import Simulation

if __name__=="__main__":
    expression = "(a|b)*abb"
    postfix = ShuntingYard(expression)
    nfa = Thompson(postfix)
    sim = Simulation(nfa)