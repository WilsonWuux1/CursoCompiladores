def validadorVariables(file_name):
    try:
        with open(file_name, 'r') as file:
            codigo = file.readlines()

            declaraciones = set()

            for linea in codigo:
                # Eliminar espacios en blanco y dividir la línea
                palabras = linea.strip().split()

                # Verificar si es una declaración 'int' y almacenar la variable
                if 'int' in palabras and len(palabras) >= 3 and palabras[1] not in declaraciones:
                    declaraciones.add(palabras[1])

                # Verificar si hay asignaciones y comprobar si la variable ha sido declarada
                elif '=' in palabras and palabras[0] not in declaraciones:
                    print(f"Error: '{palabras[0]}' sin declaración.")
                    return

            print("correcto.")

    except FileNotFoundError:
        print("El archivo no se encontró.")
    except Exception as e:
        print("Ocurrió un error:", e)

nameFile = input("ingrese ruta del archivo: ")
validadorVariables(nameFile)