from ply import lex
import pandas as pd
import matplotlib.pyplot as plt

PATH = 'dados.txt'

try:
    with open(PATH, 'r') as arquivo:
        conteudo = arquivo.read()
except FileNotFoundError:
    print(f"Arquivo não encontrado '{PATH}' !!!")
except Exception as e:
    print(f"ERRO: '{e}'")

file = conteudo

reserved = {
    'some': 'SOME',
    'all': 'ALL',
    'value': 'VALUE',
    'min': 'MIN',
    'max': 'MAX',
    'exactly': 'EXACTLY',
    'that': 'THAT',
    'not': 'NOT',
    'and': 'AND',
    'or': 'OR',
    'only': 'ONLY',
    'class': 'CLASS',
    'equivalent': 'EQUIVALENTTO',
    'individuals': 'INDIVIDUALS',
    'subclassof': 'SUBCLASSOF',
    'disjointclasses': 'DISJOINTCLASSES'
}

tokens = [
    'ID',
    'HAS',
    'IS',
    'OF',
    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET',
    'LBRACE',
    'RBRACE',
    'COMMA',
    'GT',
    'LT',
    'EQ',
    'COLON',
    'CARDINALITY',
    'DATA_TYPE',
    'PROPERTY'
] + list(reserved.values())

t_SOME = r'SOME'
t_ALL = r'ALL'
t_VALUE = r'VALUE'
t_MIN = r'MIN'
t_MAX = r'MAX'
t_EXACTLY = r'EXACTLY'
t_THAT = r'THAT'
t_NOT = r'NOT'
t_AND = r'AND'
t_OR = r'OR'
t_CLASS = r'Class'
t_EQUIVALENTTO = r'EquivalentTo'
t_INDIVIDUALS = r'Individuals'
t_SUBCLASSOF = r'SubClassOf'
t_DISJOINTCLASSES = r'DisjointClasses'
t_HAS = r'has'
t_IS = r'is'
t_OF = r'Of'
t_ONLY = r'only'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_COMMA = r','
t_GT = r'>'
t_LT = r'<'
t_COLON = r':'
t_EQ = r'='

def t_INDIVIDUAL(t):
    r'[A-Z][a-zA-Z0-9]*\d+'
    t.type = 'INDIVIDUALS'
    return t

def t_PROPERTY_IS_OF(t):
    r'\bis\w*Of\b'
    t.type = 'PROPERTY'
    return t

def t_PROPERTY_HAS(t):
    r'\bhas\w*\b'
    t.type = 'PROPERTY'
    return t

def t_DATA_TYPE(t):
    r'(owl:|rdfs:|xsd:)\w+'
    t.type = 'DATA_TYPE'
    return t

def t_CARDINALITY(t):
    r'\d+'
    t.type = 'CARDINALITY'
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_ID(t):
    r'[a-z][a-z]*'
    t.type = 'ID'
    return t

def t_Class(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = 'CLASS'
    if t.value.upper() in ('EQUIVALENTTO', 'SUBCLASSOF', 'DISJOINTCLASSES', 'INDIVIDUALS'):
        t.type = t.value.upper()
    return t

def t_error(t):
    print(f"Caractere ilegal: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

lexer.input(file)

found_tokens = []
id_count = 0
property_count = 0
individual_count = 0
cardinalidade_count = 0
data_type_count = 0
reserved_count = 0

while True:
    tok = lexer.token()
    if not tok:
        break
    found_tokens.append((tok.lineno, tok.type, tok.value))
    if tok.type == 'ID' and tok.value.upper() == 'INDIVIDUALS':
        individual_count += 1
    elif tok.type == 'ID':
        id_count += 1
    elif tok.type == 'PROPERTY':
        property_count += 1
    elif tok.type == 'INDIVIDUALS':
        individual_count += 1
    elif tok.type == 'CARDINALITY':
        cardinalidade_count += 1
    elif tok.type == 'DATA_TYPE':
        data_type_count += 1
    elif tok.type in list(reserved.values()):
        reserved_count += 1

for lineno, token_type, token_value in found_tokens:
    print(f'Linha {lineno}: Token: {token_type}, Valor: {token_value}')

print(f"######################################## Resumo #########################################")
print(f"#                           Quantidade de IDs: {id_count}\t\t\t\t\t#")
print(f"#                           Quantidade de Propriedades: {property_count}\t\t\t\t#")
print(f"#                           Quantidade de Indivíduos: {individual_count}\t\t\t\t#")
print(f"#                           Quantidade de Cardinalidades: {cardinalidade_count}\t\t\t\t#")
print(f"#                           Quantidade de Tipos de dados: {data_type_count}\t\t\t\t#")
print(f"#                           Quantidade de Palavras reservadas: {reserved_count}\t\t\t#")
print(f"#########################################################################################")

# Dados do resumo
data = {
    "Quantidade de IDs": [id_count],
    "Quantidade de Propriedades": [property_count],
    "Quantidade de Indivíduos": [individual_count],
    "Quantidade de Cardinalidades": [cardinalidade_count],
    "Quantidade de Tipos de dados": [data_type_count],
    "Quantidade de Palavras reservadas": [reserved_count]
}

# Criar um DataFrame
df = pd.DataFrame(data)

# Criar uma tabela
fig, ax = plt.subplots(figsize=(8, 2))  # Ajuste o tamanho conforme necessário
ax.axis('off')
table = ax.table(cellText=df.values,
                 colLabels=df.columns,
                 cellLoc='center',
                 loc='center')

# Salvar como PNG com maior resolução (aumente dpi conforme necessário)
plt.savefig('resumo_tabela.png', bbox_inches='tight', dpi=300)