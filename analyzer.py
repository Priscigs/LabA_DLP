import re

# How every token is 
digits = r"[0-9]+"
decimal = r"[0-9]*\.[0-9]+"
letter = r"[a-zA-Z]+[0-9]*"
reserved_words = ["for", "if", "while", "else", "return"]
for word in reserved_words:
    letter += fr"|\\b{word}\\b"
operand = r"[\+\-\*/]"
poww = r"\^"
delim = r"[ \t\n]"

# Every regex in one expression
expresion_total = re.compile(f"({digits}|{decimal}|{letter}|{operand}|{poww}|{delim})")
print(expresion_total)

def analizar(input):
    tokens = expresion_total.findall(input)
    print("----------------TOKENS----------------")
    for token in tokens:
        if re.match(digits, token):
            print(f"Digits: {token}")
        elif re.match(decimal, token):
            print(f"Decimal: {token}")
        elif re.match(letter, token):
            if token in reserved_words:
                print(f"Reserved word: {token}")
            else:
                print(f"Letter: {token}")
        elif re.match(operand, token):
            print(f"Arithmetic operand: {token}")
        elif re.match(poww, token):
            print(f"Pow operand: {token}")
        elif re.match(delim, token):
            pass
