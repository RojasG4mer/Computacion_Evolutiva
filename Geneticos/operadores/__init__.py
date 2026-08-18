from .seleccion import ruleta, torneo, torneo_umbral, seleccion_rango, seleccion_boltzmann, muestreo_deterministico
from .cruza import un_punto, uniforme, cruza_n_puntos, cruza_uniforme_prob, cruza_aritmetica_real, cruza_geometrica_real
from .muta import mutacion_un_bit, mutacion_multiple, mutacion_intercambio, mutacion_inversion_secuencia, mutacion_gaussiana
from .aptitud import funcion_polinomial, funcion_cauchy, funcion_lineal, de_jong_1_esfera, de_jong_3_escalon, de_jong_4_cuartica_ruido, rastrigin_2d, ackley_2d
from .codificacion import decodificar_binario, decodificar_gray, decodificar_binario_2d, decodificar_gray_2d
from .escalamiento import minimizacion_fmax_conocido, minimizacion_fmin_inverso, escalamiento_lineal

SELECCION = {"ruleta": ruleta, "torneo": torneo, "torneo_umbral": torneo_umbral, "rango": seleccion_rango, "boltzmann": seleccion_boltzmann, "deterministico": muestreo_deterministico}
CRUZA = {"un_punto": un_punto, "uniforme": uniforme, "n_puntos": cruza_n_puntos, "uniforme_prob": cruza_uniforme_prob, "aritmetica_real": cruza_aritmetica_real, "geometrica_real": cruza_geometrica_real}
MUTACION = {"un_bit": mutacion_un_bit, "multiple": mutacion_multiple, "intercambio": mutacion_intercambio, "inversion": mutacion_inversion_secuencia, "gaussiana": mutacion_gaussiana}
APTITUD = {"polinomial": funcion_polinomial, "cauchy": funcion_cauchy, "lineal": funcion_lineal, "de_jong_1": de_jong_1_esfera, "de_jong_3": de_jong_3_escalon, "de_jong_4": de_jong_4_cuartica_ruido, "rastrigin": rastrigin_2d, "ackley": ackley_2d}

CODIFICACION = {
    "binario": decodificar_binario, "gray": decodificar_gray,
    "binario_2d": decodificar_binario_2d, "gray_2d": decodificar_gray_2d # NUEVOS!
}