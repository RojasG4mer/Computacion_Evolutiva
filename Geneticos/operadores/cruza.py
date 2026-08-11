import random

def un_punto(in1, in2, n_bits):
    hijo1, hijo2 = in1.copy(), in2.copy()
    punto = random.randint(1, n_bits - 1)
    hijo1[punto:], hijo2[punto:] = hijo2[punto:], hijo1[punto:]
    return hijo1, hijo2

def uniforme(in1, in2, n_bits):
    # Un método nuevo que quieras experimentar
    hijo1, hijo2 = [], []
    for b1, b2 in zip(in1, in2):
        if random.random() < 0.5:
            hijo1.append(b1); hijo2.append(b2)
        else:
            hijo1.append(b2); hijo2.append(b1)
    return hijo1, hijo2

def n_puntos(in1, in2, n_bits, num_puntos=2):
    hijo1, hijo2 = in1.copy(), in2.copy()
    puntos = sorted(random.sample(range(1, n_bits), num_puntos))
    for i in range(len(puntos)):
        if i % 2 == 0:
            hijo1[puntos[i]:puntos[i + 1] if i + 1 < len(puntos) else None], hijo2[puntos[i]:puntos[i + 1] if i + 1 < len(puntos) else None] = hijo2[puntos[i]:puntos[i + 1] if i + 1 < len(puntos) else None], hijo1[puntos[i]:puntos[i + 1] if i + 1 < len(puntos) else None]
    return hijo1, hijo2    

def aritmetica(in1, in2, n_bits):
    hijo1 = [(b1 + b2) / 2 for b1, b2 in zip(in1, in2)]
    hijo2 = [(b1 + b2) / 2 for b1, b2 in zip(in1, in2)]
    return hijo1, hijo2

def geometrica(in1, in2, n_bits):
    hijo1 = [(b1 * b2) ** 0.5 for b1, b2 in zip(in1, in2)]
    hijo2 = [(b1 * b2) ** 0.5 for b1, b2 in zip(in1, in2)]
    return hijo1, hijo2

def diagonal(in1, in2, n_bits):
    hijo1 = [b1 if i % 2 == 0 else b2 for i, (b1, b2) in enumerate(zip(in1, in2))]
    hijo2 = [b2 if i % 2 == 0 else b1 for i, (b1, b2) in enumerate(zip(in1, in2))]
    return hijo1, hijo2
