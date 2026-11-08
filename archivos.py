
import csv
import json
import os

CARPETA_RESULTADOS = "resultados"  

def cargar_dataset(ruta_archivo):
    """Lee el dataset con csv.reader y devuelve (encabezado, filas)."""
    try:
        archivo = open(ruta_archivo, "r", encoding="utf-8", newline="")
    except FileNotFoundError:
        print("No se encontró el archivo:", ruta_archivo)
        return [], []

    lector = csv.reader(archivo)
    todas = list(lector)     
    archivo.close()

    if len(todas) == 0:
        print("El archivo está vacío.")
        return [], []

    encabezado = todas[0]
    filas = todas[1:]
    return encabezado, filas

def limpiar_nombre(texto):
    """Deja solo letras, números, guion y guion bajo (los espacios pasan a _)."""
    texto = texto.strip().replace(" ", "_")
    limpio = ""
    for caracter in texto:
        if caracter.isalnum() or caracter == "_" or caracter == "-":
            limpio = limpio + caracter
    return limpio


def preparar_carpeta():
    """Crea la carpeta de resultados si no existe."""
    if not os.path.exists(CARPETA_RESULTADOS):
        os.makedirs(CARPETA_RESULTADOS)


def guardar_csv(nombre, encabezado, filas):
    """Guarda una tabla (encabezado + filas) en resultados/<nombre>.csv.
    Devuelve la ruta del archivo creado."""
    preparar_carpeta()
    ruta = os.path.join(CARPETA_RESULTADOS, nombre + ".csv")
    archivo = open(ruta, "w", encoding="utf-8", newline="")
    escritor = csv.writer(archivo)
    escritor.writerow(encabezado)
    escritor.writerows(filas)
    archivo.close()
    return ruta


def guardar_json(nombre, datos):
    """Guarda un diccionario (o lista) en resultados/<nombre>.json.
    Devuelve la ruta del archivo creado."""
    preparar_carpeta()
    ruta = os.path.join(CARPETA_RESULTADOS, nombre + ".json")
    archivo = open(ruta, "w", encoding="utf-8")
    json.dump(datos, archivo, indent=4, ensure_ascii=False)
    archivo.close()
    return ruta

def listar_guardados():
    """Devuelve la lista de archivos .csv y .json guardados (vacía si no hay)."""
    if not os.path.exists(CARPETA_RESULTADOS):
        return []
    guardados = []
    for nombre in os.listdir(CARPETA_RESULTADOS):
        if nombre.endswith(".csv") or nombre.endswith(".json"):
            guardados.append(nombre)
    guardados.sort()
    return guardados


def cargar_csv_guardado(nombre_archivo):
    """Lee un CSV guardado y devuelve (encabezado, filas)."""
    ruta = os.path.join(CARPETA_RESULTADOS, nombre_archivo)
    archivo = open(ruta, "r", encoding="utf-8", newline="")
    todas = list(csv.reader(archivo))
    archivo.close()
    if len(todas) == 0:
        return [], []
    return todas[0], todas[1:]


def cargar_json_guardado(nombre_archivo):
    """Lee un JSON guardado y devuelve su contenido (diccionario o lista)."""
    ruta = os.path.join(CARPETA_RESULTADOS, nombre_archivo)
    archivo = open(ruta, "r", encoding="utf-8")
    datos = json.load(archivo)
    archivo.close()
    return datos


def ruta_resultado(nombre_archivo):
    """Ejemplo: ruta_resultado("resumen.json") -> "resultados/resumen.json"."""
    return os.path.join(CARPETA_RESULTADOS, nombre_archivo)

def formatear_json(datos):
    """Devuelve el contenido en texto con sangría, listo para imprimir."""
    return json.dumps(datos, indent=4, ensure_ascii=False)
