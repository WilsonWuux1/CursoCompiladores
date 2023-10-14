import ply.lex as lex
import os

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

def t_ID(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    t.type = palabrasReservadas.get(t.value, "ID")
    return t

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

def t_invalido(t):
    r"."
    print(f"Caracter no válido '{t.value[0]}' en la línea {t.lineno}, posición {t.lexpos}")
    t.lexer.skip(1)
    

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


        # nombre_archivo = 'C:/Users/Wuux/Desktop/Compiladores/evaluadores.txt'
nombre_archivo = 'C:/Users/Rafael/OneDrive/Escritorio/EjercicioCompiExamen/CursoCompiladores/evaluadores.txt'
with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
    entrada = archivo.read()
    tokensValidos = ejecutar_analisis_lexico(entrada)
    for token in tokensValidos:
        print(token)



