# ==========================================
# PROYECTO DATALAB - ENTREGA 1 
# ==========================================

def cargar_y_buscar(ruta_archivo, termino_busqueda):
    # Tarea del Integrante 2
    pass 

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