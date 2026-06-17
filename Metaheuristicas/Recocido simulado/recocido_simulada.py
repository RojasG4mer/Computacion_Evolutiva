import random
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def decodificar_binario(bits, a, b):
    """
    Convierte una lista de bits a un valor real en el intervalo [a, b].
    """
    n = len(bits)
    # Convertir lista de bits a string y luego a entero decimal
    decimal = int("".join(str(bit) for bit in bits), 2)
    # Interpolar en el intervalo [a, b] (normalizar)
    return a + decimal * (b - a) / ((2**n) - 1)

def de_jong_1(x):
    """
    Función objetivo: Polinomio de De Jong 1 (Esfera) en 1D.
    f(x) = x^2
    """
    return -45*x**13 + 34*x**11 + 56*x**5 + x + 546


def Recocido_Binario(n_bits, a, b, func, minimizar=True, 
                     T_max=100.0, epsilon=0.01, tol=1e-4, 
                     tipo_temp='asintotica', alpha=0.1, iter_por_T=10):
    
    # Generar solución inicial aleatoria en formato binario
    s_actual_bits = [random.choice([0, 1]) for _ in range(n_bits)] # Creamos aleatoriamente un punto de inicio en binario
    s_actual_x = decodificar_binario(s_actual_bits, a, b)
    
    mejor_bits = list(s_actual_bits)
    mejor_x = s_actual_x
    
    T = T_max
    k = 1 # Contador de épocas para la temperatura asintótica
    
    # Lista para almacenar los registros de la tabla
    registros_tabla = []

    # Historial para graficar
    historial_x = [s_actual_x]
    historial_y = [func(s_actual_x)]
    
    s_anterior_x = s_actual_x + tol * 10 # Evitamos que no se cumpla la tolerancia en la iteración 1
    
    # T > epsilon (temperatura minima) Y la diferencia entre soluciones es mayor a la Tolerancia
    while T > epsilon and abs(s_actual_x - s_anterior_x) >= tol:
        
        s_anterior_x = s_actual_x # Guardamos la solución de la época anterior
        
        # Evaluamos para una temperatura concreta que luego haremos descender
        for _ in range(iter_por_T):
            # Generar vecino cercano
            s_vecino_bits = list(s_actual_bits)
            idx = random.randint(0, n_bits - 1)
            s_vecino_bits[idx] = 1 - s_vecino_bits[idx] # Cambia 0 a 1, o 1 a 0
            
            s_vecino_x = decodificar_binario(s_vecino_bits, a, b)
            
            # Calcular delta E
            delta_E = func(s_vecino_x) - func(s_actual_x)
            
            # Si queremos maximizar, preguntamos y solo cambiamos el signo para evaluar el cambio
            if not minimizar:
                delta_E = -delta_E 
            
            # Como solo podemos aceptar si es deltaE <= 0 o la ec de Woltzman lo permite
            aceptado = False
            # Criterio de aceptación
            if delta_E <= 0:
                aceptado = True
                # Evaluar si es el mejor histórico
                if (minimizar and func(s_vecino_x) < func(mejor_x)) or \
                   (not minimizar and func(s_vecino_x) > func(mejor_x)): ## Aqui preguntamos si queremos minimo o máximo
                    mejor_bits = list(s_vecino_bits)
                    mejor_x = s_vecino_x
            else:
                probabilidad = math.exp(-delta_E / T)
                if random.random() < probabilidad:
                    aceptado = True
            
            # Si se acepta, el vecino se vuelve la solución actual
            if aceptado:
                s_actual_bits = list(s_vecino_bits)
                s_actual_x = s_vecino_x
                
        

        # Guardar el registro para la tabla ANTES de actualizar la solución
        str_vecino = "".join(str(b) for b in s_vecino_bits)
        registros_tabla.append({
            "T": round(T, 1) if not T.is_integer() else int(T),
            # "Move": s_vecino_x
            "Solution": str_vecino,
            "x": s_actual_x,
            "Δf": delta_E,
            "Move?": "Yes" if aceptado else "No",
            "New Neighbor-Solution": str_vecino if aceptado else "".join(str(b) for b in s_actual_bits),
            'y': func(s_actual_x)
        })

        # Guardar solución de esta época para la gráfica
        historial_x.append(s_actual_x)
        historial_y.append(func(s_actual_x))
        
        # Actualización de Temperatura
        if tipo_temp == 'lineal':
            # T = T - alpha
            T = T - alpha
        elif tipo_temp == 'asintotica':
            T = T_max / (1 + alpha * k)
            
        k += 1 # Incrementar época

    return pd.DataFrame(registros_tabla)

a = -10
b = 10
tipo_temp = 'asintotica' # 'lineal' o 'asintotica'
Datos = Recocido_Binario(
    n_bits = 10,            # Longitud de la cadena binaria
    a = a,              # Límite inferior (Estándar para De Jong)
    b = b,               # Límite superior
    func = de_jong_1,       # Función a optimizar
    minimizar = False,       # True para Minimizar, False para Maximizar
    T_max = 600.0,          # Temperatura inicial
    epsilon = 0.001,        # Criterio de parada por enfriamiento (épsilon)
    tol = 1e-4,             # Criterio de parada por tolerancia de cambio
    tipo_temp = tipo_temp, # 'lineal' o 'asintotica'
    alpha = 0.5,            # Tasa de decaimiento
    iter_por_T = 10         # Vecinos evaluados por nivel de temperatura
)

print(Datos.to_string(index=False)) 
