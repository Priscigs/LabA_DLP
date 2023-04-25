from TokensReader2 import reescribir_archivo, get_values_list, get_variable_names
from NFA2 import regex_to_enfa, Simulate_epsilonNFA, Simulate_megautomata

def Reader():
    # Input file names
    yalex_file_name = "YALex/slr-1.yal"
    input_file_name = "YALex/input1yal.txt"

    # yalex_file_name = "Pruebas/yalex1.yal"
    # input_file_name = "Pruebas/input1.txt"

    # yalex_file_name = "Pruebas/yalex3.yal"
    # input_file_name = "Pruebas/input3.txt"

    # Read the Yalex file and input file
    with open(yalex_file_name, "r") as file:
        yalex_text = file.read()

    with open(input_file_name, "r") as file:
        input_text = file.read().replace('\n', '')

    # Rewrite the Yalex file to Python regex format and get variable names and regex values
    rewritten_text = reescribir_archivo(yalex_text)

    if rewritten_text is None:
        # If there are errors in the Yalex file, print an error message and return
        print("Existen errores.")
        return

    variable_names = get_variable_names(rewritten_text)
    resultado = get_values_list(rewritten_text)

    # Convert each regex value to an epsilon-NFA
    enfas = [regex_to_enfa(regex) for regex in resultado]

    # Create a dictionary of categories (variable names) for each regex value
    categorias = {}
    for i, var_name in enumerate(variable_names):
        if i < len(resultado):
            categorias[resultado[i]] = var_name

    # Create a list of identifiers (variable names) for each epsilon-NFA
    identifiers = [categorias.get(regex, "Desconocido") for regex in resultado]

    # Generate a Graphviz representation for each epsilon-NFA and save it to a file
    for idx, enfa in enumerate(enfas):
        identifier = identifiers[idx]
        enfa_graph = Simulate_epsilonNFA(enfa, identifier)
        enfa_graph.render(f"epsilonNFA{idx}", view=True)

    # Generate a mega epsilon-NFA from all the epsilon-NFAs and create a Graphviz representation
    mega_enfa_graph = Simulate_megautomata(enfas, identifiers)
    mega_enfa_graph.render("megautomata", view=True)

    # Write the compiled regex expressions to a Python file
    with open("compilado.py", "w") as compiled_file:
        # Write an import statement for the re module
        compiled_file.write("import re\n\n")

        # Write each variable name and its corresponding compiled regex expression to the file
        for regex, var_name in zip(resultado, identifiers):
            compiled_file.write(f"{var_name} = r\"{regex}\"\n")

        # Write code to compile all the regex expressions into a single expression
        compiled_file.write("\n# Compilación de todas las expresiones regulares en una sola expresión\n")
        compiled_file.write("expresion_total = re.compile(")
        compiled_file.write("f\"(")
        compiled_file.write("|".join([f"{{{var_name}}}" for var_name in identifiers]))
        compiled_file.write(")\")\n")
        # compiled_file.write("print(expresion_total)\n")

        # Write code to read the input file and analyze its contents using the compiled regex expressions
        compiled_file.write(f'\n# Analizar el archivo de entrada\narchivo_entrada = "{input_text}"\n')
        compiled_file.write("def analizar(entrada):\n")
        compiled_file.write("    tokens = entrada.split()\n")
        compiled_file.write("    for token in tokens:\n")

        # Loop through each identifier (variable name) and its associated regular expression
        for i, var_name in enumerate(identifiers):
            # If it's the first identifier, use an "if" statement
            if i == 0:
                compiled_file.write(f"        if re.match({var_name}, token):\n")
            # Otherwise, use an "elif" statement
            else:
                compiled_file.write(f"        elif re.match({var_name}, token):\n")
            # Print the identifier and matched token if a match is found
            compiled_file.write(f"            print(f\"{var_name.capitalize()}: {{token}}\")\n")
        # If no match is found, print an error message
        compiled_file.write("        else:\n")
        compiled_file.write("            print(f\"Error Sintactico(No reconocido): {token}\")\n")
        # Call the "analizar" function with the input text
        compiled_file.write("\n\nanalizar(archivo_entrada)\n")
