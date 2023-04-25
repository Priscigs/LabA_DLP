import ply.lex as lex

tokens = [
    'ID',          # Identificador
    'INTEGER',     # Número entero
    'STRING',      # Cadena de caracteres
    'LPAREN',      # Paréntesis izquierdo
    'RPAREN',      # Paréntesis derecho
    'LBRACKET',    # Corchete izquierdo
    'RBRACKET',    # Corchete derecho
    'LBRACE',      # Llave izquierda
    'RBRACE',      # Llave derecha
    'COMMA',       # Coma
    'SEMICOLON',   # Punto y coma
    'PLUS',        # Suma
    'MINUS',       # Resta
    'TIMES',       # Multiplicación
    'DIVIDE',      # División
    'MOD',         # Módulo
    'ASSIGN',      # Asignación
    'EQ',          # Igualdad
    'NE',          # Diferente
    'LT',          # Menor que
    'LE',          # Menor o igual que
    'GT',          # Mayor que
    'GE',          # Mayor o igual que
    'IF',          # if
    'ELSE',        # else
    'WHILE',       # while
    'FOR',         # for
    'WHITESPACE',  # Espacio
]

# Palabras reservadas
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
}

# Expresiones regulares para reconocer cada token
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_COMMA = r','
t_SEMICOLON = r';'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_ASSIGN = r'='
t_EQ = r'=='
t_NE = r'!='
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID') # Verificar si es una palabra reservada
    return t

def t_INTEGER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)
    return t

def t_STRING(t):
    r'"(?:\\.|[^\\"])*"'
    t.value = t.value[1:-1] # Eliminar comillas dobles al inicio y al final
    return t

# Expresión regular para identificar espacios en blanco y tabuladores
def t_WHITESPACE(t):
    r'[ \t]+'
    return t

# Ignorar comentarios
t_ignore_COMMENT = r'\#.*'

# Ignorar salto de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignorar cualquier otro caracter que no sea un espacio, tabulador o salto de línea
t_ignore = ''

def t_error(t):
    print(f"Caracter no reconocido '{t.value[0]}' en la línea {t.lineno}, columna {t.lexpos}")
    t.lexer.skip(1)

def generar_tokens(contenido):
    lexer = lex.lex()
    lexer.input(contenido)
    tokens = []
    for token in lexer:
        tokens.append(token)
    return tokens

def main():
    lexer = lex.lex()
    filename = input("Ingrese el nombre del archivo: ")
    try:
        with open(filename, 'r') as file:
            lexer.input(file.read())
            for token in lexer:
                print(token)
    except FileNotFoundError:
        print("El archivo especificado no existe")

