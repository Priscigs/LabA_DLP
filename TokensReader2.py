import re

# function to validate if parentheses are balanced in a string
def validate_parentheses(value):
    count = 0
    for char in value:
        if char == '(':
            count += 1
        elif char == ')':
            count -= 1
        if count < 0:
            return False
    return count == 0

# function to validate that the number of single quotes in a string is even
def validate_single_quotes(value):
    return value.count("'") % 2 == 0

# function to get the set of used variables in the "rule tokens" section of the input text
def get_used_variables(input_text):
    rule_tokens_section = input_text.split("rule tokens =")[1]
    used_variables = re.findall(r'\b\w+\b', rule_tokens_section)
    return set(used_variables)

# function to rewrite the input text by substituting variable values in expressions
def rewrite(input_text):
    lines = input_text.split("\n")
    variables = {} # dictionary to store variable values
    errors = [] # list to store any validation errors
    used_variables = get_used_variables(input_text) # set of used variables in the "rule tokens" section of the input text

    # loop through each line in the input text
    for line in lines:
        if not line.startswith("let"): # skip any lines that don't define a variable
            continue
        
        var_name, value = line[4:].split(" = ") # extract the variable name and value from the line
        
        # validate that the value is enclosed in single quotes
        if not validate_single_quotes(value):
            errors.append(f"Error en la línea: {line}. Los valores deben estar entre comillas simples.")
            continue
        
        value = value.strip("'") # remove the enclosing single quotes
        
        # validate that the parentheses in the value are balanced
        if not validate_parentheses(value):
            errors.append(f"Error en la línea: {line}. Los paréntesis no están balanceados.")
            continue
        
        variables[var_name] = value # add the variable name and value to the dictionary

    if errors: # if there were any validation errors, print them and return None
        for error in errors:
            print(error)
        return None

    # loop through each variable in the dictionary and substitute its value in expressions
    for var_name, value in variables.items():
        for dependent_var in variables:
            variables[dependent_var] = variables[dependent_var].replace(var_name, f"({value})")

    output_lines = []
    # loop through each variable in the dictionary and add its name and value to the output lines if it is used in the "rule tokens" section
    for var_name, value in variables.items():
        if var_name in used_variables:
            output_lines.append(f"let {var_name} = '{value}'")

    return "\n".join(output_lines)

# function to extract a list of values from the rewritten text
def getTokensList(rewritten_text):
    lines = rewritten_text.split("\n")
    values_list = []

    for line in lines:
        if line.startswith("let"): # skip any lines that don't define a variable
            _, value = line.split(" = ") # extract the value from the line
            value = value.strip("'") # remove the enclosing single quotes
            values_list.append(value)

    return values_list

# This function finds the identifier (category) associated with the symbol that transitions to a final state in an ENFA.
# It takes as input an ENFA (enfa) and a dictionary (categories) mapping symbols to categories.
# It returns the category associated with the symbol that transitions to a final state, or "Desconocido" (unknown) if no such symbol is found.
def getToken(enfa, categories):
    for from_state, to_dict in enfa._transition_function._transitions.items():
        for symbol, to_states in to_dict.items():
            for to_state in to_states:
                if to_state in enfa.final_states:
                    for key, value in categories.items():
                        if symbol in key:
                            return value
    return "Unknown"

# This function extracts the variable names from rewritten code.
# It takes as input a string (rewritten_text) containing the rewritten code.
# It returns a list of variable names.
def get_variable_names(rewritten_text):
    lines = rewritten_text.split("\n")
    variable_names = []

    for line in lines:
        if line.startswith("let"):
            var_name, _ = line[4:].split(" = ")
            variable_names.append(var_name.strip())

    return variable_names
