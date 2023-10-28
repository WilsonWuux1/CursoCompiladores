import re

def validar_cadena(cadena):
    
    patron = re.compile(r'^\s*([a-zA-Z_]\w*)\s+([a-zA-Z_]\w*)\s*=\s*(.+?)\s*;\s*$')


    coincidencia = patron.match(cadena)

    if coincidencia:
        tipo, nombre, valor = coincidencia.groups()

        if tipo in ('int', 'double') and not re.match(r'^[+-]?\d+(\.\d+)?$', valor):
            return False

        if tipo == 'char' and not re.match(r'^".*"$', valor):
            return False

        return True
    else:
        return False


cadena = input("Ingresa la cadena de declaración de variable ")

if validar_cadena(cadena):
    print(f'Valido: {cadena}')
else:
    print(f'No Valido: {cadena}')

