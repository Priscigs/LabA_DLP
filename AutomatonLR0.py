from Grammar import Grammar
from TokenCheck import *

def checkEquality(a,b):
    # Check if two dictionaries have the same keys and values
    if a.keys() != b.keys():
        return False

    for key, value in a.items():
        c = set(a[key])
        d = set(b[key])
        if c != d:
            return False

    return True

def multicheck(a_list, b):
    # Check if a list of dictionaries contains a dictionary equal to 'b'
    b_list = []
    for a in a_list:
        b_list.append(checkEquality(a, b))
    for i in range(len(b_list)):
        if b_list[i] == True:
            return True, i
    return False, -1

class Conjunto():
    def __init__(self, grammar: Grammar, numero, puntoS=None):
        # Initialize a Conjunto object
        self.number = numero
        self.grammar = grammar
        self.allprod = self.grammar.prod
        self.puntoS = puntoS or {}
        self.initial = list(self.puntoS.keys())[0]
        self.addDot()
        self.resto = self.Cerradura()
        self.newprod = self.newProducciones()

    def addDot(self):
        # Add a dot (.) before the first symbol in each production
        for key, value in self.allprod.items():
            for i in range(len(value)):
                if self.allprod[key][i][0] != '.':
                    self.allprod[key][i] = '.' + value[i]

    def Cerradura(self):
        # Compute the closure of the initial state
        puntoS = self.puntoS
        production = self.puntoS[self.initial][0]
        dot_idx = production.index('.')
        cerradura = {}

        if dot_idx < len(production) - 1:
            ini_lookat = production[dot_idx + 1]
            if ini_lookat not in self.grammar.terminals:
                stack = [ini_lookat]
                vistos = [ini_lookat]

                while stack:
                    lookat = stack.pop()

                    if lookat not in cerradura.keys():
                        cerradura[lookat] = []

                    if lookat in self.grammar.nonterminals:
                        cerradura[lookat].extend(self.allprod[lookat])
                        for i in self.allprod[lookat]:
                            idx = i.index('.')
                            if idx < len(i) - 1 and i[idx + 1] in self.grammar.nonterminals and i[idx + 1] not in vistos:
                                stack.append(i[idx + 1])
                                vistos.append(i[idx + 1])

        return cerradura

    def moveDot(self, prod):
        # Move the dot (.) one position to the right in a production
        if prod.replace('.', '') in self.grammar.tokens:
            idx = prod.index('.') + len(prod)
            prod = prod.replace('.', '')
            new_prod = prod[:idx] + '.' + prod[idx:]
        else:
            idx = prod.index('.')
            prod = prod.replace('.', '')
            new_prod = prod[:idx + 1] + '.' + prod[idx + 1:]
        return new_prod

    def newProducciones(self):
        # Combine the productions from the puntoS and resto dictionaries
        new_dict = {}
        for key, value in self.puntoS.items():
            if key in new_dict.keys():
                new_dict[key].extend(value)
            else:
                new_dict[key] = []
                new_dict[key].extend(value)

        for key, value in self.resto.items():
            if key in new_dict.keys():
                new_dict[key].extend(value)
            else:
                new_dict[key] = []
                new_dict[key].extend(value)

        return new_dict

    def go_to(self, X):
        # Compute the Ir_A (go-to) set for a given symbol X
        producciones = self.newprod
        new_puntoS = {}

        for key, value in producciones.items():
            for prod in value:
                if f'.{X}' in prod:
                    new_puntoS[key] = prod
        for key, prod in new_puntoS.items():
            new_puntoS[key] = [self.moveDot(prod)]

        return Conjunto(self.grammar, self.number + 1, puntoS=new_puntoS.copy())

class SyntaxAutomata():
    def __init__(self,initial_state, grammar):
        self.initial_state = initial_state
        self.conjuntos = [self.initial_state]
        self.grammar = grammar
        self.edges = {}
        self.generateAutomata()
        self.changeNumbers()
        self.changeEdges()
        self.tabla = self.CreateTable()

    def changeNumbers(self):
        for i in range(len(self.conjuntos)):
            self.conjuntos[i].number = i
            
    def changeEdges(self):
        edges = self.edges
        new_edges = {}

        visto = []
        
        #key -> tuple (conjunto1, conjunto2)
        #value -> transition_symbol
        for key, value in self.edges.items():
            a = key[0]
            b = key[1]
            vis = [i.newprod for i in visto]
            test =  multicheck(vis, key[0].newprod)
            
            if test[0]==False:
                visto.append(a)
            else:
                a = visto[test[1]]
                
            test = multicheck(vis, key[1].newprod)
            
            if test[0]==False:
                visto.append(b)
            else:
                b = visto[test[1]]
                
            new_edges[(a,b)] = value
            
        self.edges = new_edges.copy()

    def getConjuntos(self, conjunto: Conjunto):
        # Compute the Conjunto objects that can be reached from a given Conjunto
        c = conjunto
        g = c.grammar
        prod = conjunto.newprod
        vistos = []
        conjuntos = []

        for value in prod.values():
            for prod in value:
                if prod.replace('.', '') in g.tokens:
                    idx = prod.index('.')
                    if idx != len(prod) - 1:
                        if prod[idx + 1:] not in vistos:
                            vistos.append(prod[idx + 1:])
                            c2 = c.go_to(prod[idx + 1:])
                            conjuntos.append(c2)
                            self.edges[(c, c2)] = prod[idx + 1:]
                else:
                    idx = prod.index('.')
                    if idx != len(prod) - 1:
                        if prod[idx + 1] not in vistos:
                            vistos.append(prod[idx + 1])
                            c2 = c.go_to(prod[idx + 1])
                            conjuntos.append(c2)
                            self.edges[(c, c2)] = prod[idx + 1]

        return conjuntos

    def generateAutomata(self):
        # Generate the syntax automaton
        visitado = []
        stack = [self.initial_state]

        while stack:
            lookat = stack.pop()
            conjuntos = self.getConjuntos(lookat)
            for i in conjuntos:
                vis = [i.newprod for i in visitado]
                if multicheck(vis, i.newprod)[0] == False:
                    visitado.append(i)
                    stack.append(i)
                    self.conjuntos.append(i)

    def showEdges(self):
        count = 1
        for key, value in self.edges.items():
            print(f'Conjunto = {count}')
            # First item in the edge key
            print(f'1. {key[0].newprod}')
            # Second item in the edge key
            print(f'2. {key[1].newprod}')
            # Edge transition
            print(f'-> {value}')
            print('')
            count += 1

    def getTransitions(self, number):
        transiciones = {}
        for i in self.edges.keys():
            if i[0].number==number:
                transiciones[self.edges[i]] = i[1].number
        return transiciones
    
    def addEdge(self, number1, number2, transition):
        c = Conjunto(self.initial_state.grammar, number2)
        self.conjuntos.append(c)
        for i in self.conjuntos:
            if i.name == number1:
                c2 = i
        self.edges[(c2, c)] = transition
                
    def Simulation(self, entrada:list):
        grammar = self.grammar
        producciones = {}

        count = 1
        # Generating productions dictionary for grammar
        for key, value in [(key, value) for key,value in grammar.prod.items() if key!="E'"]:
            for i in value:
                productions = []
                if i !="ID":
                    for j in i:
                        productions.append(j)
                    producciones[count] = {key:productions}
                    count+=1
                else:
                    producciones[count] = {key: [i]}
                    count+=1
        e = entrada
        entrada.append("$")
        pila = [0]
        
        
        while True:
            action = self.tabla["Accion"][e[0]][pila[-1]]
            
            if action[0]=='s':
                # Shift operation
                pila.append(int(action[1:]))
                e = e[1:]
            elif action[0]=='r':
                num = int(action[1:])
                prod = producciones[num]
                key = list(prod.keys())[0]
                for i in range(len(prod[key])):
                    # Pop from stack
                    pila.pop()
                # Goto operation
                pila.append(self.tabla["Ir_a"][key][pila[-1]])
                
            elif action=='ACCEPT':
                return True
            else:
                # Error handling
                pila.append(action)
            
            if not entrada:
                return False
                
    def CreateTable(self):
        grammar = self.grammar
        
        producciones = {}
        
        count = 1
        # Generating productions dictionary for grammar
        for key, value in [(key, value) for key,value in grammar.prod.items() if key!="E'"]:
            for i in value:
                producciones[f'{key}->' + i] = count
                count+=1
        
        non_terminals = grammar.nonterminals
        terminals = grammar.terminals
        
        siguientes = {}
        
        for i in non_terminals: 
            # Calculate the follow set for each non-terminal
            siguientes[i] = list(Next(grammar, i))
        
        terminals.add('$')
        
        tabla = {}
        
        # Generate state numbers
        estados = [i for i in range(len(self.conjuntos))]
        
        tabla["Estados"] = estados
        
        tabla["Accion"] = {}
        
        tabla["go_to"] = {}
         
        for i in terminals:
            # Initialize action table with empty strings
            tabla["Accion"][i] = ["" for i in range(len(estados))]
            
        # Set accept state
        tabla["Accion"]['$'][1] = "ACCEPT"
            
        for i in non_terminals:
            # Initialize goto table with empty strings
            tabla["go_to"][i] = ["" for i in range(len(estados))]
        
        for i in tabla["Estados"]:
            trans = self.getTransitions(i)
            for terminal, conjunto in trans.items():
                if terminal in terminals:
                    # Set shift entries in the action table
                    tabla["Accion"][terminal][i] = f's{conjunto}'
                    
        for i in tabla["Estados"]:
            trans = self.getTransitions(i)
            for nonterminal, conjunto in trans.items():
                if nonterminal in non_terminals:
                    # Set goto entries in the goto table
                    tabla["go_to"][nonterminal][i] = conjunto
    
        for i in self.conjuntos:
            
            for encabezado, values in i.newprod.items():
                
                for prod in values:
                    if prod[-1] == '.' and i.number != 1:
                        
                        for key, value in siguientes.items():
                            
                            if key == encabezado:
                                for j in value:
                                    numero = producciones[f'{encabezado}->{prod[:-1]}']
                                    # Set reduce entries in the action table
                                    tabla["Accion"][j][i.number] = f'r{numero}'
                                    
        return tabla
    
    def print_table(self, table):
        estados = table["Estados"]
        accion = table["Accion"]
        ir_a = table["go_to"]

        terminales = list(accion.keys())
        no_terminales = list(ir_a.keys())

        print("Estados: ", end="")
        for terminal in terminales:
            # Print terminals with left alignment
            print(f"{terminal:<10}", end="")
        for no_terminal in no_terminales:
            # Print non-terminals with left alignment
            print(f"{no_terminal:<10}", end="")
        print()

        for estado in estados:
            # Print state number with left alignment
            print(f"{estado:<10}", end="")
            for terminal in terminales:
                # Print action entries with left alignment
                print(f"{accion[terminal][estado]:<10}", end="")
            for no_terminal in no_terminales:
                # Print goto entries with left alignment
                print(f"{ir_a[no_terminal][estado]:<10}", end="")
            print()

        
        # def print_table(tabla):
        #     estados = tabla["Estados"]
        #     accion = tabla["Accion"]
        #     ir_a = tabla["Ir_a"]
            
        #     # Imprimir encabezados de columnas
        #     print("Estados:", estados)
        #     print("Accion:")
        #     for terminal, valores in accion.items():
        #         print(f"\t{terminal}:", valores)
        #     print("Ir_a:")
        #     for no_terminal, valores in ir_a.items():
        #         print(f"\t{no_terminal}:", valores)

        # def print_table(self,tabla):
        #     # Imprimir encabezados de la tabla
        #     print("Estados:", end="\t")
        #     for terminal in tabla["Accion"]:
        #         print(terminal, end="\t")
        #     for nonterminal in tabla["Ir_a"]:
        #         print(nonterminal, end="\t")
        #     print()

        #     # Imprimir contenido de la tabla
        #     for estado in tabla["Estados"]:
        #         print(estado, end="\t")
        #         for terminal in tabla["Accion"]:
        #             print(tabla["Accion"][terminal][estado], end="\t")
        #         for nonterminal in tabla["Ir_a"]:
        #             print(tabla["Ir_a"][nonterminal][estado], end="\t")
        #         print()