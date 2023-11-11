import re

def validar_cadena(cadena):
    patron = re.compile(r'^\s*([a-zA-Z_]\w*)\s+([a-zA-Z_]\w*)\s*=\s*(.+?)\s*;\s*$')

    coincidencia = patron.match(cadena)

    if coincidencia:
        tipo, nombre, valor = coincidencia.groups()

        if tipo in ('int', 'double') and not re.match(r'^[+-]?\d+(\.\d+)?$', valor):
            raise ValueError(f'Error: El valor de {nombre} no es válido para el tipo {tipo}')

        if tipo == 'char' and not re.match(r'^".*"$', valor):
            raise ValueError(f'Error: El valor de {nombre} no es una cadena válida para el tipo {tipo}')

        return True
    else:
        raise ValueError('Error: La cadena no sigue el formato de declaración de variable')

try:

    cadena_usuario = input("Ingresa la cadena de declaración de variable: ")


    if validar_cadena(cadena_usuario):
        print(f'Valido: {cadena_usuario}')
except ValueError as e:
    print(e)