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