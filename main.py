from Thompson import Thompson
from ShuntingYard import ShuntingYard
from SimulationNFA import SimulationNFA
from SimulationDFA import SimulationDFA
from SimulationTree import SimulationTree
from SimulationLR0 import SimulationLR0
from Grammar import Grammar
from TokensReader import regexCreate, rules
from CreateAut import createReAfn
from AutomatonLR0 import Conjunto, SyntaxAutomata
from TokenCheck import *
from Subconjuntos import *
from TokensReader import *
from TreeContinue import *
from Automaton import *

if __name__ == "__main__":

    # LAB B

    # Regular Expression
    expression = "a(a?b*|c+)b|bba"

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

    ## LAB D NO TERMINADO

    if regexCreate(file):
        regex = regexCreate(file)

        # LAB C

        dfa = TreeToDFA(regex)
        dfa2 = SimulationTree(dfa)

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

    # LAB E

    if(prod:=readYalp('Yapar/slr-1.yalp')):
        afn = rules('YALex/slr-1.yal')
        if(checkTokens(afn[1].values(), prod[1])):
            g = Grammar(*prod)
            print(" ")
            print('No Terminales: ', g.nonterminals)
            print('Terminales: ', g.terminals)
            print('Producciones: ', g.prod)
            print('Tokens: ', g.tokens)
            print('Inicial: ', g.initial)
            print(" ")
            
            g.AugmentedGrammar()
            
            c0 = Conjunto(g, 0, puntoS={g.initial: g.prod[g.initial]})

            a1 = SyntaxAutomata(c0)
            
            a2 = SimulationLR0(a1)
        else:
            print('Los tokens no son iguales entre archivos')