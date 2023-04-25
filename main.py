from Thompson import Thompson
from ShuntingYard import ShuntingYard
from SimulationNFA import SimulationNFA
from SimulationDFA import SimulationDFA
from Subconjuntos import *
from Tree import Tree
from TokensReader import regexCreate
from Reader import Reader
from analyzer import *
from TokensReader2 import *

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

    # DFA Direct
    afd2 = Tree(expression)
    #sim3 = SimulationDFA(afd2)

    # Lex file to read and give the regular definition
    # file = "YALex/slr-3.yal"

    # if regexCreate(file):
    #     regex = regexCreate(file)
    #     print(regex)

    # YALex
    # Reader()

    # Read file
    with open("YALex/input4yal.txt", "r") as archivo:
        archivo_input = archivo.read()

    # Token identifier
    analizar(archivo_input)

    # # leer el archivo de entrada
    # with open("Pruebas/input1.txt", "r") as f:
    #     input_text = f.read()

    # # llamar a la función para reescribir el archivo
    # rewritten_text = reescribir_archivo(input_text)

    # # imprimir la lista de valores resultante
    # if rewritten_text:
    #     values_list = get_values_list(rewritten_text)
    #     print("Lista de valores resultante:", values_list)
