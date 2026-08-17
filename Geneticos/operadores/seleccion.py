# Agregar esto al final de operadores/seleccion.py
import math
import random
import numpy as np

def torneo_umbral(datos_poblacion, num_seleccionados, umbral=0.75):
    """
    Selección por torneo con umbral.
    Si r < umbral, gana el mejor; de lo contrario, gana el peor[cite: 1].
    """
    seleccionados = []
    for _ in range(num_seleccionados):
        # Escogen 2 aleatoriamente[cite: 1]
        p1, p2 = random.sample(datos_poblacion, 2)
        r = random.random() #[cite: 1]
        
        if r < umbral: #[cite: 1]
            ganador = p1 if p1["aptitud"] > p2["aptitud"] else p2
        else:
            ganador = p1 if p1["aptitud"] < p2["aptitud"] else p2 #[cite: 1]
            
        seleccionados.append(ganador)
    return seleccionados

def seleccion_rango(datos_poblacion, num_seleccionados, min_val=0.5, max_val=1.5):
    """
    Valor esperado = Min + (Max - Min) * (Rango - 1) / (N - 1)[cite: 1].
    """
    # Ordenamos de peor a mejor para asignar rangos (1 a N)
    poblacion_ordenada = sorted(datos_poblacion, key=lambda x: x["aptitud"])
    N = len(poblacion_ordenada) #[cite: 1]
    
    valores_esperados = []
    for i, ind in enumerate(poblacion_ordenada):
        rango = i + 1
        # Aplicamos la fórmula del documento[cite: 1]
        f_rango = min_val + (max_val - min_val) * ((rango - 1) / (N - 1)) if N > 1 else 1.0 #[cite: 1]
        valores_esperados.append(f_rango)
        
    suma_rango = sum(valores_esperados)
    probabilidades = [ve / suma_rango for ve in valores_esperados]
    
    indices = np.random.choice(N, size=num_seleccionados, p=probabilidades)
    return [poblacion_ordenada[i] for i in indices]

def seleccion_boltzmann(datos_poblacion, num_seleccionados, temperatura=100.0):
    """
    Valor Esperado = e^(f_i / T) / Promedio_Poblacional[cite: 1].
    """
    N = len(datos_poblacion) #[cite: 1]
    pesos_boltzmann = [math.exp(d["aptitud"] / temperatura) for d in datos_poblacion] #[cite: 1]
    promedio_b = sum(pesos_boltzmann) / N #[cite: 1]
    
    valores_esperados = [peso / promedio_b for peso in pesos_boltzmann] #[cite: 1]
    
    suma_ve = sum(valores_esperados)
    probabilidades = [ve / suma_ve for ve in valores_esperados]
    
    indices = np.random.choice(N, size=num_seleccionados, p=probabilidades)
    return [datos_poblacion[i] for i in indices]

def muestreo_deterministico(datos_poblacion, num_seleccionados):
    """
    1. Calcular P_selecc = f_i / suma(f)
    2. Calcular poblacion esperada = n * P_selecc
    3. Asignar determinísticamente la parte entera[cite: 1].
    """
    suma_apt = sum(d["aptitud"] for d in datos_poblacion) #[cite: 1]
    esperados = []
    
    # Pasos 1 y 2[cite: 1]
    for d in datos_poblacion:
        p_selec = d["aptitud"] / suma_apt if suma_apt > 0 else 0 #[cite: 1]
        v_e = num_seleccionados * p_selec #[cite: 1]
        esperados.append({"ind": d, "entero": int(v_e), "decimal": v_e - int(v_e)}) #[cite: 1]

    seleccionados = []
    # Paso 3: Asignar parte entera[cite: 1]
    for item in esperados:
        seleccionados.extend([item["ind"]] * item["entero"]) #[cite: 1]

    # Paso 4: Ordenar por parte decimal (de mayor a menor)[cite: 1]
    esperados.sort(key=lambda x: x["decimal"], reverse=True) #[cite: 1]

    # Paso 5: Obtener padres faltantes de la parte superior[cite: 1]
    faltantes = num_seleccionados - len(seleccionados)
    for i in range(faltantes):
        seleccionados.append(esperados[i]["ind"]) #[cite: 1]

    return seleccionados