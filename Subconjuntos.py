from NFA import NFA
from DFA import DFA

def Closure(transiciones: dict, state: str):
    epsilon = "ε"
    visited = {state}
    stack = [state]
    
    while stack:
        estado = stack.pop()
        if estado in transiciones and epsilon in transiciones[estado]:
            epsilon_transitions = transiciones[estado][epsilon]
            if isinstance(epsilon_transitions, list):
                for t in epsilon_transitions:
                    if t not in visited:
                        stack.append(t)
                        visited.add(t)
            else:
                if epsilon_transitions not in visited:
                    stack.append(epsilon_transitions)
                    visited.add(epsilon_transitions)
    return visited

def get_groups(transiciones: dict, estados:list, character: str):
    group = set()
    for i in estados:
        if i in transiciones and character in transiciones[i]:
            if isinstance(transiciones[i][character], list):
                group.update(transiciones[i][character])
            else:
                group.add(transiciones[i][character])
                
    closure_states = set()
    for state in group:
        closure_states.update(Closure(transiciones, state))
    return closure_states
                
def Subconjuntos(AFN: NFA):
    transiciones = AFN.transitions
    alphabet = AFN.getAplhabet()
    
    #State name
    count = 0
    state = "S"+str(count)
    groups = {state: Closure(transiciones, AFN.initial_state.label)}
    stack = {state}
    #Transiciones ya con los nuevos grupos
    transitions = {}
    
    #Mientras haya algun estado en el stack que no se haya visitado
    while stack:
        #estado = estado a ser revisado para sus grupos
        estado = stack.pop()
        
        #Se inicializa un diccionario para guardar transiciones para el estado
        transitions[estado] = {}
        new_groups = {}
        
        #Chequear si hay transiciones para cada letra dentro del alfabeto
        for i in alphabet:
            
            #Conseguir los grupos para el simbolo de transición -> E-Closure(delta(state, i))
            grupos = set(get_groups(transiciones, groups[estado], i))
            
            #Si si existen grupos para esa transicion entonces
            if grupos: 
                seen_state = None
                
                #Revisar si alguno de los grupos que ya se tienen es igual al grup
                for s, g in groups.items():
                    #Si el grupos ya existe dentro de los grupos que ya se tienen
                    #Entonces agarrar el estado que representa a ese grupo
                    if grupos == g:
                        seen_state = s
                        break
                #Si el estado ya existe entonces crear una transición que vaya hacia ese estado
                if seen_state:
                    transitions[estado][i] = seen_state
                #De lo contrario cambiar el contador para concatenarlo al estado
                #Añadir el nuevo estado para revisar sus trancisiones.
                #Añadir los nuevos estados junto a sus grupos
                #Agregar la nueva transición al diccionario de transiciones 
                else:
                    count += 1
                    state = "S" + str(count)
                    stack.add(state)
                    new_groups[state] = grupos
                    transitions[estado][i] = state
                    
                    
        #Añadir los nuevos grupos creados al diccionario de groups
        groups.update(new_groups)
        
    finales = set([key for key, value in groups.items() if AFN.accept_state.label in value])
    start = "S0"
    
    
    return DFA(start,finales, transitions)  
    

    