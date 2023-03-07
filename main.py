from Thompson import Thompson
from ShuntingYard import ShuntingYard
from Simulation import Simulation
from Subconjuntos import construct_dfa
from DFA import nfa_to_dfa

if __name__=="__main__":
    expression = "a(a?b*|c+)b|baa"
    postfix = ShuntingYard(expression)
    nfa = Thompson(postfix)
    sim = Simulation(nfa) 

    # dfa = nfa_to_dfa(nfa)
    # print(dfa)