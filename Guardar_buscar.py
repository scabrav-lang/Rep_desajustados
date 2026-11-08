
import csv
import json


def cargar_dataset(ruta_archivo):
    #Lee el CSV con csv.reader y devuelve (encabezado, filas).
    try:
        with open(ruta_archivo, "r", encoding="utf-8", newline="") as archivo:
            lector = csv.reader(archivo)
            encabezado = next(lector)
            filas = []
            for fila in lector:
                if fila:                      
                    filas.append(fila)
            return encabezado, filas
    except FileNotFoundError:
        print(f"No se encontró el archivo: {ruta_archivo}")
    except StopIteration:
        print(f"El archivo '{ruta_archivo}' está vacío.")
    except UnicodeDecodeError:
        print(f"No se pudo leer '{ruta_archivo}': la codificación no es UTF-8.")
    except csv.Error as error:
        print(f"El archivo '{ruta_archivo}' no es un CSV válido: {error}")
    return [], []


#Guardar resultados

def guardar_csv(ruta, encabezado, filas): #Guarda un resultado en CSV. Devuelve True si salió bien, False si falló
    try:
        with open(ruta, "w", encoding="utf-8", newline="") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(encabezado)
            escritor.writerows(filas)
        return True
    except OSError as error:                  
        print(f"No se pudo guardar '{ruta}': {error}")
        return False


def guardar_json(ruta, encabezado, filas): #Guarda un resultado en JSON (lista de diccionarios). True si salió bien.
    registros = []
    for fila in filas:
        registro = {}
        for i in range(len(encabezado)):
            registro[encabezado[i]] = fila[i] if i < len(fila) else ""
        registros.append(registro)

    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(registros, archivo, ensure_ascii=False, indent=2)
        return True
    except OSError as error:
        print(f"No se pudo guardar '{ruta}': {error}")
        return False


def leer_indice(): #Devuelve la lista de nombres anotados en el índice (vacía si no existe).
    nombres = []
    try:
        with open(ARCHIVO_INDICE, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                nombre = linea.strip()
                if nombre != "":
                    nombres.append(nombre)
    except FileNotFoundError:
        pass                                  # aún no se ha guardado nada
    return nombres


def registrar_en_indice(nombre_archivo):  #Anota el archivo en el índice si todavía no estaba.
    if nombre_archivo in leer_indice():
        return
    try:
        with open(ARCHIVO_INDICE, "a", encoding="utf-8") as archivo:
            archivo.write(nombre_archivo + "\n")
    except OSError as error:
        print(f"No se pudo actualizar el índice: {error}")


def guardar_resultado(nombre, formato, encabezado, filas):
    if formato != "json":
        formato = "csv"
    nombre_archivo = f"{nombre}.{formato}"

    if formato == "json":
        exito = guardar_json(nombre_archivo, encabezado, filas)
    else:
        exito = guardar_csv(nombre_archivo, encabezado, filas)

    if not exito:
        return None
    registrar_en_indice(nombre_archivo)
    return nombre_archivo


# Para recuperar resultados 

def cargar_csv(ruta): #Lee un resultado guardado en CSV. Devuelve (encabezado, filas).
    return cargar_dataset(ruta)

def cargar_json(ruta): #Lee un resultado guardado en JSON y lo devuelve como (encabezado, filas).
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            registros = json.load(archivo)

        if len(registros) == 0:
            return [], []

        encabezado = list(registros[0].keys())
        filas = []
        for registro in registros:
            fila = []
            for columna in encabezado:
                fila.append(registro[columna])
            filas.append(fila)
        return encabezado, filas

    except FileNotFoundError:
        print(f"No se encontró el archivo: {ruta}")
    except json.JSONDecodeError:
        print(f"'{ruta}' no es un JSON válido (¿se editó a mano?).")
    except (KeyError, AttributeError, TypeError):
        print(f"'{ruta}' no tiene la estructura esperada (lista de registros).")
    return [], []


def listar_resultados_guardados(): #Devuelve los resultados del índice que todavía existen en disco.
    existentes = []
    for nombre in leer_indice():
        try:
            archivo = open(nombre, "r", encoding="utf-8")
            archivo.close()
            existentes.append(nombre)
        except FileNotFoundError:
            continue                          # el archivo fue borrado a mano
    return sorted(existentes)


def recuperar_resultado(nombre_archivo):
    """Carga un resultado guardado, sin importar si es CSV o JSON."""
    if nombre_archivo.endswith(".json"):
        return cargar_json(nombre_archivo)
    return cargar_csv(nombre_archivo)


# Interacción (para que main solo las llame) 

def ofrecer_guardar(encabezado, filas): #Después de una consulta, pregunta si se quiere guardar el resultado.
    if len(filas) == 0:
        return

    respuesta = input("¿Deseas guardar estos resultados? (s/n): ").lower().strip()
    if respuesta != "s":
        return

    nombre = input("Nombre del archivo (sin extensión): ").strip()
    if nombre == "":
        print("Nombre vacío, no se guardó.")
        return

    formato = input("Formato (csv/json): ").lower().strip()
    if formato not in ("csv", "json"):
        print("Formato no reconocido, se usará csv.")
        formato = "csv"

    ruta = guardar_resultado(nombre, formato, encabezado, filas)
    if ruta is not None:
        print(f"Guardado en {ruta}")


def menu_recuperar(): #Muestra resultados guardados, deja elegir uno y lo imprime.
    guardados = listar_resultados_guardados()
    if len(guardados) == 0:
        print("No hay resultados guardados todavía.")
        return

    print("\nResultados guardados:")
    for i in range(len(guardados)):
        print(f"  {i + 1}. {guardados[i]}")

    eleccion = input("Número del archivo a cargar: ").strip()
    if not eleccion.isdigit() or not (1 <= int(eleccion) <= len(guardados)):
        print("Opción no válida.")
        return

    encabezado, filas = recuperar_resultado(guardados[int(eleccion) - 1])
    for fila in filas:
        detalles = []
        for i in range(len(encabezado)):
            detalles.append(f"{encabezado[i]}: {fila[i]}")
        print(" | ".join(detalles))
    print(f"Total: {len(filas)} registros")
