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


def calcular_estadisticas(ruta_archivo, indice_columna):
    # Tarea del Integrante 3
    pass

def funcionalidad_opcional(ruta_archivo):
    # Tarea del Integrante 4
    pass

# --- EL MENÚ INTERACTIVO ---

def mostrar_menu():
    print("="*50)
    print("  DATALAB: RETENCIÓN Y RENDIMIENTO ESTUDIANTIL")
    print("="*50)
    print("1. Buscar un término específico")
    print("2. Ver estadísticas básicas (Máx, Mín, Promedio)")
    print("3. Funcionalidad opcional (Filtro/Agrupación)")
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
            indice = int(input("Ingresa el número de la columna numérica: "))
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
