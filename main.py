# ==========================================
# PROYECTO DATALAB - ENTREGA 2
# ==========================================
import Guardar_buscar
from Guardar_buscar import cargar_dataset
from archivos import registrar_historial, mostrar_historial
from resumen import generar_resumen


def cargar_y_buscar(ruta_archivo, termino_busqueda):
    coincidencias = 0
    encontradas = []
    termino_busqueda = termino_busqueda.lower().strip()

    # Cambio: ahora se carga con csv.reader (vía cargar_dataset)
    cabecera, filas = cargar_dataset(ruta_archivo)
    if not cabecera:
        return cabecera, encontradas

    print("\n--- Resultados de la Búsqueda ---")
    for valores in filas:
        coincidencia_en_linea = False
        for valor in valores:
            if termino_busqueda == valor.lower().strip():
                coincidencia_en_linea = True
                break

        if coincidencia_en_linea:
            coincidencias += 1
            encontradas.append(valores)
            detalles = []
            for i in range(len(cabecera)):
                val = valores[i] if i < len(valores) else ""
                detalles.append(f"{cabecera[i]}: {val}")
            print(f"[{coincidencias}] " + " | ".join(detalles))

    print("-" * 50)
    print(f"Total de coincidencias encontradas: {coincidencias}")
    print("-" * 50)
    return cabecera, encontradas


def obtener_encabezados(ruta_archivo):
    """Devuelve una lista con los nombres de las columnas del CSV."""
    return cargar_dataset(ruta_archivo)[0]


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
    maximo = None
    minimo = None
    suma = 0
    cantidad = 0

    # Cambio: se usa cargar_dataset en vez de abrir el archivo a mano
    encabezado, filas = cargar_dataset(ruta_archivo)

    for partes in filas:
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

    if cantidad == 0:
        print("Esa columna no tiene valores numéricos.")
        return None

    promedio = suma / cantidad
    print(f"Máximo: {maximo} · Mínimo: {minimo} · Promedio: {promedio:.2f}")
    return maximo, minimo, promedio


# =============================================
# FUNCIONALIDAD OPCIONAL: AGRUPAR POR CATEGORIA
# =============================================

def leer_archivo(ruta_archivo):
    """Devuelve el encabezado y las filas del CSV."""
    return cargar_dataset(ruta_archivo)


def contar_categorias(filas, indice):
    """Devuelve un diccionario con la cantidad de registros por categoría.
    Ejemplo: {"Enrolled": 42, "Dropped_Out": 8}"""
    conteo = {}
    for fila in filas:
        valor = fila[indice].strip() if indice < len(fila) else ""
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
    lista.sort(reverse=True)
    return lista


def funcionalidad_agrupar(ruta_archivo):
    """Pide una columna al usuario y muestra cuántos registros hay por categoría."""
    encabezado, filas = leer_archivo(ruta_archivo)
    if len(filas) == 0:
        return

    indice = pedir_columna(encabezado)
    if indice == -1:
        return

    conteo = contar_categorias(filas, indice)
    lista = ordenar_de_mayor_a_menor(conteo)
    total = len(filas)

    # Cambio: ahora esta consulta también queda en el historial
    registrar_historial(f"agrupar por {encabezado[indice]}", len(lista))

    print("\nRegistros por", encabezado[indice], "(de mayor a menor):")
    for cantidad, categoria in lista:
        porcentaje = cantidad * 100 / total
        print(f"  {categoria}: {cantidad} ({porcentaje:.1f}%)")

    print("\nCategorías distintas:", len(lista))
    filas_resumen = []
    for cantidad, categoria in lista:
        filas_resumen.append([categoria, cantidad])
    Guardar_buscar.ofrecer_guardar([encabezado[indice], "cantidad"], filas_resumen)


def funcionalidad_opcional(ruta_archivo):
    funcionalidad_agrupar(ruta_archivo)


# --- EL MENÚ INTERACTIVO ---

def mostrar_menu():
    print("=" * 50)
    print("  PERSEUS DATA: PLATAFORMA DE PREDICCIÓN DE DESERCIÓN")
    print("=" * 50)
    print("1. Buscar un término específico")
    print("2. Ver estadísticas básicas (Máx, Mín, Promedio)")
    print("3. Agrupar por Categoría")
    print("4. Recuperar resultados guardados")
    print("5. Ver Historial de Consultas")
    print("6. Salir")
    opcion = input("Elige una opción (1-6): ")
    return opcion


def main():
    archivo_actual = "estudiantes_50.csv"
    print(f"Iniciando sistema con el archivo: {archivo_actual}...")

    # Cambio: al iniciar se genera resultados/resumen.json (funcionalidad opcional)
    if generar_resumen(archivo_actual) is not None:
        print("Resumen del dataset guardado en resultados/resumen.json")

    while True:
        opcion = mostrar_menu()

        if opcion == '1':
            print("\nTip: Intenta buscar términos como 'Enrolled'...")
            termino = input("Ingresa el término a buscar: ")
            cabecera, encontradas = cargar_y_buscar(archivo_actual, termino)
            registrar_historial(termino, len(encontradas))
            Guardar_buscar.ofrecer_guardar(cabecera, encontradas)
        elif opcion == '2':
            encabezados = obtener_encabezados(archivo_actual)
            indice = pedir_columna(encabezados)
            if indice != -1:
                resultado = calcular_estadisticas(archivo_actual, indice)
                if resultado is not None:
                    # Cambio: también se registra en el historial
                    registrar_historial(f"estadísticas de {encabezados[indice]}", 1)
                    Guardar_buscar.ofrecer_guardar(
                        ["Columna", "Maximo", "Minimo", "Promedio"],
                        [[encabezados[indice], resultado[0], resultado[1], resultado[2]]])
        elif opcion == '3':
            print("Ejecutando funcionalidad opcional...")
            funcionalidad_opcional(archivo_actual)
        elif opcion == '4':
            Guardar_buscar.menu_recuperar()
        elif opcion == '5':
            mostrar_historial()
        elif opcion == '6':
            print("Saliendo del explorador. ¡Hasta pronto!")
            break
        else:
            print("Opción no válida. Ingresa un número del 1 al 6.")


# Cambio: sin esto el programa nunca arrancaba
if __name__ == "__main__":
    main()
