import ply.lex as lex

# Cargar archivo de definición de analizador léxico
yalex_file_name = "YALex/slr-1.yal"
with open(yalex_file_name, "r") as file:
    yalex_text = file.read()

# Construir analizador léxico a partir del archivo de definición
lexer = lex.lex(debug=True)

# Leer archivo de entrada
with open("YALex/input1yal.txt") as f:
    input_text = f.read()

# Poner el texto de definición en el analizador léxico
lexer.input(yalex_text)

# Poner el texto de entrada en el analizador léxico
lexer.input(input_text)

# Tokenize input
for token in lexer:
    print(token)
