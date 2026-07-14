import random

def mutacion_un_bit(individuo):
    """
    Selecciona un bit al azar y lo invierte (de 0 a 1, o de 1 a 0).
    Esta es la función original.
    """
    posicion = random.randrange(len(individuo)) #[cite: 1]
    individuo[posicion] = 1 - individuo[posicion] #[cite: 1]
    return individuo #[cite: 1]

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