import math
import numpy as np
import random

# Definimos una lista de ciudades con coordenadas (x, y)
ciudades = {
    'A': (0, 0),
    'B': (20, 4),
    'C': (58, 2),
    'D': (7, 6),
    'E': (8, 1), 
    'F': (45, 89),
    'G': (12, 34),
    'H': (23, 45),
    'I': (56, 78),
    'J': (90, 12)
}

def calcular_distancia(coord1, coord2):
    """
    Calcula la distancia Euclidiana entre dos puntos.
    """
    x1, y1 = coord1
    x2, y2 = coord2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


Ciudades_letras = list(ciudades.keys())
print(Ciudades_letras)

ciudad_inicial = 'A'  # Ciudad de inicio
individuos = 10

# Crear las combinaciones de inicio
# Generar individuos aleatorios
poblacion_inicial = []

for i in range(individuos):
    # Crear una lista de ciudades excluyendo la ciudad inicial
    otras_ciudades = [c for c in Ciudades_letras if c != ciudad_inicial]
    
    # Mezclar aleatoriamente las otras ciudades
    random.shuffle(otras_ciudades)
    
    # Crear el individuo agregando la ciudad inicial al principio y al final
    individuo = [ciudad_inicial] + otras_ciudades + [ciudad_inicial]
    
    poblacion_inicial.append(individuo)

# print("Población inicial:")
# for ind in poblacion_inicial:
#     print(ind)


# ==========================================
# Calcular la distancia total de cada individuo
# ==========================================






