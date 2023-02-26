# | -> or
# . -> concatenation
# * -> kleene star
# + -> positive
# ? -> 0 or once
precedence = {"|": 0, ".": 1, "*": 2, "+": 2, "?": 2}

def ShuntingYard(infix:str):
    output = []
    operators = []

    i = 0
    while i < len(infix):
        # Read the next symbol
        c = infix[i]
        # Letter or number add it to the end
        if c.isalnum():
            output.append(c)
        # Left bracket add it to the stack of operands
        elif c == "(":
            operators.append(c)
        # If it's and operand
        elif c in precedence:
            # While there are operands in the stack and this has the hightest precedence
            while operators and operators[-1] != "(" and precedence[operators[-1]] >= precedence[c]:
                # Take the operand out of the stack and add it to the output
                output.append(operators.pop())
            # Add current operand to stack
            operators.append(c)
        # Right bracket
        elif c == ")":
            # While the top operand isn't a left bracket
            while operators and operators[-1] != "(":
                # Take the operand out of the stack and add it to the output
                output.append(operators.pop())
            # Take the left bracket and add it to the satcj without adding it to the output
            operators.pop()
        # Ignore any other sybol
        i += 1
    # Take any operand left and add it to the stack
    while operators:
        output.append(operators.pop())
    # Join the list
    return "".join(output)