import re

ws = r"([' ''\t''\n'])+"
id = r"(['A'-'Z''a'-'z'])((['A'-'Z''a'-'z'])|(['0'-'9']))*"

# Compilación de todas las expresiones regulares en una sola expresión
expresion_total = re.compile(f"({ws}|{id})")

# Analizar el archivo de entrada
archivo_entrada = "22342 +  2 * 3 = 2350323.123 - -21.35 = 301.773 0x3F - 0x1A = 0x254 ^ 2 / 4 = 4"
def analizar(entrada):
    tokens = entrada.split()
    for token in tokens:
        if re.match(ws, token):
            print(f"Ws: {token}")
        elif re.match(id, token):
            print(f"Id: {token}")
        else:
            print(f"Error Sintactico(No reconocido): {token}")


analizar(archivo_entrada)
