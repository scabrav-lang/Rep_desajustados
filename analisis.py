import csv
import json

def generar_resumen_json(ruta_archivo, ruta_salida="resumen.json"):
    total_registros = 0
    generos = set()
    estados_vivienda = set()
    estados_academicos = set()
    edad_maxima = -1
    edad_minima = 999
    
    try:
        with open(ruta_archivo, mode='r', encoding='utf-8') as archivo_csv:
            lector = csv.DictReader(archivo_csv) 
            
            for fila in lector:
                total_registros += 1
                
                # Extraer valores unicos 
                if 'Gender' in fila:
                    generos.add(fila['Gender'].strip())
                if 'Housing_Status' in fila:
                    estados_vivienda.add(fila['Housing_Status'].strip())
                if 'End_of_Semester_Status' in fila:
                    estados_academicos.add(fila['End_of_Semester_Status'].strip())
                    
                # Calcular maximos y minimos de edad
                if 'Age' in fila and fila['Age'].isdigit():
                    edad = int(fila['Age'])
                    if edad > edad_maxima:
                        edad_maxima = edad
                    if edad < edad_minima:
                        edad_minima = edad
                        
        # Diccionario con los resultados
        resumen = {
            "Total_Estudiantes": total_registros,
            "Edades": {
                "Minima": edad_minima if edad_minima != 999 else "N/A",
                "Maxima": edad_maxima if edad_maxima != -1 else "N/A"
            },
            "Categorias_Unicas": {
                "Generos": list(generos), 
                "Tipos_Vivienda": list(estados_vivienda),
                "Estados_Academicos": list(estados_academicos)
            }
        }
        
        # Guardar el archivo JSON
        with open(ruta_salida, mode='w', encoding='utf-8') as archivo_json:
            json.dump(resumen, archivo_json, indent=4)
            
        print(f"\n[Éxito] Archivo '{ruta_salida}' generado correctamente.")
        
    except FileNotFoundError:
        print(f"\nError: No se encontró el archivo '{ruta_archivo}'.")