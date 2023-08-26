import os
import re

def is_valid_decimal(token):    
    parts = token.split('.')
    return len(parts) == 2 and all(part.isdigit() for part in parts)

def tokenize(input_str):
    tokens = []
    pattern = r"([0-9]+\.[0-9]+|[0-9]+|\+|\-|\*|\/|\(|\))"
    matches = re.finditer(pattern, input_str)

    lines = input_str.split('\n')
    line_number = 1

    for line in lines:
        for match in re.finditer(pattern, line):
            token = match.group()
            if re.match(r"[0-9]+\.[0-9]+", token):
                if is_valid_decimal(token):
                    tokens.append(("NUMERO_DECIMAL", token, line_number))
                else:
                    tokens.append(("ERROR_DECIMAL", token, line_number))
            elif re.match(r"[0-9]+", token):
                tokens.append(("NUMERO_ENTERO", token, line_number))
            elif token in "+-*/":
                if token == "+":
                    token_type = "SIGNO_MAS"
                elif token == "-":
                    token_type = "SIGNO_MENOS"
                elif token == "*":
                    token_type = "SIGNO_MULTIPLICACION"
                elif token == "/":
                    token_type = "SIGNO_DIVISION"
                else:
                    token_type = "ERROR"
                tokens.append((token_type, token, line_number))
            elif token == "(":
                tokens.append(("PARENTESIS_IZQ", token, line_number))
            elif token == ")":
                tokens.append(("PARENTESIS_DER", token, line_number))
            else:
                tokens.append(("ERROR", token, line_number))
        line_number += 1

    return tokens

# Resto del código

nombre_archivo = "numeros.txt"  # Nombre del archivo
ruta_archivo = "C:/Users/Rafael/OneDrive/Escritorio/EjercicioCompiExamen/CursoCompiladores"
# ruta_archivo = "C:/Users/Wuux/Desktop/Compiladores"  # Ruta del archivo
ruta_completa = os.path.join(ruta_archivo, nombre_archivo)  # Combina la ruta y el nombre del archivo

if os.path.exists(ruta_completa):
    archivo = open(ruta_completa, "r", encoding="utf-8")  # Abre el archivo en modo lectura
    contenido = archivo.read()  # Lee el contenido del archivo
    archivo.close()  # Cierra el archivo

    tokens = tokenize(contenido)  # Tokeniza el contenido del archivo
    for token_type, token_value, line_number in tokens:
        print(f"{token_type:20} {token_value:10} Linea: {line_number}")

else:
    archivo = open(ruta_completa, "w")  # Crea el archivo si no existe
    archivo.write("Curso de compiladores.\n")  # Escribe contenido en el archivo
    archivo.close()  # Cierra el archivo
