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

archivo_input = "2 \n2342 +  2 * 3 = 2350\n323.123 - -21.35 = 301.773\n0x3F - 0x1A = 0x25\n4 ^ 2 / 4 = 4"
# archivo_input = "10 20.5 0xA1B2 + - * / ^\n42 3.14 0x12345 * / ^ + -"
# archivo_input = "9 8.5 0xA1B2 + - * / ^ 2 1\n4 3.1 0x12345 * / ^ + - 5 ?"
# archivo_input = "a1 b2 for if 10 20\nwhile sum123 + - * /"

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
