import sys
import os
import ply.yacc as yacc
import ply.lex as lex

# --------------- ANALIZADOR SINTÁCTICO -------------------

tokens = ['LBRACE', 'RBRACE', 'ID']

# Regular expression rules for simple tokens
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'


# Build the lexer and parser
lexer = lex.lex()


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
    ''' main : PUBLIC STATIC VOID MAIN LPAREN ID LBRACKET RBRACKET ARGS RPAREN LBRACE statements RBRACE  '''
    
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


# Reglas de producción para bucles for y for-each 
def p_for_statement(p):
    ''' for_statement : FOR LPAREN INT ID EQUALS NUMBER SEMI condicion SEMI increment_or_decrement RPAREN LBRACE statements RBRACE
                      | FOR LPAREN INT ID EQUALS NUMBER SEMI expression SEMI increment_or_decrement RPAREN LBRACE statements RBRACE
                      | FOR LPAREN tipo_palabra ID COLON ID RPAREN LBRACE statements RBRACE'''
    
    p[0] = ("for:", p[1:]) 


# Reglas de producción para sentencias if
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

# ----------------- LÓGICA DE EJECUCIÓN ------------------------
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
    

# Ejecuta el análisis sintáctico
def ejecutarASintactico(nombre_archivo):
    result = parser().parse(nombre_archivo)
    if result is not None:
        print("Análisis sintáctico exitoso")
        # print_ast(result)
    else:
        print("Error de análisis sintáctico")

# Principal
def main():
    listadoTokens='''Tipo PUBLIC Valor public Linea 1 Posicion 0       
Tipo CLASS Valor class Linea 1 Posicion 7
Tipo ID Valor HolaMundo Linea 1 Posicion 13       
Tipo PUBLIC Valor public Linea 2 Posicion 26      
Tipo STATIC Valor static Linea 2 Posicion 33      
Tipo VOID Valor void Linea 2 Posicion 40
Tipo MAIN Valor main Linea 2 Posicion 45
Tipo ID Valor tring Linea 2 Posicion 51
Tipo ARGS Valor args Linea 2 Posicion 59
Tipo SYSTEM Valor System Linea 3 Posicion 73      
Tipo ID Valor ut Linea 3 Posicion 81
Tipo ID Valor rintln Linea 3 Posicion 85
Tipo ID Valor Hola Linea 3 Posicion 93
Tipo ID Valor Mundo Linea 3 Posicion 98'''
    ejecutarASintactico(listadoTokens)
   
if __name__ == "__main__":
    main()
