def expError(expression):
    operandsList = ["|",".","*","+","?"]
    
    # Check for empty expression
    if not expression:
        return False
    
    # Check for operator at the beginning of the expression
    if expression[0] in operandsList:
        return False
    
    # No errors detected
    return True

def ShuntingYard(expression):

    # Check for errors in the expression
    if expError(expression)==False:
        return None
    
    # Define the precedence of operators
    # | -> or
    # . -> concatenation
    # * -> kleene star
    # + -> positive
    # ? -> 0 or once
    precedence = {"|": 0, ".": 1, "*": 2, "+": 2, "?": 2}
    
    # Add a "." between concatenated expressions
    infToPos = "" 
    for i in range(len(expression)):
        if i == len(expression)-1:
            infToPos += expression[i]
        else:
            if expression[i+1] not in precedence.keys() and expression[i+1]!= ")":
                if expression[i] == "*":
                    infToPos += expression[i]
                    infToPos += "."
                elif expression[i] == "?":
                    infToPos += expression[i]
                    infToPos += "."
                elif expression[i] == "+":
                    infToPos += expression[i]
                    infToPos += "."
                elif expression[i] not in precedence.keys() and expression[i]!="(":
                    infToPos += expression[i]
                    infToPos+= "."
                else:
                    infToPos+=expression[i]
            else:
                infToPos +=expression[i]
                
    cadena = ""
    operatorStack = []
    expression = infToPos
    
    # Convert infix to postfix
    for i in expression:
        if i in precedence.keys() or i=="(" or i == ")":
            # Add opening brackets to the stack
            if len(operatorStack)==0 or operatorStack[-1]=="(" or i == "(":
                operatorStack.append(i)
            # Add closing brackets to the stack and pop everything inside the brackets
            elif i == ")":
                check = ""
                while check!="(":
                    cadena += operatorStack.pop()
                    check = operatorStack[-1]
                operatorStack.pop()
            # Pop operators from the stack until an operator with lower precedence is encountered
            elif precedence[i] < precedence[operatorStack[-1]]:
                while precedence[i] < precedence[operatorStack[-1]]:
                    cadena += operatorStack.pop()
                    if len(operatorStack) == 0 or operatorStack[-1]=="(":
                       break
                operatorStack.append(i)
            # Add operators to the stack
            elif precedence[i] > precedence[operatorStack[-1]]:
                operatorStack.append(i)
            # If two operators have equal precedence, pop the one already in the stack
            elif precedence[i] == precedence[operatorStack[-1]]:
                cadena += operatorStack.pop()
                operatorStack.append(i)
                
        else:
            # Add operands to the postfix string
            cadena += i
        
    # Pop any remaining operators from the stack
    while len(operatorStack)!=0:
        cadena += operatorStack.pop()
        
    return (cadena)