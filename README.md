# Perseus Data: Plataforma de Predicción de Deserción Universitaria

## Descripción del Proyecto
Este proyecto analiza factores socioeconómicos y académicos que inciden en el rendimiento escolar y la tasa de retención estudiantil universitaria. En esta **Segunda Entrega ("Analizador")**, el sistema evoluciona hacia una arquitectura modular en Python con persistencia de datos (CSV y JSON), auditoría automática de consultas y estructuras de datos nativas (listas, diccionarios y conjuntos), sin depender de librerías externas como Pandas.

## Integrantes
- Danna Villamizar
- Diego Sabogal
- Julián Hernández
- Sara Fontecha
- Sofía Cabra

## Preguntas de Investigación
1. ¿Cuál es la relación entre las horas trabajadas a la semana y el promedio académico del estudiante?
2. ¿Cómo influye el estrés financiero en la deserción universitaria durante los primeros semestres?
3. ¿Existe una diferencia en el rendimiento académico entre estudiantes de primera generación universitaria y los demás?

## Estructura Modular del Repositorio
El código se encuentra dividido en módulos especializados según su responsabilidad:

- `main.py`: Orquestador principal. Contiene el menú interactivo en consola, la lógica de búsqueda, cálculo de estadísticas descriptivas, agrupación por categorías y la generación inicial del resumen del dataset.
- `archivos.py`: Módulo encargado de la persistencia de auditoría y resumen. Gestiona el registro automático del historial con marcas de tiempo (`historial.csv`) y el almacenamiento del resumen estadístico (`resultados/resumen.json`).
- `Guardar_buscar.py`: Módulo de lectura de datasets (`csv.reader`) y persistencia de consultas bajo demanda. Permite exportar resultados en formatos `.csv` o `.json`, indexarlos en `indice_resultados.txt` y recuperarlos posteriormente desde el menú.
- `analisis.py`: Módulo auxiliar de análisis de datos sobre diccionarios (`csv.DictReader`) para extracción de categorías únicas mediante conjuntos (`set`).
- `estudiantes_completos.csv`: Dataset principal de análisis (más de 200 registros) cargado por defecto al iniciar el sistema.

### Archivos generados automáticamente durante la ejecución:
- `resultados/resumen.json`: Resumen general del dataset generado al arrancar el programa (total de registros, valores máximos/mínimos y conteo de categorías únicas).
- `historial.csv`: Registro silencioso y cronológico de todas las búsquedas y consultas realizadas en el sistema.
- `indice_resultados.txt` y archivos `.csv`/`.json`: Resultados específicos exportados por el usuario.

## Requisitos Técnicos
- **Python 3.x**
- **Librerías nativas utilizadas:** `csv`, `json`, `datetime`, `os` *(No requiere instalación de paquetes externos)*.

## Instrucciones de Ejecución
1. Asegúrate de tener instalado **Python 3.x**.
2. Clona o descarga este repositorio en tu equipo:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd <NOMBRE_DE_LA_CARPETA>
