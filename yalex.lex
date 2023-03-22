let if = "if"
let else = "else"
let digit = "1|2|3"
let number = "digit(digit)*"
let letter = "a|b|c|d|e"
let identifier = "letter(letter|digit)*"

rule tokens =
  if	{ print("IF\n") }
  | else	{ print("ELSE\n") }
  | identifier  	{ print("Identifier\n") }
  | digit			{ print("Digit\n") }
  | letter			{ print("Letter\n") }
  | number			{ print("Numbre\n") }
