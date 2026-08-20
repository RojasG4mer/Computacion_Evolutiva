import random

# ==========================================
# MÉTODOS ORIGINALES
# ==========================================
def mutacion_un_bit(individuo):
    """
    Selecciona un bit al azar y lo invierte (de 0 a 1, o de 1 a 0).
    Esta es la función original.
    """
    posicion = random.randrange(len(individuo))
    individuo[posicion] = 1 - individuo[posicion]
    return individuo

def mutacion_multiple(individuo, probabilidad_por_bit=0.1):
    """
    Método alternativo: En lugar de mutar un solo bit forzosamente,
    recorre toda la cadena y cada bit tiene una pequeña probabilidad de mutar.
    Ideal para mantener mayor diversidad genética.
    """
    for i in range(len(individuo)):
        if random.random() < probabilidad_por_bit:
            individuo[i] = 1 - individuo[i]
    return individuo

# ==========================================
# MÉTODOS AVANZADOS
# ==========================================
def mutacion_intercambio(individuo):
    """
    Mutación Swap (Intercambio): Elige dos posiciones distintas al azar 
    y permuta sus valores. 
    """
    idx1, idx2 = random.sample(range(len(individuo)), 2)
    individuo[idx1], individuo[idx2] = individuo[idx2], individuo[idx1]
    return individuo

def mutacion_inversion_secuencia(individuo):
    """
    Mutación por Inversión: Selecciona un subconjunto de la cadena 
    y voltea su orden por completo.
    Ejemplo: [1, (0, 1, 1), 0] -> [1, (1, 1, 0), 0]
    """
    n = len(individuo)
    if n < 2: return individuo
    
    # Escogemos dos puntos de corte
    punto1, punto2 = sorted(random.sample(range(n + 1), 2))
    
    # Invertimos la sublista
    individuo[punto1:punto2] = reversed(individuo[punto1:punto2])
    return individuo

def mutacion_gaussiana(individuo, media=0.0, desviacion=0.1):
    """
    Mutación ideal si estás usando codificación real (no binaria).
    En lugar de invertir un bit, le suma "ruido" basado en una 
    campana de Gauss a un alelo seleccionado.
    """
    posicion = random.randrange(len(individuo))
    ruido = random.gauss(media, desviacion)
    individuo[posicion] += ruido
    return individuo