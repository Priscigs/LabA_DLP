import re

def ShuntingY(expression):
    # Crear diccionario de precedencia de operadores
    precedence = {'+':1, '-':1, '*':2, '/':2, '^':3}

    # Inicializar listas para la pila de operadores y la salida
    operator_stack = []
    output_queue = []

    # Separar la expresión en tokens
    tokens = expression.split()

    # Filtrar los paréntesis de la lista de tokens
    tokens = [token for token in tokens if token not in '()']

    # Procesar cada token
    for token in tokens:
        # Si el token es un número o una letra, agregar a la salida
        if re.match(r'\w+', token):
            output_queue.append(token)
        # Si el token es un operador
        elif token in precedence:
            # Sacar de la pila todos los operadores con mayor o igual precedencia y agregar a la salida
            while operator_stack and operator_stack[-1] != '(' and precedence[token] <= precedence[operator_stack[-1]]:
                output_queue.append(operator_stack.pop())
            # Apilar el operador
            operator_stack.append(token)
        # Si el token es un paréntesis izquierdo, apilar
        elif token == '(':
            operator_stack.append(token)
        # Si el token es un paréntesis derecho, sacar de la pila todos los operadores hasta encontrar el paréntesis izquierdo correspondiente
        elif token == ')':
            while operator_stack and operator_stack[-1] != '(':
                output_queue.append(operator_stack.pop())
            # Eliminar los paréntesis izquierdo y derecho
            if operator_stack and operator_stack[-1] == '(':
                operator_stack.pop()

    # Desapilar los operadores restantes y agregar a la salida
    while operator_stack:
        output_queue.append(operator_stack.pop())

    # Unir los elementos de la salida en una cadena de caracteres y retornar
    return ' '.join(output_queue)


# Ejemplo de uso
expression = '3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3'
print(ShuntingY(expression)) # Salida: 'a b 2 * 1 5 - 2 3 ^ ^ / +'

