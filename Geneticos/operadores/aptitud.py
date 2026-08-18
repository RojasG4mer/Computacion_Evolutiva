import math
import random

# ==========================================
# FUNCIONES ORIGINALES
# ==========================================
def funcion_polinomial(x):
    """
    Función de aptitud original del algoritmo.
    """
    return -x**3 + 60*x**2 + 15000

def funcion_cauchy(x):
    """
    Función para el algoritmo de Cauchy.
    """
    # Ejemplo de estructura (debes poner tu fórmula real si es diferente):
    return 1 / (math.pi * (1 + x**2)) 

def funcion_lineal(x):
    """
    Función lineal para el análisis de zonas y líneas de intersección.
    """
    # Ejemplo de estructura lineal básica:
    return x 

import math
import random

# Funciones 1D originales (Se mantienen por compatibilidad)
def funcion_polinomial(x): return -x**3 + 60*x**2 + 15000
def funcion_cauchy(x): return 1 / (math.pi * (1 + x**2)) 
def funcion_lineal(x): return x 

# ==========================================
# FUNCIONES DE JONG PARA GRÁFICAS 3D (X, Y)
# ==========================================
def de_jong_1_esfera(valores):
    x, y = valores
    return x**2 + y**2

def de_jong_3_escalon(valores):
    x, y = valores
    return math.floor(x) + math.floor(y)

def de_jong_4_cuartica_ruido(valores):
    x, y = valores
    return (x**4) + (y**4) + random.gauss(0, 1)

def rastrigin_2d(valores):
    x, y = valores
    return 20 + (x**2 - 10 * math.cos(2 * math.pi * x)) + (y**2 - 10 * math.cos(2 * math.pi * y))

def ackley_2d(valores):
    x, y = valores
    termino1 = -20 * math.exp(-0.2 * math.sqrt(0.5 * (x**2 + y**2)))
    termino2 = -math.exp(0.5 * (math.cos(2 * math.pi * x) + math.cos(2 * math.pi * y)))
    return termino1 + termino2 + 20 + math.e