# This function checks if a given string is enclosed in brackets (either [] or ())
def parentesis(string):
    if string[0] == "[" and string[-1]== "]":
        return True
    elif string[0] == "(" and string[-1] == ")":
        return True
    return False

# This function checks the structure of a "let" statement and makes sure it is properly formatted
def checkLetStructure(line):
    line = line.strip()
    if "let" in line[:3]:
        if line[3:][0] !=" ":
            return False
        after_let = line[3:]
        name, definition = after_let.split("=")
        name = name.strip()
        definition = definition.strip()
        if len(name.split(" "))>1:
            return False
        if commentsCheck(definition):
            definition = commentsQuit(definition).strip()
            if parentesis(definition):
                if len(definition[:definition.index("[")]) >0:
                    return False
            else:
                if len(definition.split(" ")) > 1:
                    return False
        return True
    else:
        return False

# This function removes comments from a given line of code
def commentsQuit(line):
    if "(*" in line:
        line = line[:line.index("(*")] + line[line.index("*)") + 2:]
    return line

# This function checks if there are any unclosed or incorrectly formatted comments in the line
def commentsCheck(line):
    if "(*" in line:
        return( "*)" in line[line.index("(*"):])
    if "*)" in line:
        return( "(*" in line[:line.index("*)")])
    else:
        return True

def rules(filename):
    errors = []
    line_counter = 1
    definitions, tokens = {}, {}
    rule_tokens = False

    # Open the file and read each line
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            # Check for comments and remove them
            if commentsCheck(line)==False:
                errmess = f"Error en la línea {line_counter}. Se escribió mal un comentario"
                errors.append(errmess)

            else:
                line = commentsQuit(line.strip())

            # If rule_tokens is True, add tokens to the dictionary
            if rule_tokens:
                if line == "":
                    break 

                if "|" == line[:1]:
                    line = line[2:]

                if " {" in line:
                    token, function = line.split(" {")
                else:
                    token = line
                    function = "None"

                tokens[token.strip()] = function.replace("return", "").replace("}", "").strip()
                line_counter+=1
                continue

            # Check if the line contains "rule tokens ="
            if "rule tokens =" == line[:13]:
                rule_tokens = True
                continue

            # Check if the line contains "let"
            if "let" in line.split("=")[0].split(" ")[0]:
                # If the "let" statement is well-formed, add the definition to the dictionary
                if checkLetStructure(line):
                    name, definition = line[4:].split(" = ")
                    definition = definition.replace("'E'", "ε").replace("\\n", "↓").replace("\\t", "→").replace("\\r", "↕").replace("\\s", "↔").replace(".","▪")

                    if definition.strip()[0] == "[":
                        definition.replace("['", "").replace("']", "").split(", ")
                        # TODO tengo que ver que hacer en los espacios

                    definitions[name.strip()] = definition.strip()
                    line_counter+=1

                    continue
                else:
                    # If the "let" statement is not well-formed, add an error message to the errors list
                    errmess = f"Error en la línea {line_counter}. Forma incorrecta del let."
                    errors.append(errmess)
                    line_counter+=1
                    continue

            line_counter+=1

    # If there are any errors, print them and return None
    if errors:
        for i in errors:
            print(i)
        return None
    # Otherwise, return the definitions and tokens dictionaries
    return definitions, tokens

def get_range(start, end):
    # Helper function to create a range of characters
    return range(ord(start), ord(end) + 1)

def regexCreate(filename):
    # This function reads a YACC file, extracts definitions and tokens from it, and returns a regular expression that matches those tokens
    if rules(filename):
        # If the file can be read, extract definitions and tokens
        definitions, tokens = rules(filename)

        # Define a translation table for characters to be removed from the regular expressions
        transtable = str.maketrans("[]\'\"", "    ")

        # Iterate through all definitions and replace any references to other definitions with their true regular expression definitions
        for name, definition in definitions.items():
            for key, true_regex in sorted(list(definitions.items()), key=lambda x:x[0].lower(), reverse=True):
                if key in definition:
                    definition = definition.replace(key, f"{true_regex}")

            # If the definition contains a character range in square brackets (e.g. [a-z]), split the range into individual characters and replace it with a regular expression that matches any of those characters
            if "[" in definition and "]" in definition:
                indexa = definition.index("[")
                in_brackets = definition[definition.index("[")+1:definition.index("]")]

                if "''" in in_brackets:
                    # If the character range is enclosed in double quotes (e.g. ["a-z"]), split the range into individual characters and replace any empty parts with a placeholder character
                    split_regex, final_regex = in_brackets.split("''"), []
                    for char in split_regex:
                        char = char.translate(transtable).strip()
                        if char == "":
                            char = "@"
                        final_regex += [char]
                else:
                    # If the character range is not enclosed in double quotes, use the whole range as the regular expression
                    final_regex = [definition]

                # Create a regular expression that matches any of the characters in the range, replacing any hyphens with a range of characters
                regex_str = ""
                for regex_part in final_regex:
                    sanitized_regex = regex_part.translate(transtable).strip()
                    if "-" in sanitized_regex and len(sanitized_regex) >= 3:
                        split_range = sanitized_regex.split(" - ")
                        char_range = get_range(*split_range)
                        sanitized_regex = "|".join([chr(char) for char in char_range])
                    if regex_str:
                        regex_str += "|"
                    regex_str += sanitized_regex
                    regex_str = regex_str.replace("+", "＋")

                # Replace the character range in the definition with the new regular expression
                definition = definition[:indexa] + "(" + regex_str + ")" + definition[definition.index("]")+1:]

            # Store the updated definition back into the definitions dictionary
            definitions[name] = definition

        # Concatenate all the regular expression definitions into a single regular expression string
        full_regex = ""
        for name, definition in definitions.items():
            if full_regex:
                full_regex += "|"
            full_regex += f"{definition}"

        return full_regex
    else:
        # If the file cannot be read, return None
        return None