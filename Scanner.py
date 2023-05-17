from DFA import DFA
from Thompson import Thompson

reg = '(@|→|↓)|(@|→|↓)+|(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)|(_)*|(0|1|2|3|4|5|6|7|8|9)|(0|1|2|3|4|5|6|7|8|9)+|(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)((A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)|(_)*|(0|1|2|3|4|5|6|7|8|9))*|(0|1|2|3|4|5|6|7|8|9)+(▪(0|1|2|3|4|5|6|7|8|9)+)?(ε(＋|-)?(0|1|2|3|4|5|6|7|8|9)+)?'
nfa = Thompson(reg)
txt_input = 'inputYalex.txt'
lines = []
tokens = []

with open('inputYalex.txt', 'r', encoding='utf-8') as file:
	lines = file.readlines()

lines = [i.strip() for i in lines]
errors = []

for i in range(len(lines)):
	if nfa.simulate2(lines[i]) == False:
		errors.append(f'Syntax error on line {i} -> {lines[i]}')
	else:
		tokens.append(lines[i])

if errors:
	for i in errors:
		print(i)
else:
	print('Program has no syntax errors')
	for i in tokens:
		print('token: ', i)
