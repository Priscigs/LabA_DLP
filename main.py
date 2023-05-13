from Thompson import Thompson
from ShuntingYard import ShuntingYard
from SimulationNFA import SimulationNFA
from SimulationDFA import SimulationDFA
from SimulationTree import SimulationTree
from Subconjuntos import *
from TokensReader import *
from TreeContinue import *
from Automaton import *

if __name__ == "__main__":

    # # Regular Expression
    # expression = "ab*ab*"

    # # Using Shunting Yard Algorithm for infix to postfix
    # postfix = ShuntingYard(expression)

    # # NFA Thompson
    # nfa = Thompson(postfix)
    # sim = SimulationNFA(nfa) 

    # # DFA Sub
    # afd = Subconjuntos(nfa)
    # sim2 = SimulationDFA(afd)

    # Lex file to read and give the regular definition
    file = "YALex/slr-4.yal"

    if regexCreate(file):
        regex = regexCreate(file)

        # dfa = TreeToDFA(regex)
        # dfa2 = SimulationTree(dfa)

        with open('Scanner.py', 'w', encoding="utf-8") as file:
            file.write("from DFA import DFA\n")
            file.write("from Thompson import Thompson\n")
            file.write("\n")
            file.write(f"reg = '{regex}'\n")
            file.write(f"nfa = Thompson(reg)\n")
            file.write("txt_input = 'inputYalex.txt'\n")
            file.write("lines = []\n")
            file.write("tokens = []\n")
            file.write("\n")
            file.write("with open('inputYalex.txt', 'r', encoding='utf-8') as file:\n")
            file.write("\tlines = file.readlines()\n")
            file.write("\n")
            file.write("lines = [i.strip() for i in lines]\n")
            file.write("errors = []\n")
            file.write("\n")
            file.write("for i in range(len(lines)):\n")
            file.write("\tif nfa.simulate2(lines[i]) == False:\n")
            file.write("\t\terrors.append(f'Syntax error on line {i} -> {lines[i]}')\n")
            file.write("\telse:\n")
            file.write("\t\ttokens.append(lines[i])\n")
            file.write("\n")
            file.write("if errors:\n")
            file.write("\tfor i in errors:\n")
            file.write("\t\tprint(i)\n")
            file.write("else:\n")
            file.write("\tprint('Program has no syntax errors')\n")
            file.write("\tfor i in tokens:\n")
            file.write("\t\tprint('token: ', i)\n")

