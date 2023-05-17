# Has a disctinary with the variaty of the productions eg. {'Simbolo': [producciones]}
class Grammar():
    def __init__(self, prod, tokens):
        # Dictionary containing the productions
        self.prod = prod 
        # Set of terminal symbols
        self.tokens = tokens  
        self.nonterminals = []
        # List of nonterminal symbols
        self.nonterminals = [i for i in prod.keys() if i not in self.nonterminals]  
        # Initial nonterminal symbol
        self.initial = self.nonterminals[0]  
        # Set of all terminal symbols
        self.terminals = self.AllTerminals()  
        
    def AllTerminals(self):
        # Compute the set of all terminal symbols in the grammar
        # Flatten the list of productions
        allprods = [x for sublist in self.prod.values() for x in sublist]  
        terminals = set()

        for prod in allprods:
            if prod not in self.tokens:
                for i in range(len(prod)):
                    if prod[i] not in self.nonterminals:
                        if i < len(prod) - 2:
                            if prod[i+1] == "'":
                                # Handle single quote for extended symbols (e.g., E')
                                terminals.update(prod[i] + prod[i+1])
                            else:
                                terminals.update(prod[i])
                        else:
                            terminals.update(prod[i])
            else:
                terminals.add(prod)
        return terminals
    
    # Associate the productions to its nonterminal state E -> E+T|T  = {'E': ['E+T', T]}
    def getAllProductions(self, prod):
        for key, value in prod.items():
            for production in value:
                if '|' in production:
                    temp = production.split('|')
                    self.prod[key].remove(production)
                    self.prod[key].extend(temp)
            
    def AugmentedGrammar(self):
        # Augment the grammar by introducing a new initial nonterminal
        new_nonterminal = self.initial + "'"
        new_val = [new_nonterminal, *self.nonterminals]
        self.prod[new_nonterminal] = [self.initial]
        self.initial = new_nonterminal
