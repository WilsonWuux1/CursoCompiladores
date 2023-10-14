import ply.lex as lex
import os

# Lista que almacenará los resultados del análisis léxico
resultadoLexico = []

# Palabras reservadas
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

# Nombres de tokens
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

# Expresión regular para identificadores insensibles a mayúsculas y minúsculas
def t_ID(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    t.type = palabrasReservadas.get(t.value, "ID")
    return t

# Expresión regular para números enteros y decimales
def t_NUMERO(t):
    r"\d+(\.\d+)?"
    t.type = "NUMERO"
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

# Expresión regular para ignorar comentarios
def t_COMENTARIO(t):
    r"\/\/.*"
    pass

# Expresión regular para ignorar comentarios de bloque
def t_COMENTARIO_BLOQUE(t):
    r"\/\*(.|\n)*\*\/"
    pass

# Manejo de saltos de línea para hacer un seguimiento del número de línea actual en el código fuente
def t_nueva_linea(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Expresión regular para ignorar caracteres no válidos

# Ignorar espacios en blanco o tabulaciones
t_ignore = " \t"

# Manejo de errores
def t_invalido(t):
    r"."
    print(f"Caracter no válido '{t.value[0]}' en la línea {t.lineno}, posición {t.lexpos}")
    t.lexer.skip(1)
    

# Construcción del analizador léxico
lexer = lex.lex()

# Función para ejecutar el análisis léxico
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

# Función para verificar el balance de paréntesis, corchetes y llaves
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

# Función para ejecutar el verificador de balance
def ejecutar_verificador(codigo):
    if verificar_balance(codigo):
        return True
    else:
        print("¡ERROR! Hay paréntesis, corchetes o llaves abiertos o sin cerrar")
        return False

try:
    # nombre_archivo = 'C:/Users/Wuux/Desktop/Compiladores/evaluadores.txt'
    nombre_archivo= 'C:/Users/Rafael/OneDrive/Escritorio/EjercicioCompiExamen/CursoCompiladores/evaluadores.txt'
    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        entrada = archivo.read()

        # Verificar balance antes de realizar el análisis léxico
        if ejecutar_verificador(entrada):
            # Ejecutar el análisis léxico solo si el balance es correcto
            tokensValidos = ejecutar_analisis_lexico(entrada)
            for token in tokensValidos:
                print(token)

except FileNotFoundError:
    print(f"No se pudo encontrar el archivo '{nombre_archivo}'")
except Exception as e:
    print(f"Ocurrió un error al analizar el archivo: {e}")