from ply import lex

# Definindo os tokens para o analisador léxico
tokens = (
    'SOME',
    'ALL',
    'VALUE',
    'MIN',
    'MAX',
    'EXACTLY',
    'THAT',
    'NOT',
    'AND',
    'OR',
    'CLASS',
    'EQUIVALENTTO',
    'INDIVIDUALS',
    'SUBCLASSOF',
    'DISJOINTCLASSES',
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
    'COLON',
    'CARDINALITY',
    'DATA_TYPE',
)

# Expressões regulares para os tokens
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

# Expressão regular para identificadores (IDs)
def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = 'ID'
    if t.value.upper() in ('SOME', 'AND', 'VALUE', 'INDIVIDUALS'):
        t.type = t.value.upper()  # Se for uma palavra reservada, ajusta o tipo
    return t

# Expressão regular para nomes de indivíduos
def t_INDIVIDUAL(t):
    r'[A-Z][a-zA-Z0-9]*\d+'
    t.type = 'INDIVIDUAL'
    return t

# Expressão regular para tipos de dados
def t_DATA_TYPE(t):
    r'(owl:|rdfs:|xsd:)\w+'
    t.type = 'DATA_TYPE'
    return t

# Expressão regular para cardinalidades
def t_CARDINALITY(t):
    r'\d+'
    t.type = 'CARDINALITY'
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
Class: Customer
EquivalentTo:
Person
and (purchasedPizza some Pizza)
and (hasPhone some xsd:string)
Individuals:
Customer1,
Customer10,
Customer2,
Customer3,
Customer4,
Customer5,
Customer6,
Customer7,
Customer8,
Customer9
Class: Employee
SubClassOf:
Person
and (ssn min 1 xsd:string)
Individuals:
Chef,
Manager,
Waiter1,
Waiter2
Class: Pizza
SubClassOf:
hasBase some PizzaBase,
hasCaloricContent some xsd:integer
DisjointClasses:
Pizza, PizzaBase, PizzaTopping
Individuals:
CustomPizza1,
CustomPizza2
Class: CheesyPizza
EquivalentTo:
Pizza
and (hasTopping some CheeseTopping)
Individuals:
CheesyPizza1
Class: HighCaloriePizza
EquivalentTo:
Pizza
and (hasCaloricContent some xsd:integer[>= 400])
Class: InterestingPizza
EquivalentTo:
Pizza
and (hasTopping min 3 PizzaTopping)
Class: LowCaloriePizza
EquivalentTo:
Pizza
and (hasCaloricContent some xsd:integer[< 400])
Class: NamedPizza
SubClassOf:
Pizza
Class: AmericanaHotPizza
SubClassOf:
NamedPizza,
hasTopping some JalapenoPepperTopping,
hasTopping some MozzarellaTopping,
hasTopping some PepperoniTopping,
hasTopping some TomatoTopping
DisjointClasses:
AmericanaHotPizza, AmericanaPizza, MargheritaPizza, SohoPizza
Individuals:
AmericanaHotPizza1,
AmericanaHotPizza2,
AmericanaHotPizza3,
ChicagoAmericanaHotPizza1
Class: AmericanaPizza
SubClassOf:
NamedPizza,
hasTopping some MozzarellaTopping,
hasTopping some PepperoniTopping,
hasTopping some TomatoTopping
DisjointClasses:
AmericanaHotPizza, AmericanaPizza, MargheritaPizza, SohoPizza
Individuals:
AmericanaPizza1,
AmericanaPizza2
Class: MargheritaPizza
SubClassOf:
NamedPizza,
hasTopping some MozzarellaTopping,
hasTopping some TomatoTopping,
hasTopping only
(MozzarellaTopping or TomatoTopping)
DisjointClasses:
AmericanaHotPizza, AmericanaPizza, MargheritaPizza, SohoPizza
Individuals:
MargheritaPizza1,
MargheritaPizza2
Class: SohoPizza
SubClassOf:
NamedPizza,
hasTopping some MozzarellaTopping,
hasTopping some OliveTopping,
hasTopping some ParmesanTopping,
hasTopping some TomatoTopping,
hasTopping only
(MozzarellaTopping or OliveTopping or ParmesanTopping or TomatoTopping)
DisjointClasses:
AmericanaHotPizza, AmericanaPizza, MargheritaPizza, SohoPizza
Individuals:
SohoPizza1,
SohoPizza2
Class: SpicyPizza
EquivalentTo:
Pizza
and (hasTopping some (hasSpiciness value Hot))
Class: VegetarianPizza
EquivalentTo:
Pizza
and (hasTopping only
(CheeseTopping or VegetableTopping))
Class: PizzaBase
DisjointClasses:
Pizza, PizzaBase, PizzaTopping
Class: PizzaTopping
DisjointClasses:
Pizza, PizzaBase, PizzaTopping
Class: Spiciness
EquivalentTo:
{Hot , Medium , Mild}                                                                                                                                                                                                                                                                                                                                  
"""

lexer.input(data)

found_tokens = []
id_count = 0
property_count = 0
individual_count = 0

while True:
    tok = lexer.token()
    if not tok:
        break  # Não há mais tokens
    found_tokens.append((tok.lineno, tok.type, tok.value))
    if tok.type == 'ID' and tok.value.upper() == 'INDIVIDUALS':
        individual_count += 1
    elif tok.type == 'ID':
        id_count += 1
    elif tok.type in ('HAS', 'IS', 'OF'):
        property_count += 1
    elif tok.type == 'INDIVIDUAL':
        individual_count += 1

# Imprimir o que foi encontrado para cada token
for lineno, token_type, token_value in found_tokens:
    print(f'Linha {lineno}: Token: {token_type}, Valor: {token_value}')

# Resumo
print("\nResumo:")
print(f"Quantidade de IDs: {id_count}")
print(f"Quantidade de Propriedades: {property_count}")
print(f"Quantidade de Indivíduos: {individual_count}")