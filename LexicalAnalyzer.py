from ply import lex

# Definindo os tokens para o analisador léxico
tokens = (
    'CLASS',
    'INDIVIDUAL',
    'OBJECT_PROPERTY',
    'DATA_PROPERTY',
    'HAS_VALUE',
    'SOME_VALUES_FROM',
    'OPEN_PAREN',
    'CLOSE_PAREN',
    'COMMA',
    'COLON',
    'ID',
)

# Expressões regulares para os tokens
t_CLASS = r'Class'
t_INDIVIDUAL = r'Individual'
t_OBJECT_PROPERTY = r'ObjectProperty'
t_DATA_PROPERTY = r'DataProperty'
t_HAS_VALUE = r'hasValue'
t_SOME_VALUES_FROM = r'someValuesFrom'
t_OPEN_PAREN = r'\('
t_CLOSE_PAREN = r'\)'
t_COMMA = r','
t_COLON = r':'

# Expressão regular para identificadores (IDs)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = 'ID'
    return t

# Ignorar espaços em branco e tabulações
t_ignore = ' \t'

# Contador de linhas para rastrear a linha atual
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Tratamento de erro
def t_error(t):
    print(f"Caractere ilegal: {t.value[0]}")
    t.lexer.skip(1)

# Criar o analisador léxico
lexer = lex.lex()

# Testar o analisador léxico
data = """
Class: Animal
    SubClassOf: hasLegs some (Leg and hasColor some xsd:string)
"""

lexer.input(data)

while True:
    tok = lexer.token()
    if not tok:
        break  # Não há mais tokens
    print(tok)
