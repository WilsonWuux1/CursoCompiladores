import os
import re

def esLiteralValida(literal):
    # Validar que el primer carácter sea alfabético, '_', o '$'
    if not re.match(r'^[a-zA-Z$_]', literal):
        return False

    # Validar que el resto de los caracteres sean alfanuméricos, '_', o '$'
    if not re.match(r'^[a-zA-Z0-9$_]*$', literal[1:]):
        return False

    return True

def esDecimal(token):    
    parts = token.split('.')
    return len(parts) == 2 and all(part.isdigit() for part in parts)

def Analizador(textoArchivo):
    
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
    numeroLinea = 1  # Mantenemos el número de línea actual
    for line in textoArchivo.split('\n'):

        for datoTexto in re.findall(r'\w+|[^\w\s]+|".*?"', line):
        #    print("Processing datoTexto:", datoTexto)
            if datoTexto in palabrasReservadas:
                tokens.append(("PALABRA_RESERVADA", datoTexto,numeroLinea))
            elif datoTexto in operadores:
                # tokens.append(("Operator", datoTexto))
                if datoTexto == "+":
                    tipoToken = "SIGNO_MAS"
                elif datoTexto == "-":
                    tipoToken = "SIGNO_MENOS"
                elif datoTexto == "*":
                    tipoToken = "SIGNO_MULTIPLICACION"
                elif datoTexto == "/":
                    tipoToken = "SIGNO_DIVISION"
                elif datoTexto == ".":
                    tipoToken = "PUNTO"
                elif datoTexto == "++":
                    tipoToken = "INCREMENTO"
                elif datoTexto == "--":
                    tipoToken = "DECREMENTO"
                elif datoTexto == "!":
                    tipoToken = "NOT"
                elif datoTexto == "~":
                    tipoToken = "COMPLEMENTO"
                elif datoTexto == "instanceof":
                    tipoToken = "INSTANCEOF"
                elif datoTexto == "<<":
                    tipoToken = "DESPLAZAMIENTO_IZQUIERDO"
                elif datoTexto == ">>":
                    tipoToken = "DESPLAZAMIENTO_DERECHO"
                elif datoTexto == ">>>":
                    tipoToken = "DESPLAZAMIENTO_DERECHO_SIN_SIGNO"
                elif datoTexto == "<<<":
                    tipoToken = "DESPLAZAMIENTO_IZQUIERDO_SIN_SIGNO"
                elif datoTexto == "<":
                    tipoToken = "MENOR_QUE"
                elif datoTexto == ">":
                    tipoToken = "MAYOR_QUE"
                elif datoTexto == ">=":
                    tipoToken = "MENOR_O_IGUAL_QUE"
                elif datoTexto == "<=":
                    tipoToken = "MAYOR_O_IGUAL_QUE"
                elif datoTexto == "==":
                    tipoToken = "IGUAL"
                elif datoTexto == "!=":
                    tipoToken = "NO_IGUAL"
                elif datoTexto == "&":
                    tipoToken = "AND_BIT_A_BIT"
                elif datoTexto == "^":
                    tipoToken = "XOR_BIT_A_BIT"
                elif datoTexto == "|":
                    tipoToken = "OR_BIT_A_BIT"
                elif datoTexto == "&&":
                    tipoToken = "AND_LOGICO"
                elif datoTexto == "||":
                    tipoToken = "OR_LOGICO"
                elif datoTexto == "?":
                    tipoToken = "OPERADOR_TERNARIO"
                elif datoTexto == ":":
                    tipoToken = "DOS_PUNTOS"
                elif datoTexto == "=":
                    tipoToken = "ASIGNACION"
                elif datoTexto == "op=":
                    tipoToken = "OPERADOR_ASIGNACION"
                elif datoTexto == ",":
                    tipoToken = "COMA"
                elif datoTexto == "[]":
                    tipoToken = "DOBLE_CORCHETE"
                else:
                    tipoToken = "ERROR"
                tokens.append((tipoToken, datoTexto, numeroLinea))
            elif datoTexto in delimitadores:
                tokens.append(("DELIMITADOR", datoTexto,numeroLinea))
            elif re.match(r'^[a-zA-Z_]\w*$', datoTexto):
                if datoTexto.lower() in palabrasReservadas:
                    raise ValueError(f"Palabra reservada mal escrita: '{datoTexto}' en la línea {numeroLinea}")
                #palabrasReservadas.add(datoTexto)
                tokens.append(("IDENTIFICADOR", datoTexto, numeroLinea))
            elif re.match(r"[0-9]+\.[0-9]+", datoTexto):
                if esDecimal(datoTexto):
                    tokens.append(("NUMERO_DECIMAL", datoTexto, numeroLinea))
                else:
                    raise ValueError(f"ERROR_DECIMAL: '{datoTexto}' en la línea {numeroLinea}")
            elif re.match(r"[0-9]+", datoTexto):
                
                tokens.append(("NUMERO_ENTERO", datoTexto, numeroLinea))
            elif re.match(r'^\d+\.\d+$', datoTexto):
                 
                 tokens.append(("Float Literal", datoTexto,numeroLinea))
            
            elif re.match(r'^[a-zA-Z_][a-zA-Z0-9$_]*$', datoTexto):  # Validación de literales
                if esLiteralValida(datoTexto):
                    
                    tokens.append(("LITERAL", datoTexto, numeroLinea))
                else:
                    raise ValueError(f"Literal inválido: '{datoTexto}' en la línea {numeroLinea}")
            else:
                raise ValueError(f"No se reconoce token: '{datoTexto}'")

            numeroLinea += 1

    return tokens #, identificadores, literales

nombre_archivo = "evaluadores.txt"
# ruta_archivo = "C:/Users/Wuux/Desktop/Compiladores"  # Coloca la ruta correcta aquí
ruta_archivo = "C:/Users/Rafael/OneDrive/Escritorio/EjercicioCompiExamen/CursoCompiladores"

ruta_completa = os.path.join(ruta_archivo, nombre_archivo)

if os.path.exists(ruta_completa):
    archivo = open(ruta_completa, "r", encoding="utf-8")
    textoArchivo = archivo.read()
    archivo.close()

    try:
        tokens = Analizador(textoArchivo)

        for tipoToken, valorToken, numeroLinea in tokens:
            print(f"{tipoToken:20} {valorToken:10} Linea: {numeroLinea}")


    except ValueError as e:
        print("Error:", e)
else:
    print("El archivo no existe.")