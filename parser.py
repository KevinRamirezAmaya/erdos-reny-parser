import os
import numpy as np
from scipy.spatial import distance
import matplotlib.pyplot as plt
import time

def leer_tsp_local(ruta_archivo):
    print(f"\n[1/3] Leyendo archivo local: {ruta_archivo}...")
    coordenadas_x, coordenadas_y = [], []
    leyendo_nodos = False
    
    try:
        with open(ruta_archivo, 'r') as archivo:
            for linea in archivo:
                linea = linea.strip()
                if not linea: continue
                if linea == "EOF": break
                if linea == "NODE_COORD_SECTION":
                    leyendo_nodos = True
                    continue
                
                if leyendo_nodos:
                    partes = linea.split()
                    if len(partes) >= 3:
                        coordenadas_x.append(float(partes[1]))
                        coordenadas_y.append(float(partes[2]))
                        
        print(f"       Se leyeron {len(coordenadas_x)} ciudades correctamente.")
        return coordenadas_x, coordenadas_y
        
    except FileNotFoundError:
        print(f"\n ERROR: No se encontró el archivo '{ruta_archivo}'.")
        return None, None

def calcular_matriz_optimizada(x, y):
    """Calcula la matriz NxN usando vectorización subyacente en C (SciPy)."""
    print("[2/3] Calculando matriz de distancias vectorizada...")
    inicio = time.time()
    
    # Unir X y Y en una matriz de N filas y 2 columnas
    coordenadas = np.column_stack((x, y))
    
    # cdist calcula TODA la matriz euclidiana de golpe
    matriz = distance.cdist(coordenadas, coordenadas, 'euclidean')
    
    # Redondear a enteros según estándar TSPLIB
    matriz = np.round(matriz).astype(np.int32) 
    
    fin = time.time()
    print(f"      ✓ Matriz de {len(x)}x{len(x)} generada en {fin - inicio:.4f} segundos.")
    return matriz

def guardar_matriz_binaria(matriz, ruta_base):
    """Guarda la matriz en un formato binario .npy ultraligero."""
    print(f"[3/3] Exportando datos para el Algoritmo Evolutivo...")
    ruta_salida = f"{ruta_base}.npy"
    np.save(ruta_salida, matriz)
    print(f"      ✓ Archivo binario guardado en: {ruta_salida}")


carpeta_datos = "data" 

print("="*50)
print(" PREPROCESADOR OPTIMIZADO TSPLIB ")
print("="*50)

if not os.path.exists(carpeta_datos):
    print(f" La carpeta '{carpeta_datos}' no existe. Por favor, créala.")
else:
    archivos_disponibles = [f for f in os.listdir(carpeta_datos) if f.endswith('.tsp')]
    
    if not archivos_disponibles:
        print(" No hay archivos .tsp en la carpeta 'data'.")
    else:
        print("Archivos disponibles:")
        for file in archivos_disponibles:
            print(f"  - {file}")
            
        nombre_archivo = input("\nIntroduce el nombre del archivo (ej. berlin52.tsp): ").strip()
        ruta_completa = os.path.join(carpeta_datos, nombre_archivo)

        x, y = leer_tsp_local(ruta_completa)

        if x and y:
            matriz_distancias = calcular_matriz_optimizada(x, y)
            
            ruta_base_salida = os.path.join(carpeta_datos, f"matriz_{nombre_archivo.replace('.tsp', '')}")
            guardar_matriz_binaria(matriz_distancias, ruta_base_salida)
            
            print("\nGenerando visualización espacial...")
            plt.figure(figsize=(8, 6))
            plt.scatter(x, y, c='darkblue', marker='o', s=60, alpha=0.7, label='Nodos (Ciudades)')

            if len(x) <= 100:
                for i in range(len(x)):
                    plt.text(x[i] + 1, y[i] + 1, str(i+1), fontsize=8)

            plt.title(f'Espacio de Búsqueda TSPLIB: {nombre_archivo}', fontsize=14, fontweight='bold')
            plt.xlabel('Eje X')
            plt.ylabel('Eje Y')
            plt.grid(True, linestyle='--', alpha=0.4)
            plt.legend()
            
            nombre_imagen = f"plot_{nombre_archivo.replace('.tsp', '.png')}"
            plt.savefig(nombre_imagen, dpi=300, bbox_inches='tight')
            print(f"       Gráfica guardada como '{nombre_imagen}'")
            
            print("\n ¡PROCESO COMPLETADO CON ÉXITO! ")
            print("Revisa tu carpeta, ya tienes los inputs optimizados listos para el paper.")
            
            plt.show()