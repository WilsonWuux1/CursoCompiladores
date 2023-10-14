import sys
import os
import ply.lex as lex
import ply.yacc as yacc
import warnings

# Examen parcial 2 
# analizador lexico 
# analizador sintactico
# estructuras de analisis for e if 
# almacenamiento de tokens


# Presentado por Wilson Estuardo Peñate y Eddison Rafael Morales
# Carnets 2100022 - 2000457

warnings.filterwarnings("ignore")

# Lista que almacenará los resultados del análisis léxico
resultadoLexico = []

# ------------- ANALIZADOR LÉXICO ----------------

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

# Expresiones regulares comunes
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_OR = r'\|'
t_AND = r'&'

t_NOT = r'~'
t_XOR = r'\^'
t_LSHIFT = r'<<'
t_RSHIFT = r'>>'
t_LOR = r'\|\|'
t_LAND = r'&&'
t_LNOT = r'!'
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='

# Operadores de asignación
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

# Operadores de incremento o decremento
t_INCREMENT = r'\+\+'
t_DECREMENT = r'--'

# Operador condicional
t_TERNARY = r'\?'

# Delimitadores
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

# Expresión regular para identificadores insensibles a mayúsculas y minúsculas
def t_ID(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    t.type = palabrasReservadas.get(t.value, "ID")
    return t

# Expresión regular para números enteros y decimales
def t_INVALID_NUMBER(t):
    r"\d+\.\d+\.\d+"
    raise ValueError(f"Número inválido '{t.value}'")

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

# Ignorar espacios en blanco o tabulaciones
t_ignore = " \t"

# Manejo de errores
def t_error(t):
    print(f"Caracter inválido '{t.value[0]}'")
    raise ValueError("Error léxico")

# Construcción del analizador léxico
lexer = lex.lex()

def ejecutar_analisis_lexico(datos):
    # Accede a la variable global resultadoLexico
    global resultadoLexico
    
    # Establece los datos de entrada para el analizador léxico (lexer)
    lexer.input(datos)
    
    # Limpia la lista resultadoLexico antes de realizar el análisis
    resultadoLexico.clear()
    
    # Bucle para obtener tokens mediante el analizador léxico
    while True:
        # Obtiene el siguiente token del analizador léxico
        tok = lexer.token()
        
        # Si no hay más tokens, sale del bucle
        if not tok:
            break
        
        # Crea una cadena de estado para el token actual
        estado = f"Tipo {tok.type} Valor {tok.value} Linea {tok.lineno} Posicion {tok.lexpos}"
        
        # Agrega el estado a la lista resultadoLexico
        resultadoLexico.append(estado)
    
    # Devuelve la lista de estados resultante del análisis léxico
    return resultadoLexico



# ------------- VERIFICA CIERRE Y APERTURA ------------

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


# --------------- ANALIZADOR SINTÁCTICO -------------------

# Reglas de producción para la estructura del programa
def p_program(p):
    """
    program : class_declaration
           | program class_declaration
    """
    
    p[0] = ("program: ", p[1:])


# Reglas de producción para declaración de la clase
def p_class_declaration(p):
    """
    class_declaration : CLASS ID LBRACE class_body RBRACE
    """
    
    p[0] = ("class: ", p[4])


# Reglas de producción para el cuerpo de la clase
def p_class_body(p):
    """
    class_body : statement main 
               | class_body statement
               | main
               | statement class_body
    """
    
    p[0] = ("body: ", p[1:])


# Reglas de producción para el método main
def p_main(p):
    ''' main : PUBLIC STATIC VOID MAIN LPAREN STRING LBRACKET RBRACKET ARGS RPAREN LBRACE statements RBRACE  '''
    
    p[0] = ("main: ", p[12])


# Reglas de producción para sentencias
def p_statement(p):
    '''statement : assignment
                | array_usage
                | print_statement
                | dcl_variable SEMI
                | for_statement
                | if_statement'''
    
    p[0] = (p[1:]) 


# Reglas de producción para expresiones
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


# Reglas de producción para condiciones
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


# Reglas de producción para incrementos o decrementos
def p_increment_or_decrement(p):
    ''' increment_or_decrement : ID INCREMENT
                               | ID DECREMENT '''
    
    p[0] = ("increment or decrement: ", p[1], p[2])

#Estructura FOR Reglas de producción para bucles for y for-each 
def p_for_statement(p):
    ''' for_statement : FOR LPAREN INT ID EQUALS NUMBER SEMI condicion SEMI increment_or_decrement RPAREN LBRACE statements RBRACE
                      | FOR LPAREN INT ID EQUALS NUMBER SEMI expression SEMI increment_or_decrement RPAREN LBRACE statements RBRACE
                      | FOR LPAREN tipo_palabra ID COLON ID RPAREN LBRACE statements RBRACE'''
    
    p[0] = ("for:", p[1:]) 


# Estructura IF Reglas de producción para sentencias if
def p_if_statement(p):
    """
    if_statement : IF LPAREN condicion RPAREN LBRACE statements RBRACE
                | IF LPAREN condicion RPAREN LBRACE statements RBRACE ELSE statements 
                | IF LPAREN condicion RPAREN LBRACE statements RBRACE ELSE LBRACE statements RBRACE
    """
    
    p[0] = (p[1:]) 


# Reglas de producción para varios argumentos
def p_args(p):
    """
    args : arg
         | args arg
    """
    
    if len(p) == 2:
        p[0] = ["args: ", p[1]]
    else:
        p[0] = p[1] + [p[2]]


# Reglas de producción de un argumento
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
    
    p[0] = ("arg: ", p[1])


# Reglas de producción para propiedades de un objeto
def p_propiedades(p):
    ''' propiedades : ID PUNTO ID'''
    
    p[0] = ("propiedades", p[1], p[3])


# Producción statements:
# - Secuencia de declaraciones que pueden consistir en una sola declaración 
# - Secuencia de declaraciones compuesta por una secuencia existente de declaraciones seguida de una declaración adicional
def p_statements(p):
    '''statements : statement
                  | statements statement'''
    
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


# Reglas de producción de asignación de valores a variables
def p_assignment(p):
    '''assignment : ID EQUALS expression SEMI'''
    
    p[0] = (p[1], p[2], p[3], p[4])


# Reglas de producción de declaración de variables:
# - Declaración de variables que contengan números
# - Declaración de variables que contengan cadena
# - Declaración de variables que contengan valor booleano
def p_dcl_variable(p):
    '''dcl_variable : tipo_number ID EQUALS NUMBER
                    | tipo_palabra ID EQUALS STRING_LITERAL
                    | tipo_booleano ID EQUALS valor_boolean'''
    
    p[0] = (p[1], p[2], p[4])


# Reglas de producción de tipo_booleano
def p_tipo_booleano(p):
    '''tipo_booleano : BOOLEAN'''
    
    p[0] = ("type_boolean: ", p[1])


# Reglas de producción de tipo_number
def p_tipo_number(p):
    '''tipo_number : INT
                    | DOUBLE'''
    
    p[0] = ("type_number: : ", p[1])


# Reglas de producción de tipo_booleano
def p_tipo_palabra(p):
    '''tipo_palabra : STRING'''
    
    p[0] = ("type_string: ", p[1])


# Reglas de producción de valores booleanos que pueden ser True o False
def p_valor_boolean(p):
    '''valor_boolean : TRUE
                    | FALSE'''
    
    p[0] = ("boolean: ", p[1])


# Reglas de producción de creación de listas
def p_array_usage(p):
    '''array_usage : tipo_number LBRACKET RBRACKET ID EQUALS LBRACE args RBRACE SEMI
                    | tipo_palabra LBRACKET RBRACKET ID EQUALS LBRACE args RBRACE SEMI'''
    
    p[0] = ("array_usage", p[1:])


# Reglas de producción de impresión
def p_print_statement(p):
    '''print_statement : SYSTEM PUNTO OUT PUNTO PRINTLN LPAREN STRING_LITERAL RPAREN SEMI
                       | SYSTEM PUNTO OUT PUNTO PRINTLN LPAREN ID RPAREN SEMI
                       | SYSTEM PUNTO OUT PUNTO PRINTLN LPAREN ID LBRACKET ID RBRACKET RPAREN SEMI'''
    
    p[0] = ('print_statement', p[7])


# Vacío
def p_empty(p):
    '''empty :'''
    pass

# Función de manejo de errores
def p_error(p):
    if p:
        print(f"Sintaxis incorrecta en la línea {p.lineno}: antes del token '{p.value}'")


# --------------- Construcción del analizador sintáctico -------------------

# Crea el analizador
parser = yacc.yacc()

# Método para imprimir el árbol
def print_ast(node, level=0):
    # Crea una cadena de espacios en blanco para la indentación
    indentation = " " * level * 2
    
    # Verifica si el nodo es una tupla (representando una producción gramatical)
    if isinstance(node, tuple):
        # Imprime el nombre del nodo (el primer elemento de la tupla)
        print(f"{indentation}{node[0]}")
        
        # Recorre los hijos del nodo e imprime cada uno recursivamente
        for child in node[1:]:
            print_ast(child, level + 1)
    
    # Verifica si el nodo es una lista
    elif isinstance(node, list):
        # Para cada elemento en la lista, imprime recursivamente
        for child in node:
            print_ast(child, level + 1)
    
    # Si el nodo no es una tupla ni una lista, es un nodo terminal, como un identificador o un número
    else:
        # Imprime el nodo terminal con la indentación adecuada
        print(f"{indentation}{node}")



# Función para llamar al análisis sintáctico
def llamadaAnalizadorSintactico(source_code):
    # Llama al analizador sintáctico para analizar el código fuente
    result = parser.parse(source_code)

    # Comprueba si el resultado del análisis sintáctico no es None (indicando éxito)
    if result is not None:
        # Imprime un mensaje indicando que el análisis sintáctico fue exitoso
        print("Análisis sintáctico exitoso")

        # Imprime la representación del árbol de análisis sintáctico utilizando la función print_ast
        print_ast(result)
    else:
        # Imprime un mensaje indicando que hubo un error en el análisis sintáctico
        print("Error de análisis sintáctico")


# ----------------- LÓGICA DE EJECUCIÓN ------------------------

# Crea el nombre del nuevo archivo
def nombre__crear_archivo():
    contador = 1
    while True:
        nombre_archivo = f"Mistokens{contador}.txt"
        if not os.path.exists(nombre_archivo):
            break
        contador += 1
    return nombre_archivo

# Ejecuta el análisis léxico
def ejecutarALexico(entrada):
    # Obtiene la lista de tokens válidos mediante el análisis léxico
    tokensValidos = ejecutar_analisis_lexico(entrada)

    # Crea un nombre de archivo único para almacenar los tokens
    nombre_archivo = nombre__crear_archivo()

    try:
        # Intenta abrir un archivo en modo escritura ('w') con codificación UTF-8
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            # Escribe cada token en una línea del archivo
            for token in tokensValidos:
                archivo.write(f"{token}\n")
            
            # Imprime un mensaje indicando que los tokens se han almacenado en el archivo
            print(f"Los tokens se han almacenado en el archivo '{nombre_archivo}'.")
        
        # Cierra el archivo automáticamente al salir del bloque 'with'
    except Exception as e:
        # Maneja excepciones en caso de errores durante la escritura del archivo
        print(f"Ocurrió un error al almacenar los tokens en el archivo: {e}")

    # Imprime cada token en la consola
    for token in tokensValidos:
        print(token)

# Ejecuta el análisis sintáctico
def ejecucionAnalizador(nombre_archivo):
    
    with open(nombre_archivo, 'r') as archivo:
        codigo = archivo.read()
        archivo.close()
        if not ejecutar_verificador(codigo):
            sys.exit(1)
    llamadaAnalizadorSintactico(codigo)

# Principal
def main():
    try:
        # nombre_archivo = 'C:/Users/Wuux/Desktop/Compiladores/evaluadores.txt'
        nombre_archivo = 'C:/Users/Rafael/OneDrive/Escritorio/EjercicioCompiExamen/CursoCompiladores/evaluadores.txt'
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            entrada = archivo.read()
            ejecutarALexico(entrada)
        
        ejecucionAnalizador(nombre_archivo)
    except FileNotFoundError:
        print(f"No se pudo encontrar el archivo '{nombre_archivo}'")
    except Exception as e:
        print(f"Ocurrió un error al analizar el archivo: {e}")


if __name__ == "__main__":
    main()
