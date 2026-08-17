# Actualiza las importaciones en la parte superior:
from .seleccion import ruleta, torneo, torneo_umbral, seleccion_rango, seleccion_boltzmann, muestreo_deterministico
from .cruza import un_punto, uniforme, cruza_n_puntos, cruza_uniforme_prob, cruza_aritmetica_real, cruza_geometrica_real
from .escalamiento import minimizacion_fmax_conocido, minimizacion_fmin_inverso, escalamiento_lineal # <--- Nuevo archivo

# Agrega los nuevos métodos a los diccionarios existentes:
SELECCION = {
    "ruleta": ruleta,
    "torneo": torneo,
    "torneo_umbral": torneo_umbral,
    "rango": seleccion_rango,
    "boltzmann": seleccion_boltzmann,
    "deterministico": muestreo_deterministico
}

CRUZA = {
    "un_punto": un_punto,
    "uniforme": uniforme,
    "n_puntos": cruza_n_puntos,
    "uniforme_prob": cruza_uniforme_prob,
    "aritmetica_real": cruza_aritmetica_real,
    "geometrica_real": cruza_geometrica_real
}

# (APTITUD, MUTACION Y CODIFICACION quedan igual)