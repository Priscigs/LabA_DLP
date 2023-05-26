from DFA import DFA
from Thompson import Thompson

reg = '(@|→|↓)|(@|→|↓)+|(0123456789)|(0123456789)+|(0123456789)+(▪(0123456789)+)?(ε(＋|-)?(0123456789)+)?'
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
