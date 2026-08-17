# operadores/escalamiento.py
import math

def minimizacion_fmax_conocido(f_x, f_max=100.0):
    """
    Ecuación (1): Phi(x) = f_max - f(x). 
    Útil si la meta es minimizar y conocemos el valor máximo.
    """
    return f_max - f_x #

def minimizacion_fmin_inverso(f_x, f_min_t=0.0):
    """
    Ecuación (3): Phi(x) = 1 / (1 + f(x) - f_min(t)).
    Resultan valores de 0 a 1, donde 1 es el mejor.
    """
    return 1.0 / (1.0 + f_x - f_min_t) #[cite: 1]

def escalamiento_lineal(f_x, f_min, f_max, f_min_prima=10.0, f_max_prima=20.0):
    """
    Escalamiento Lineal para evitar convergencia prematura.
    f' = ((f'_max - f'_min) / (f_max - f_min)) * (f - f_min) + f'_min[cite: 1].
    """
    if f_max == f_min:
        return f_max_prima # Evita división por cero
    pendiente = (f_max_prima - f_min_prima) / (f_max - f_min) #[cite: 1]
    return pendiente * (f_x - f_min) + f_min_prima #[cite: 1]