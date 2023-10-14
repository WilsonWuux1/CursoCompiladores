import sys
import os
import ply.lex as lex
import ply.yacc as yacc
import warnings

warnings.filterwarnings("ignore")

resultadoLexico = []

palabrasReservadas = {
    "int": "INT",
    "char": "CHAR",
    "float": "FLOAT",
    "if": "IF",
    "else": "ELSE",
    "do": "DO",
    "while": "WHILE",
    "return": "RETURN",
    "void": "VOID",
    "#include": "INCLUDE",
    "String": "STRING",
    "args": "ARGS",
    "public": "PUBLIC",
    "static": "STATIC",
    "main": "MAIN",
    "class": "CLASS",
    "System": "SYSTEM",
    "out": "OUT",
    "println": "PRINTLN",
    "true": "TRUE",
    "false": "FALSE",
    "boolean": "BOOLEAN",
    "double": "DOUBLE",
    "for": "FOR",
    "package": "PACKAGE",
}

tokens = list(palabrasReservadas.values()) + [
    'ID', 'NUMBER', 'TYPEID', 'INTEGER', 'STRING_LITERAL', 'CHARACTER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO',
    'OR', 'AND', 'NOT', 'XOR', 'LSHIFT', 'RSHIFT',
    'LOR', 'LAND', 'LNOT',
    'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',
    'EQUALS', 'TIMESEQUAL', 'DIVEQUAL', 'MODEQUAL', 'PLUSEQUAL', 'MINUSEQUAL',
    'LSHIFTEQUAL', 'RSHIFTEQUAL', 'ANDEQUAL', 'XOREQUAL', 'OREQUAL',
    'INCREMENT', 'DECREMENT', 'TERNARY',
    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET',
    'LBRACE', 'RBRACE', 'COMMA', 'PUNTO', 'SEMI', 'COLON',
]


t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_OR = r'\|'
t_AND = r'&'

t_NOT              = r'~'
t_XOR              = r'\^'
t_LSHIFT           = r'<<'
t_RSHIFT           = r'>>'
t_LOR              = r'\|\|'
t_LAND             = r'&&'
t_LNOT             = r'!'
t_LT               = r'<'
t_GT               = r'>'
t_LE               = r'<='
t_GE               = r'>='
t_EQ               = r'=='
t_NE               = r'!='

t_EQUALS = r'='
t_TIMESEQUAL = r'\*='
t_DIVEQUAL = r'/='
t_MODEQUAL = r'%='
t_PLUSEQUAL = r'\+='
t_MINUSEQUAL = r'-='
t_LSHIFTEQUAL = r'<<='
t_RSHIFTEQUAL = r'>>='
t_ANDEQUAL = r'&='
t_OREQUAL = r'\|='
t_XOREQUAL = r'\^='

t_INCREMENT        = r'\+\+'
t_DECREMENT        = r'--'

t_TERNARY          = r'\?'

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','
t_PUNTO = r'\.'
t_SEMI = r';'
t_COLON = r':'
t_STRING_LITERAL = r'"[^"]*"'


def t_ID(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    t.type = palabrasReservadas.get(t.value, "ID")
    return t

def t_INVALID_NUMBER(t):
    r"\d+\.\d+\.\d+"
    raise ValueError(f"Número inválido '{t.value}'")

def t_NUMERO(t):
    r"\d+(\.\d+)?"
    t.type = "NUMERO"
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_COMENTARIO(t):
    r"\/\/.*"
    pass

def t_COMENTARIO_BLOQUE(t):
    r"\/\*(.|\n)*\*\/"
    pass

def t_nueva_linea(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = " \t"

def t_error(t):
    print(f"Caracter inválido '{t.value[0]}'")
    raise ValueError("Error léxico")

lexer = lex.lex()

def ejecutar_analisis_lexico(datos):
    global resultadoLexico
    lexer.input(datos)
    resultadoLexico.clear()
    while True:
        tok = lexer.token()
        if not tok:
            break
        estado = f"Tipo {tok.type} Valor {tok.value} Linea {tok.lineno} Posicion {tok.lexpos}"
        resultadoLexico.append(estado)
    return resultadoLexico



def verificar_balance(texto):
    pila = []
    pares = {')': '(', ']': '[', '}': '{'}

    for char in texto:
        if char in '([{':
            pila.append(char)
        elif char in ')]}':
            if not pila or pila.pop() != pares[char]:
                return False

    return len(pila) == 0

def ejecutar_verificador(codigo):
    if verificar_balance(codigo):
        return True
    else:
        print("¡ERROR! Hay paréntesis, corchetes o llaves abiertos o sin cerrar")
        return False




def p_program(p):
    """
    program : class_declaration
           | program class_declaration
    """
    
    p[0] = ("program: ",p[1:])
    


# Reglas de producción para declaración de la clase
def p_class_declaration(p):
    """
    class_declaration : CLASS ID LBRACE class_body RBRACE
    """
    
    p[0] = ("class: ",p[4])
    


def p_class_body(p):
    """
    class_body : statement main 
               | class_body statement
               | main
               | statement class_body
    """
    
    p[0] = ("body: ", p[1:])
    

def p_main(p):
    ''' main : PUBLIC STATIC VOID MAIN LPAREN STRING LBRACKET RBRACKET ARGS RPAREN LBRACE statements RBRACE  '''
    
    p[0] = ("main: ", p[12])
    


def p_statement(p):
    '''statement : assignment
                | array_usage
                | print_statement
                | dcl_variable SEMI
                | for_statement
                | if_statement'''
    
    p[0] = ( p[1:]) 
    


def p_expression(p):
    """
    expression : ID
               | NUMBER
               | ID EQUALS propiedades
               | ID GT propiedades
               | ID GE propiedades
               | ID LE propiedades
               | ID LT propiedades
               | NOT expression
    """
    
    if len(p) == 4:
        p[0] = (p[1], p[2], p[3])
    else:
        p[0] = (p[1])
    


def p_condicion(p):
    ''' condicion : ID EQUALS NUMBER
               | ID GT NUMBER
               | ID GE NUMBER
               | ID LE NUMBER
               | ID LT NUMBER
               | ID AND NUMBER
               | ID OR NUMBER
               | NUMBER EQUALS NUMBER
               | NUMBER GT NUMBER
               | NUMBER GE NUMBER
               | NUMBER LE NUMBER
               | NUMBER LT NUMBER
               | ID AND ID
               | ID OR ID
               | ID EQ ID 
               | ID EQ STRING_LITERAL '''
    
    p[0] = ("condicion: ", p[1], p[2], p[3])
    


def p_increment_or_decrement(p):
    ''' increment_or_decrement : ID INCREMENT
                               | ID DECREMENT '''
    
    p[0] = ("increment or decrement: ", p[1], p[2])
    


def p_for_statement(p):
    ''' for_statement : FOR LPAREN INT ID EQUALS NUMBER SEMI condicion SEMI increment_or_decrement RPAREN LBRACE statements RBRACE
                      | FOR LPAREN INT ID EQUALS NUMBER SEMI expression SEMI increment_or_decrement RPAREN LBRACE statements RBRACE
                      | FOR LPAREN tipo_palabra ID COLON ID RPAREN LBRACE statements RBRACE'''
    
    p[0] = ("for:", p[1:]) 
    


def p_if_statement(p):
    """
    if_statement : IF LPAREN condicion RPAREN LBRACE statements RBRACE
                | IF LPAREN condicion RPAREN LBRACE statements RBRACE ELSE statements 
                | IF LPAREN condicion RPAREN LBRACE statements RBRACE ELSE LBRACE statements RBRACE
    """
    
    p[0] = ( p[1:]) 
    


def p_args(p):
    """
    args : arg
         | args arg
    """
    
    if len(p) == 2:
        p[0] = ["args: ",p[1]]
    else:
        p[0] = p[1] + [p[2]]
    


def p_arg(p):
    """
    arg : ID
         | STRING_LITERAL
         | NUMBER
         | NOT arg
         | ID COMMA
         | STRING_LITERAL COMMA
         | NUMBER COMMA
    """
    
    p[0] = ("arg: ",p[1])
    


def p_propiedades(p):
    ''' propiedades : ID PUNTO ID'''
    
    p[0] = ("propiedades", p[1], p[3])
    


def p_statements(p):
    '''statements : statement
                  | statements statement'''
    
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]
    
    

def p_assignment(p):
    '''assignment : ID EQUALS expression SEMI'''
    
    p[0] = (p[1], p[2], p[3], p[4])

def p_dcl_variable(p):
    '''dcl_variable : tipo_number ID EQUALS NUMBER
                    | tipo_palabra ID EQUALS STRING_LITERAL
                    | tipo_booleano ID EQUALS valor_boolean'''
    
    p[0] = (p[1], p[2], p[4])
    


def p_tipo_booleano(p):
    '''tipo_booleano : BOOLEAN'''
    
    p[0] = ("type_boolean: ", p[1])
    

def p_tipo_number(p):
    '''tipo_number : INT
                    | DOUBLE'''
    
    p[0] = ("type_number: : ", p[1])
    

def p_tipo_palabra(p):
    '''tipo_palabra : STRING'''
    
    p[0] = ("type_string: ", p[1])
    

def p_valor_boolean(p):
    '''valor_boolean : TRUE
                    | FALSE'''
    
    p[0] = ("boolean: ", p[1])
    

def p_array_usage(p):
    '''array_usage : tipo_number LBRACKET RBRACKET ID EQUALS LBRACE args RBRACE SEMI
                    | tipo_palabra LBRACKET RBRACKET ID EQUALS LBRACE args RBRACE SEMI'''
    
    p[0] = ( "array_usage", p[1:])
    

def p_print_statement(p):
    '''print_statement : SYSTEM PUNTO OUT PUNTO PRINTLN LPAREN STRING_LITERAL RPAREN SEMI
                       | SYSTEM PUNTO OUT PUNTO PRINTLN LPAREN ID RPAREN SEMI
                       | SYSTEM PUNTO OUT PUNTO PRINTLN LPAREN ID LBRACKET ID RBRACKET RPAREN SEMI'''
    
    p[0] = ('print_statement', p[7])
    

def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    if p:
        print(f"Sintaxis incorrecta en la línea {p.lineno}: antes del token '{p.value}'")



parser = yacc.yacc()

def print_ast(node, level=0):
    indentation = " " * level * 2
    if isinstance(node, tuple):
        print(f"{indentation}{node[0]}")
        for child in node[1:]:
            print_ast(child, level + 1)
    elif isinstance(node, list):
        for child in node:
            print_ast(child, level + 1)
    else:
        print(f"{indentation}{node}")


def call_Parse(source_code):
    result = parser.parse(source_code)
    if result is not None:
        print("Análisis sintáctico exitoso")
        print_ast(result)
    else:
        print("Error de análisis sintáctico")
        



def nombre__crear_archivo():
    contador = 1
    while True:
        nombre_archivo = f"tokens_{contador}.txt"
        if not os.path.exists(nombre_archivo):
            break
        contador += 1
    return nombre_archivo

def ejecutarALexico(entrada):
    tokensValidos = ejecutar_analisis_lexico(entrada)

    nombre_archivo= nombre__crear_archivo()
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            for token in tokensValidos:
                archivo.write(f"{token}\n")
            print(f"Los tokens se han almacenado en el archivo '{nombre_archivo}'.")
        archivo.close()
    except Exception as e:
        print(f"Ocurrió un error al almacenar los tokens en el archivo: {e}")
        
    for token in tokensValidos:
        print(token)

def ejecutarASintactico(nombre_archivo):
    
    with open(nombre_archivo, 'r') as archivo:
        codigo = archivo.read()
        archivo.close()
        if not ejecutar_verificador(codigo):
            sys.exit(1)
    call_Parse(codigo)

def main():
    try:
        # nombre_archivo = 'C:/Users/Wuux/Desktop/Compiladores/evaluadores.txt'
        nombre_archivo = 'C:/Users/Rafael/OneDrive/Escritorio/Analizador Léxico para lenguaje Java/CursoCompiladores/evaluadores.txt'
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            entrada = archivo.read()
            ejecutarALexico(entrada)
        
        ejecutarASintactico(nombre_archivo)
    except FileNotFoundError:
        print(f"No se pudo encontrar el archivo '{nombre_archivo}'")
    except Exception as e:
        print(f"Ocurrió un error al analizar el archivo: {e}")


if __name__ == "__main__":
    main()
