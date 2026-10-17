# ==========================================
# PROYECTO DATALAB - ENTREGA 1 
# ==========================================

def cargar_y_buscar(ruta_archivo, termino_busqueda):
    coincidencias = 0
    termino_busqueda = termino_busqueda.lower().strip()
    
    try:
        with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
            # Leer la primera línea (cabecera) para tener los nombres de las columnas
            cabecera = archivo.readline().strip().split(',')
            
            print("\n--- Resultados de la Búsqueda ---")
            for linea in archivo:
                linea = linea.strip()
                if not linea:
                    continue
                
                valores = linea.split(',')
    
                coincidencia_en_linea = False
                for valor in valores:
                    if termino_busqueda in valor.lower():
                        coincidencia_en_linea = True
                        break
                
                if coincidencia_en_linea:
                    coincidencias += 1
                    detalles = []
                    for i in range(len(cabecera)):
                        val = valores[i] if i < len(valores) else ""
                        detalles.append(f"{cabecera[i]}: {val}")
                    print(f"[{coincidencias}] " + " | ".join(detalles))
            
            print("-"*50)
            print(f"Total de coincidencias encontradas: {coincidencias}")
            print("-"*50)
            
    except FileNotFoundError:
        print(f"Error: El archivo '{ruta_archivo}' no existe. Asegúrate de que el Integrante 1 lo haya creado.")


def obtener_encabezados(ruta_archivo):
    """Devuelve una lista con los nombres de las columnas del CSV."""
    archivo = open(ruta_archivo, "r")
    primera_linea = archivo.readline()
    archivo.close()
    return primera_linea.strip().split(",")


def es_numero(texto):
    """Devuelve True si el texto es un número como 12, -3 o 2.85."""
    if texto.startswith("-"):
        texto = texto[1:]
    partes = texto.split(".")
    if len(partes) > 2:
        return False
    for parte in partes:
        if not parte.isdigit():
            return False
    return True


def buscar_indice_columna(encabezados, nombre):
    """Devuelve la posición de la columna con ese nombre, o -1 si no existe.
    No distingue mayúsculas de minúsculas."""
    nombre = nombre.strip().lower()
    for i in range(len(encabezados)):
        if encabezados[i].lower() == nombre:
            return i
    return -1


def pedir_columna(encabezados):
    """Muestra las columnas, pide un nombre y devuelve su índice (o -1)."""
    print("\nColumnas disponibles:")
    for nombre in encabezados:
        print(f"  - {nombre}")

    nombre = input("\nEscribe el nombre de la columna: ")
    indice = buscar_indice_columna(encabezados, nombre)
    if indice == -1:
        print("Esa columna no existe. Escríbela como aparece en la lista.")
    return indice


def calcular_estadisticas(ruta_archivo, indice_columna):
    """Calcula e imprime máximo, mínimo y promedio de una columna numérica."""
    maximo = None      # variable acumuladora: el mayor valor visto
    minimo = None      # variable acumuladora: el menor valor visto
    suma = 0           # variable acumu ladora: suma de todos los valores
    cantidad = 0       # variable acumuladora: cuántos valores hay

    archivo = open(ruta_archivo, "r")
    archivo.readline()  # saltar el encabezado

    for linea in archivo:  # bucle: recorre el archivo fila por fila
        partes = linea.strip().split(",")
        if indice_columna >= len(partes):
            continue
        texto = partes[indice_columna]
        if not es_numero(texto):
            continue  # saltar celdas vacías o con texto

        valor = float(texto)
        if maximo is None or valor > maximo:
            maximo = valor
        if minimo is None or valor < minimo:
            minimo = valor
        suma = suma + valor
        cantidad = cantidad + 1

    archivo.close()

    if cantidad == 0:
        print("Esa columna no tiene valores numéricos.")
    else:
        promedio = suma / cantidad
        print(f"Máximo: {maximo} · Mínimo: {minimo} · Promedio: {promedio:.2f}")
        return maximo, minimo, promedio
    # Tarea del Integrante 3
    

# =============================================
# FUNCIONALIDAD OPCIONAL: AGRUPAR POR CATEGORIA 
# =============================================

def leer_archivo(ruta_archivo):
    """Lee el CSV y devuelve el encabezado y las filas."""
    try:
        archivo = open(ruta_archivo, "r", encoding="utf-8")
    except FileNotFoundError:
        print("No se encontró el archivo:", ruta_archivo)
        return [], []

    lineas = archivo.readlines()   # lista con todas las líneas del archivo
    archivo.close()

    # La primera línea son los nombres de las columnas
    encabezado = lineas[0].strip().split(",")

    # El resto de las líneas son los registros
    filas = []
    for linea in lineas[1:]:
        linea = linea.strip()
        if linea != "":
            filas.append(linea.split(","))

    return encabezado, filas


def contar_categorias(filas, indice):
    """Devuelve un diccionario con la cantidad de registros por categoría.
    Ejemplo: {"Enrolled": 42, "Dropped_Out": 8}"""
    conteo = {}
    for fila in filas:
        valor = fila[indice].strip()
        if valor == "":
            valor = "(vacío)"

        if valor in conteo:
            conteo[valor] = conteo[valor] + 1
        else:
            conteo[valor] = 1
    return conteo


def ordenar_de_mayor_a_menor(conteo):
    """Convierte el diccionario en una lista ordenada de (cantidad, categoría)."""
    lista = []
    for categoria in conteo:
        lista.append((conteo[categoria], categoria))
    lista.sort(reverse=True)   # de mayor a menor cantidad
    return lista


def funcionalidad_agrupar(ruta_archivo):
    """Pide una columna al usuario y muestra cuántos registros hay por categoría."""
    encabezado, filas = leer_archivo(ruta_archivo)
    if len(filas) == 0:
        return

    # Reutiliza pedir_columna (la misma que usa la opción 2): pide el NOMBRE de la columna
    indice = pedir_columna(encabezado)
    if indice == -1:
        return

    # Contar, ordenar e imprimir
    conteo = contar_categorias(filas, indice)
    lista = ordenar_de_mayor_a_menor(conteo)
    total = len(filas)

    print("\nRegistros por", encabezado[indice], "(de mayor a menor):")
    for cantidad, categoria in lista:
        porcentaje = cantidad * 100 / total
        print(f"  {categoria}: {cantidad} ({porcentaje:.1f}%)")

    print("\nCategorías distintas:", len(lista))


def funcionalidad_opcional(ruta_archivo):
    funcionalidad_agrupar(ruta_archivo)


# --- EL MENÚ INTERACTIVO ---

def mostrar_menu():
    print("="*50)
    print("  DATALAB: RETENCIÓN Y RENDIMIENTO ESTUDIANTIL")
    print("="*50)
    print("1. Buscar un término específico")
    print("2. Ver estadísticas básicas (Máx, Mín, Promedio)")
    print("3. Agrupar por Categoría")
    print("4. Salir")
    opcion = input("Elige una opción (1-4): ")
    return opcion

def main():
    archivo_actual = "estudiantes_50.csv"
    print(f"Iniciando sistema con el archivo: {archivo_actual}...")
    
    while True:
        opcion = mostrar_menu()
        
        if opcion == '1':
            termino = input("Ingresa el término a buscar: ")
            cargar_y_buscar(archivo_actual, termino)
        elif opcion == '2':
            encabezados = obtener_encabezados(archivo_actual)
            indice = pedir_columna(encabezados)
            if indice != -1:
                calcular_estadisticas(archivo_actual, indice)
        elif opcion == '3':
            print("Ejecutando funcionalidad opcional...")
            funcionalidad_opcional(archivo_actual)
        elif opcion == '4':
            print("Saliendo del explorador. ¡Hasta pronto!")
            break
        else:
            print("Opción no válida. Ingresa un número del 1 al 4.")

if __name__ == "__main__":
    main()

