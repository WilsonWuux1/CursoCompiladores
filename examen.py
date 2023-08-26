import os
import re

def esDecimal(token):    
    parts = token.split('.')
    return len(parts) == 2 and all(part.isdigit() for part in parts)

def tokenize_java_code(java_code):
    palabrasReservadas = { 
        "while", "if", "return", "cout", "cin",
        "abstract", "continue", "for", "new", "switch",
        "boolean", "default", "goto", "null", "synchronized",
        "break", "do", "package", "this",
        "byte", "double", "implements", "private", "threadsafe",
        "byvalue", "else", "import", "protected", "throw",
        "case", "extends", "instanceof", "public", "transient",
        "catch", "false", "int", "true",
        "char", "final", "interface", "short", "try",
        "class", "finally", "long", "static", "void",
        "const", "float", "native", "super", "while",
        "cast", "future", "generic", "inner", "operator",
        "outer", "rest", "var"
    }
    identifiCadores = set()
    literales = set()
    operadores = {
        ".","++", "--", "!", "~", "instanceof",
        "*", "/", "%", "+", "-",
        "<<", ">>", ">>>", "<", ">", "<=", ">=", "==", "!=",
        "&", "^", "|", "&&", "||", "[]",
        "?", ":", "=", "op=", ","
    }
    delimitadores = {";", ",", "(", ")", "{", "}", "[", "]"}
    comentarios = {"//", "/", "/", "/**"}

    tokens = []
    line_number = 1  # Mantenemos el número de línea actual
    for line in java_code.split('\n'):

        for word in re.findall(r'\w+|[^\w\s]+|".*?"', line):
        #    print("Processing word:", word)
            if word in palabrasReservadas:
                tokens.append(("Keyword", word,line_number))
            elif word in operadores:
                # tokens.append(("Operator", word))
                if word == "+":
                    token_type = "SIGNO_MAS"
                elif word == "-":
                    token_type = "SIGNO_MENOS"
                elif word == "*":
                    token_type = "SIGNO_MULTIPLICACION"
                elif word == "/":
                    token_type = "SIGNO_DIVISION"
                elif word == ".":
                    token_type = "PUNTO"
                elif word == "++":
                    token_type = "INCREMENTO"
                elif word == "--":
                    token_type = "DECREMENTO"
                elif word == "!":
                    token_type = "NOT"
                elif word == "~":
                    token_type = "COMPLEMENTO"
                elif word == "instanceof":
                    token_type = "INSTANCEOF"
                elif word == "<<":
                    token_type = "DESPLAZAMIENTO_IZQUIERDO"
                elif word == ">>":
                    token_type = "DESPLAZAMIENTO_DERECHO"
                elif word == ">>>":
                    token_type = "DESPLAZAMIENTO_DERECHO_SIN_SIGNO"
                elif word == "<<<":
                    token_type = "DESPLAZAMIENTO_IZQUIERDO_SIN_SIGNO"
                elif word == "<":
                    token_type = "MENOR_QUE"
                elif word == ">":
                    token_type = "MAYOR_QUE"
                elif word == ">=":
                    token_type = "MENOR_O_IGUAL_QUE"
                elif word == "<=":
                    token_type = "MAYOR_O_IGUAL_QUE"
                elif word == "==":
                    token_type = "IGUAL"
                elif word == "!=":
                    token_type = "NO_IGUAL"
                elif word == "&":
                    token_type = "AND_BIT_A_BIT"
                elif word == "^":
                    token_type = "XOR_BIT_A_BIT"
                elif word == "|":
                    token_type = "OR_BIT_A_BIT"
                elif word == "&&":
                    token_type = "AND_LOGICO"
                elif word == "||":
                    token_type = "OR_LOGICO"
                elif word == "?":
                    token_type = "OPERADOR_TERNARIO"
                elif word == ":":
                    token_type = "DOS_PUNTOS"
                elif word == "=":
                    token_type = "ASIGNACION"
                elif word == "op=":
                    token_type = "OPERADOR_ASIGNACION"
                elif word == ",":
                    token_type = "COMA"
                elif word == "[]":
                    token_type = "DOBLE_CORCHETE"
                else:
                    token_type = "ERROR"
                tokens.append((token_type, word, line_number))
            elif word in delimitadores:
                tokens.append(("Delimiter", word,line_number))
            elif re.match(r'^[a-zA-Z_]\w*$', word):
                identifiCadores.add(word)
                tokens.append(("Identifier", word,line_number))
            elif re.match(r"[0-9]+\.[0-9]+", word):
                if esDecimal(word):
                    tokens.append(("NUMERO_DECIMAL", word, line_number))
                else:
                    tokens.append(("ERROR_DECIMAL", word, line_number))
            elif re.match(r"[0-9]+", word):
                
                tokens.append(("NUMERO_ENTERO", word, line_number))
            elif re.match(r'^\d+\.\d+$', word):
                 literales.add(word)
                 tokens.append(("Float Literal", word,line_number))
            elif re.match(r'"[^"]*"', word):
                 literales.add(word)
                 tokens.append(("String Literal", word,line_number))
            else:
                raise ValueError(f"Unrecognized token: '{word}'")

            line_number += 1

    return tokens, identifiCadores, literales

nombre_archivo = "evaluadores.txt"
ruta_archivo = "C:/Users/Rafael/OneDrive/Escritorio/EjercicioCompiExamen/CursoCompiladores"
# ruta_archivo = "C:/Users/Wuux/Desktop/Compiladores"  # Coloca la ruta correcta aquí
ruta_completa = os.path.join(ruta_archivo, nombre_archivo)

if os.path.exists(ruta_completa):
    archivo = open(ruta_completa, "r", encoding="utf-8")
    java_code = archivo.read()
    archivo.close()

    try:
        tokens, identifiCadores, literales = tokenize_java_code(java_code)

        categories = {
            "Identificadores": identifiCadores,
            "Literales": literales
        }

        for token_type, token_value, line_number in tokens:
            print(f"{token_type:20} {token_value:10} Linea: {line_number}")

        for category, values in categories.items():
            print(f"{category}: {', '.join(values)}")
    except ValueError as e:
        print("Error:", e)
else:
    print("El archivo no existe.")