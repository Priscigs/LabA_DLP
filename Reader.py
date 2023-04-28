from TokensReader2 import rewrite, getTokensList, get_variable_names
from SimulationNFA2 import regex_to_enfa, Simulate_epsilonNFA, Simulate_megautomata

def Reader():
    # Input file names
    fileDotYal = "YALex/slr-1.yal"
    fileDotTxt = "YALex/input1yal.txt"

    # fileDotYal = "Pruebas/yalex1.yal"
    # fileDotTxt = "YALex/input2yal.txt"

    # fileDotYal = "Pruebas/yalex2.yal"
    # fileDotTxt = "YALex/input3yal.txt"

    # fileDotYal = "Pruebas/yalex3.yal"
    # fileDotTxt = "YALex/input4yal.txt"

    # Read the Yalex file and input file
    with open(fileDotYal, "r") as file:
        yalex_text = file.read()

    with open(fileDotTxt, "r") as file:
        input_text = file.read().replace('\n', '')

    # Rewrite the Yalex file to Python regex format and get variable names and regex values
    rewritten_text = rewrite(yalex_text)

    if rewritten_text is None:
        # If there are errors in the Yalex file, print an error message and return
        print("You have errore!!")
        return

    variable_names = get_variable_names(rewritten_text)
    resultado = getTokensList(rewritten_text)

    # Convert each regex value to an epsilon-NFA
    nfaEpsilon = [regex_to_enfa(regex) for regex in resultado]

    # Create a dictionary of categories (variable names) for each regex value
    categorias = {}
    for i, var_name in enumerate(variable_names):
        if i < len(resultado):
            categorias[resultado[i]] = var_name

    # Create a list of identifiers (variable names) for each epsilon-NFA
    identifiers = [categorias.get(regex, "Unknown") for regex in resultado]

    # Generate a Graphviz representation for each epsilon-NFA and save it to a file
    for idx, enfa in enumerate(nfaEpsilon):
        identifier = identifiers[idx]
        enfa_graph = Simulate_epsilonNFA(enfa, identifier)
        enfa_graph.render(f"epsilonNFA{idx}", view=True)

    # Generate a mega epsilon-NFA from all the epsilon-NFAs and create a Graphviz representation
    mega_enfa_graph = Simulate_megautomata(nfaEpsilon, identifiers)
    mega_enfa_graph.render("megautomata", view=True)
