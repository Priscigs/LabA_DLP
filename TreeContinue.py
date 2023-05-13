
from Tree import Node, CreateSyntaxTree, printTree
from DFA import DFA




def TreeToDFA(regex):
    
    s = regex
    
    root = CreateSyntaxTree(s)
    root.ShowGraph()

    followpos_table = root.getTable()  
    # for i in followpos_table:
    #     print(i)  
    
    # Encontramos el alfabeto de la tabla
    alphabet = set(entry[0] for entry in followpos_table if entry[0] != "#")
    #print(alphabet)
    final = followpos_table[-1][1]
    initial =followpos_table[0][1]
    
    trans = [followpos_table[0]]
    stack = [followpos_table[0][2]]
    looked = [followpos_table[0][2]]
    
    
    while stack:
        look_at = stack.pop()
        #print(alphabet)
        for letter in alphabet:
            nodos = set()
            for node in look_at:
                if followpos_table[node-1][0] == letter:
                    nodos.update(followpos_table[node-1][2])
            if nodos not in looked:
                looked.append(nodos)
                stack.append(nodos)
            trans.append((letter, look_at, nodos))
            #print(looked)
    
    transition = [trans[i] for i in range(len(trans)) if (trans[i][1] and trans[i][2])]

    #print(transition)
    names = {}
    count = 0
    for i in range(len(transition)):
        a = transition[i][1]
        b = transition[i][2]
        if type(a) == int:
            a = set({a})
        if type(b) == int:
            b = set({b})
        if frozenset(a) not in names.keys():
            names[frozenset(a)] = "S"+str(count)
            count+=1
        if frozenset(b) not in names.keys():
            names[frozenset(b)] = "S"+str(count)
            count+=1
         
    transitions = {}  

    for i in range(len(transition)):
        a = transition[i][1]
        b = transition[i][2]
        if type(a) == int:
            a = set({a})
        if type(b) == int:
            b = set({b})
        if names[frozenset(a)] not in transitions.keys():
            transitions[names[frozenset(a)]] = {transition[i][0]: names[frozenset(b)]}
        else:
            transitions[names[frozenset(a)]].update({transition[i][0]: names[frozenset(b)]})

    print(transitions)
    start_state = names[frozenset({initial})]
    accepting_states = []
    for key, value in names.items():
        if final in key and value not in accepting_states:
            accepting_states.append(value)
   
    
    # Inicializamos el estado inicial que sería el followpos de nuestro root.
    
    return DFA(start_state, accepting_states, transitions)
