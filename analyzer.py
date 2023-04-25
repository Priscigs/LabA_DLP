import re

# How every token is 
digits = r"[0-9]+"
decimal = r"[0-9]*\.[0-9]+"
letter = r"0[xX][0-9a-fA-F]+"
operand = r"[\+\-\*/]"
poww = r"\^"
delim = r"[ \t\n]"

# Every regex in one expression
expresion_total = re.compile(f"({digits}|{decimal}|{letter}|{operand}|{poww}|{delim})")
print(expresion_total)

# Read file
with open("YALex/input1yal.txt", "r") as archivo:
    archivo_input = archivo.read()

def analizar(input):
    tokens = expresion_total.findall(input)
    print("----------------TOKENS----------------")
    for token in tokens:
        if re.match(digits, token):
            print(f"Digits: {token}")
        elif re.match(decimal, token):
            print(f"Decimal: {token}")
        elif re.match(letter, token):
            print(f"Letter: {token}")
        elif re.match(operand, token):
            print(f"Arithmetic operand: {token}")
        elif re.match(poww, token):
            print(f"Pow operand: {token}")
        elif re.match(delim, token):
            pass  

analizar(archivo_input)
