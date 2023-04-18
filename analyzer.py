import re

# Definición de las expresiones regulares para cada token
digits = r"[0-9]+"
decimal = r"[0-9]*\.[0-9]+"
letter = r"0[xX][0-9a-fA-F]+"
operador = r"[\+\-\*/]"
poww = r"\^"
delim = r"[ \t\n]"

# Compilación de todas las expresiones regulares en una sola expresión
expresion_total = re.compile(f"({digits}|{decimal}|{letter}|{operador}|{poww}|{delim})")
print(expresion_total)
# Analizar el archivo de entrada
archivo_entrada = "2 \n2342 +  2 * 3 = 2350 \n323.123 - -21.35 = 301.773 \n0x3F - 0x1A = 0x25\n4 ^ 2 / 4 = 4"

def analizar(entrada):
    tokens = expresion_total.findall(entrada)
    for token in tokens:
        if re.match(digits, token):
            print(f"digits: {token}")
        elif re.match(decimal, token):
            print(f"Decimal: {token}")
        elif re.match(letter, token):
            print(f"letter: {token}")
        elif re.match(operador, token):
            print(f"Operador aritmético: {token}")
        elif re.match(poww, token):
            print(f"Operador de potenciación: {token}")
        elif re.match(delim, token):
            pass  # Ignorar espacios, delim y saltos de línea

analizar(archivo_entrada)
