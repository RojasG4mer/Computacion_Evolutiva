import math
import random
import numpy as np

# ==========================================
# MÉTODOS ORIGINALES
# ==========================================
def ruleta(datos_poblacion, num_seleccionados):
    """
    Selección por Ruleta.
    La probabilidad de ser seleccionado es proporcional a la aptitud.
    """
    probabilidades = [d["probabilidad"] for d in datos_poblacion]
    indices = np.random.choice(len(datos_poblacion), size=num_seleccionados, p=probabilidades)
    return [datos_poblacion[i] for i in indices]

def torneo(datos_poblacion, num_seleccionados, k=3):
    """
    Selección por torneo estándar.
    Se escogen k individuos al azar y gana el de mejor aptitud.
    """
    seleccionados = []
    for _ in range(num_seleccionados):
        aspirantes = np.random.choice(datos_poblacion, size=k, replace=False)
        ganador = max(aspirantes, key=lambda x: x["aptitud"])
        seleccionados.append(ganador)
    return seleccionados


# ==========================================
# MÉTODOS AVANZADOS (DEL DOCUMENTO LATEX)
# ==========================================
def torneo_umbral(datos_poblacion, num_seleccionados, umbral=0.75):
    """
    Selección por torneo con umbral.
    Si r < umbral, gana el mejor de dos elegidos al azar; 
    de lo contrario, gana el peor.
    """
    seleccionados = []
    for _ in range(num_seleccionados):
        p1, p2 = random.sample(datos_poblacion, 2)
        r = random.random()
        
        if r < umbral:
            ganador = p1 if p1["aptitud"] > p2["aptitud"] else p2
        else:
            ganador = p1 if p1["aptitud"] < p2["aptitud"] else p2
            
        seleccionados.append(ganador)
    return seleccionados

def seleccion_rango(datos_poblacion, num_seleccionados, min_val=0.5, max_val=1.5):
    """
    Valor esperado = Min + (Max - Min) * (Rango - 1) / (N - 1).
    Evita la convergencia prematura al ignorar las aptitudes reales y usar 
    solo la posición del individuo en el ranking.
    """
    # Ordenamos de peor a mejor para asignar rangos (1 a N)
    poblacion_ordenada = sorted(datos_poblacion, key=lambda x: x["aptitud"])
    N = len(poblacion_ordenada)
    
    valores_esperados = []
    for i, ind in enumerate(poblacion_ordenada):
        rango = i + 1
        f_rango = min_val + (max_val - min_val) * ((rango - 1) / (N - 1)) if N > 1 else 1.0
        valores_esperados.append(f_rango)
        
    suma_rango = sum(valores_esperados)
    probabilidades = [ve / suma_rango for ve in valores_esperados]
    
    indices = np.random.choice(N, size=num_seleccionados, p=probabilidades)
    return [poblacion_ordenada[i] for i in indices]

def seleccion_boltzmann(datos_poblacion, num_seleccionados, temperatura=100.0):
    """
    Valor Esperado = e^(f_i / T) / Promedio_Poblacional.
    Conforme T decrece, la diferencia entre buenos y malos se magnifica.
    """
    N = len(datos_poblacion)
    
    # Encontramos la aptitud máxima para evitar un "Math Overflow Error" al calcular el exponencial
    max_apt = max(d["aptitud"] for d in datos_poblacion)
    
    # Calculamos los pesos restando el máximo para estabilidad numérica
    pesos_boltzmann = [math.exp((d["aptitud"] - max_apt) / temperatura) for d in datos_poblacion]
    promedio_b = sum(pesos_boltzmann) / N
    
    valores_esperados = [peso / promedio_b for peso in pesos_boltzmann]
    
    suma_ve = sum(valores_esperados)
    # Protegemos contra división por cero
    probabilidades = [ve / suma_ve if suma_ve > 0 else 1.0/N for ve in valores_esperados]
    
    indices = np.random.choice(N, size=num_seleccionados, p=probabilidades)
    return [datos_poblacion[i] for i in indices]

def muestreo_deterministico(datos_poblacion, num_seleccionados):
    """
    1. Calcular P_selecc = f_i / suma(f)
    2. Calcular poblacion esperada = n * P_selecc
    3. Asignar determinísticamente la parte entera.
    """
    suma_apt = sum(d["aptitud"] for d in datos_poblacion)
    esperados = []
    
    for d in datos_poblacion:
        p_selec = d["aptitud"] / suma_apt if suma_apt > 0 else 0
        v_e = num_seleccionados * p_selec
        esperados.append({"ind": d, "entero": int(v_e), "decimal": v_e - int(v_e)})

    seleccionados = []
    # Asignar parte entera
    for item in esperados:
        seleccionados.extend([item["ind"]] * item["entero"])

    # Ordenar por parte decimal (de mayor a menor)
    esperados.sort(key=lambda x: x["decimal"], reverse=True)

    # Obtener padres faltantes de la parte superior de la lista
    faltantes = num_seleccionados - len(seleccionados)
    for i in range(faltantes):
        seleccionados.append(esperados[i]["ind"])

    return seleccionados