# 1. Importamos las funciones desde los archivos individuales
from .seleccion import ruleta, torneo
from .cruza import un_punto, uniforme
from .aptitud import funcion_polinomial, funcion_cauchy, funcion_lineal
from .muta import mutacion_un_bit, mutacion_multiple
from .codificacion import decodificar_binario, decodificar_gray

# 2. Creamos los diccionarios (Fábricas) para acceder a las funciones
SELECCION = {
    "ruleta": ruleta,
    "torneo": torneo
}

CRUZA = {
    "un_punto": un_punto,
    "uniforme": uniforme
}

APTITUD = {
    "polinomial": funcion_polinomial,
    "cauchy": funcion_cauchy,
    "lineal": funcion_lineal
}

MUTACION = {
    "un_bit": mutacion_un_bit,
    "multiple": mutacion_multiple
}

CODIFICACION = {
    "binario": decodificar_binario,
    "gray": decodificar_gray
}