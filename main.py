from Thompson import Thompson
from ShuntingYard import ShuntingYard
from SimulationNFA import SimulationNFA
from SimulationDFA import SimulationDFA
from Subconjuntos import *
from Reader import Reader
from analyzer import *
from TokensReader import *

if __name__ == "__main__":

    # Regular Expression
    expression = "ab*ab*"

    # Using Shunting Yard Algorithm for infix to postfix
    postfix = ShuntingYard(expression)

    # NFA Thompson
    nfa = Thompson(postfix)
    sim = SimulationNFA(nfa) 

    # DFA Sub
    afd = Subconjuntos(nfa)
    sim2 = SimulationDFA(afd)

    # Lex file to read and give the regular definition
    file = "YALex/slr-3.yal"

    if regexCreate(file):
        regex = regexCreate(file)

    # YALex
    Reader()

    # Read file
    main()
