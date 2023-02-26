precedence = {"|": 0, ".": 1, "*": 2, "+": 2, "?": 2}

def ShuntingY(infix):
    output = []
    operators = []
    i = 0
    while i < len(infix):
        # Leer el siguiente símbolo
        c = infix[i]
        # Si es una letra o número, agregarlo a la salida
        if c.isalnum():
            output.append(c)
        # Si es un paréntesis izquierdo, agregarlo a la pila de operadores
        elif c == "(":
            operators.append(c)
        # Si es un operador
        elif c in precedence:
            # Mientras haya operadores en la pila y el operador en la cima tenga mayor o igual precedencia
            while operators and operators[-1] != "(" and precedence[operators[-1]] >= precedence[c]:
                # Sacar el operador de la pila y agregarlo a la salida
                output.append(operators.pop())
            # Agregar el operador actual a la pila de operadores
            operators.append(c)
        # Si es un paréntesis derecho
        elif c == ")":
            # Mientras el operador en la cima de la pila no sea un paréntesis izquierdo
            while operators and operators[-1] != "(":
                # Sacar el operador de la pila y agregarlo a la salida
                output.append(operators.pop())
            # Sacar el paréntesis izquierdo de la pila sin agregarlo a la salida
            operators.pop()
        # Ignorar cualquier otro símbolo
        i += 1
    # Sacar cualquier operador que quede en la pila y agregarlo a la salida
    while operators:
        output.append(operators.pop())
    # Unir la lista de salida en una cadena y devolverla
    return "".join(output)

expression = '0?(1?)?0+'
print(ShuntingY(expression))
