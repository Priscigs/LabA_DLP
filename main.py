from ShuntingYard import ShuntingYard
from Thompson import Thompson
from Simulation import Simulation

if __name__=="__main__":

    expression = "(a*|b*).c"
    postfix = ShuntingYard(expression)
    nfa = Thompson(postfix)
    dot = Simulation(nfa)
    dot.render('nfa_thompson', format = 'png', view = True)

