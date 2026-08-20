import random
import math

def un_punto(in1, in2, n_bits):
    hijo1, hijo2 = in1.copy(), in2.copy()
    punto = random.randint(1, n_bits - 1)
    
    # Intercambiamos los segmentos a partir del punto de cruza
    hijo1[punto:], hijo2[punto:] = hijo2[punto:], hijo1[punto:]
    
    return hijo1, hijo2

def uniforme(in1, in2, n_bits):
    """
    Cruza uniforme estándar (Probabilidad p=0.5 fija).
    """
    hijo1, hijo2 = [], []
    for b1, b2 in zip(in1, in2):
        if random.random() < 0.5:
            hijo1.append(b1); hijo2.append(b2)
        else:
            hijo1.append(b2); hijo2.append(b1)
    return hijo1, hijo2

def cruza_n_puntos(in1, in2, n_bits, n_puntos=2):

    h1, h2 = in1.copy(), in2.copy()
    # Aseguramos no pedir más puntos de cruza que la longitud del cromosoma
    n_puntos = min(n_puntos, n_bits - 1)
    
    # Genera puntos de cruza aleatorios y ordenados
    puntos = sorted(random.sample(range(1, n_bits), n_puntos))
    puntos.append(n_bits)

    intercambiar = False
    idx_anterior = 0
    for punto in puntos:
        if intercambiar:
            h1[idx_anterior:punto], h2[idx_anterior:punto] = h2[idx_anterior:punto], h1[idx_anterior:punto]
        intercambiar = not intercambiar
        idx_anterior = punto
        
    return h1, h2

def cruza_uniforme_prob(in1, in2, n_bits, p=0.6):
    """
    Cruza uniforme donde el intercambio ocurre con probabilidad p.
    El documento sugiere 0.5 <= p <= 0.8.
    """
    h1, h2 = [], []
    for b1, b2 in zip(in1, in2):
        if random.random() < p:
            h1.append(b2); h2.append(b1)
        else:
            h1.append(b1); h2.append(b2)
    return h1, h2

# ==========================================
# CRUZA ENTRE VECTORES REALES
# (No se usan con cadenas binarias, solo con valores flotantes)
# ==========================================
def cruza_aritmetica_real(in1, in2, n_bits, alpha=0.3):
    """
    X'_1 = alpha * X_1i + (1 - alpha) * X_2i
    """
    h1 = [alpha * v1 + (1 - alpha) * v2 for v1, v2 in zip(in1, in2)]
    h2 = [(1 - alpha) * v1 + alpha * v2 for v1, v2 in zip(in1, in2)]
    return h1, h2

def cruza_geometrica_real(in1, in2, n_bits):
    """
    X'_i = (X_1i * X_2i)^0.5
    """
    h1 = [math.sqrt(abs(v1 * v2)) for v1, v2 in zip(in1, in2)]
    # Retorna dos copias iguales para mantener la simetría de 2 hijos por cruza
    return h1.copy(), h1.copy()