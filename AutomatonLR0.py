from Grammar import Grammar

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

    def Ir_A(self, X):
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
    def __init__(self, initial_state):
        # Initialize a SyntaxAutomata object
        self.initial_state = initial_state
        self.conjuntos = [self.initial_state]
        self.edges = {}
        self.generateAutomata()
        self.changeNumbers()
        self.changeEdges()

    def changeNumbers(self):
        # Update the numbers of the Conjunto objects
        for i in range(len(self.conjuntos)):
            self.conjuntos[i].number = i

    def changeEdges(self):
        # Update the edges of the automaton with the updated Conjunto objects
        edges = self.edges
        new_edges = {}
        visto = []

        for key, value in self.edges.items():
            a = key[0]
            b = key[1]
            vis = [i.newprod for i in visto]
            test = multicheck(vis, key[0].newprod)

            if test[0] == False:
                visto.append(a)
            else:
                a = visto[test[1]]

            test = multicheck(vis, key[1].newprod)

            if test[0] == False:
                visto.append(b)
            else:
                b = visto[test[1]]

            new_edges[(a, b)] = value

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
                            c2 = c.Ir_A(prod[idx + 1:])
                            conjuntos.append(c2)
                            self.edges[(c, c2)] = prod[idx + 1:]
                else:
                    idx = prod.index('.')
                    if idx != len(prod) - 1:
                        if prod[idx + 1] not in vistos:
                            vistos.append(prod[idx + 1])
                            c2 = c.Ir_A(prod[idx + 1])
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
        # Print the edges of the syntax automaton
        count = 1
        for key, value in self.edges.items():
            print(f'Conjunto = {count}')
            print(f'1. {key[0].newprod}')
            print(f'2. {key[1].newprod}')
            print(f'-> {value}')
            print('')
            count += 1
