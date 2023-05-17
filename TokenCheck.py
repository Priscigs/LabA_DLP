from Grammar import Grammar

# Dictionary to store the computed firstT and followT sets
conjuntos = dict()

res1 = {}
res2 = {}

# Function to check if a symbol produces epsilon (ε)
def CheckEspsilon(Y, prod):
    if Y in prod.keys():
        return 'ε' in prod[Y]
    return False

# Function to check if a non-terminal has left recursion
def checkLeftRecursiveness(X, productions):
    if X in productions.keys():
        for prod in productions[X]:
            if prod[0]!=X:
                return prod[0]
    else:
        return X
    return False

# Function to compute the firstT set for a given non-terminal symbol X
def firstT(grammar: Grammar, X):
    g = grammar
    terminales = g.terminals
    noterminales = g.nonterminals
    producciones = g.prod
    
    if X not in conjuntos.keys():
        conjuntos[X] = []
        
    # If X is a terminal, add it to the firstT set
    if X in terminales:
        conjuntos[X].append(X)
        return
    temp = list(producciones[X])

    # If there is a production X -> ε, add ε to the firstT set and remove it from temp
    if 'ε' in producciones[X]:
        conjuntos[X].append('ε')
        temp.remove('ε')
        
    # Filter out productions that have length less than 2
    temp = [i for i in temp if len(i)>=2]
    
    true_temp = [[CheckEspsilon(symbol, producciones) for symbol in prod] for prod in temp]
    
    # If X is a non-terminal and there is a production of the form X -> y1y2...yk
    if not grammar:
        if X in noterminales and temp:
            for prod in range(len(temp)):
                for symbol in range(len(temp[prod])):
                    if (new_symbol:=checkLeftRecursiveness(temp[prod][symbol], g.prod)):
                        # firstT(y1) belongs to firstT(X)
                        conjuntos[X].append(firstT(g, new_symbol)) 
                    # For the followTs symbols
                    if symbol >0: 
                        if all(true_temp[prod][:symbol]):
        
                            new_symbol=checkLeftRecursiveness(temp[prod][symbol], g.prod)
                            conjuntos[X].append(firstT(g, new_symbol))
                        elif all(true_temp[prod][symbol]):
                            conjuntos[X].append('ε')
    return res1
        
# Function to compute the followT set for a given non-terminal symbol X 
def followT(grammar, res_firstT, X = None):
    g = grammar
    terminales = g.terminals
    noterminales = g.nonterminals
    producciones = g.prod
    
    if X not in conjuntos.keys():
        conjuntos[X] = []

    # If X is a terminal, add it to the followT set
    if X in terminales:
        conjuntos[X].append(X)
        return
    temp = list(producciones[X])

    # If there is a production X -> ε, add ε to the followT set and remove it from temp    
    if 'ε' in producciones[X]:
        conjuntos[X].append('ε')
        temp.remove('ε')
        
    # Filter out productions that have length less than 2
    temp = [i for i in temp if len(i)>=2]
    
    true_temp = [[CheckEspsilon(symbol, producciones) for symbol in prod] for prod in temp]
    
    # If X is a non-terminal and there is a production of the form X -> y1y2..yk
    if not grammar:
        if X in noterminales and temp:
            for prod in range(len(temp)):
                for symbol in range(len(temp[prod])):
                    # Check for left recursion
                    if (new_symbol:=checkLeftRecursiveness(temp[prod][symbol], g.prod)):
                        # firstT(y1) belongs to firstT(X)
                        conjuntos[X].append(firstT(g, new_symbol)) #firstT(y1) pertenece a firstT(X)
                    # For followT symbols
                    if symbol >0: 
                        if all(true_temp[prod][:symbol]):
                            new_symbol=checkLeftRecursiveness(temp[prod][symbol], g.prod)
                            conjuntos[X].append(firstT(g, new_symbol))
                        elif all(true_temp[prod][symbol]):
                            conjuntos[X].append('ε')
    return res2


def remove_comments(line):
    if "/*" in line:
        line = line[:line.index("/*")] + line[line.index("*/") + 2:]
    return line


def checkComments(line):
    if "/*" in line:
        return( "*/" in line[line.index("/*"):])
    if "*/" in line:
        return( "/*" in line[:line.index("*/")])
    else:
        return True
    
def checkTokenStructure(line):
    if line[0]!="%":
        return False
    if len(line.split(' '))>2:
        return False
    if line.count('%')>1 and len(line)>2:
        return False
    if line[1]==" ":
        return False
    return True

def checkProductionStructure(line):
    
    if line[0]!="|":
        return False
    if line.count('|')>1:

        return False
    if line[1]!=" ":
        return False
    return True
    
def readYalp(filename):
    tokens = []
    errors = []
    line_counter = 1

    removews = False
    getProductions = False
    productions = {}
    
    trans_table =  {'expression': 'E', 
                    'term': 'T', 
                    'PLUS': '+',
                    'TIMES': '*',
                    'factor': 'F',
                    'LPAREN': '(',
                    'RPAREN': ')',
                    'MINUS': '-',
                    'DIV': '/'}
    
    current_symbol = ""
    
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            # Remove comments and strip
            if checkComments(line)==False:
                errmess = f"Error en la línea {line_counter}. Comentario mal definido"
                errors.append(errmess)

            else:
                line = remove_comments(line.strip())
            
            if line[-1:] == "\n":
                line = line[:-1]
            temp = line.split(" ")

            # Check for token definitions
            if "%" in temp[0] and getProductions == False and '%%' not in temp[0]:
                if checkTokenStructure(line)==False:
                    errmess = f"Error en la línea {line_counter}. Token mal definido"
                    errors.append(errmess)
                else:
                    tokens.append(temp[1])

            # Check for IGNORE directive
            if temp[0]=='IGNORE':
                removews = True

            # Check for start of productions
            if temp[0][:2]=="%%":
                getProductions = True
                line_counter+=1

                continue

            # Process productions
            if getProductions == True:
                if temp[0]!="" and temp[0]!=";":
                    if len(temp) < 2 and ':' in temp[0]:
                        idx = line.index(':')
                        symbol = line[:idx]
                        current_symbol = symbol.replace(symbol, trans_table[symbol])
                        productions[current_symbol] = []
                    else:
                        if len(productions[current_symbol])>0:
                            if checkProductionStructure(line)==False:
                                errmess = f"Error en la línea {line_counter}. Error en la estructura de la produccion definida"
                                errors.append(errmess)
                            else:
                                temp2 = ''.join(temp[1:])
                                for key in trans_table:
                                    temp2 = temp2.replace(key, trans_table[key])
                                productions[current_symbol].append(temp2)
                        else:
                            temp2 = ''.join(temp)
                            for key in trans_table:
                                temp2 = temp2.replace(key, trans_table[key])
                            productions[current_symbol].append(temp2)
            line_counter+=1

    # Display errors, if any
    if errors:
        for i in errors:
            print(i)
        return None

    return productions, tokens

def checkTokens(l1, l2):

    for token in l2:
        if token not in l1:
            return False
    return True
