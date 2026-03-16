import os
import math
import matplotlib.pyplot as plt

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
                        
        print(f"      ✓ Se leyeron {len(coordenadas_x)} ciudades correctamente.")
        return coordenadas_x, coordenadas_y
        
    except FileNotFoundError:
        print(f"\n ERROR: No se encontró el archivo '{ruta_archivo}'.")
        return None, None

def calcular_matriz_distancias(x, y):
    """Calcula la matriz de distancias euclidianas entre todos los nodos."""
    print("[2/3] Calculando matriz de distancias NxN...")
    n = len(x)
    matriz = [[0.0 for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            if i != j:
                distancia = math.sqrt((x[i] - x[j])**2 + (y[i] - y[j])**2)
                matriz[i][j] = round(distancia) # El estándar TSPLIB usa enteros
    
    print(f"      ✓ Matriz de {n}x{n} generada.")
    return matriz

def guardar_matriz_txt(matriz, ruta_salida):
    """Guarda la matriz en un archivo de texto de forma legible."""
    print(f"[3/3] Exportando datos para el Algoritmo Evolutivo...")
    with open(ruta_salida, 'w') as archivo:
        archivo.write(f"{len(matriz)}\n")
        
        for fila in matriz:
            linea_str = "\t".join(str(int(valor)) for valor in fila)
            archivo.write(linea_str + "\n")
            
    print(f"      ✓ Archivo de texto guardado en: {ruta_salida}")


carpeta_datos = "data" 

print("="*50)
print(" PREPROCESADOR DE INSTANCIAS TSPLIB ")
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
            matriz_distancias = calcular_matriz_distancias(x, y)
            
            nombre_txt = f"matriz_{nombre_archivo.replace('.tsp', '.txt')}"
            guardar_matriz_txt(matriz_distancias, nombre_txt)
            
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
            print(f"      ✓ Gráfica guardada como '{nombre_imagen}'")
            
            print("\n ¡PROCESO COMPLETADO CON ÉXITO! ")
            print("Revisa tu carpeta, ya tienes los inputs listos para el paper.")
            
            plt.show()