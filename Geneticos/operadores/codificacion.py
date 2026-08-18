import math

# ==========================================
# CÁLCULO DE PRECISIÓN (De la diapositiva)
# ==========================================
def calcular_bits_por_precision(u, v, P_precision):
    """
    Calcula la longitud L de la subcadena basándose en la precisión deseada.
    Fórmula de la diapositiva: L = log2( ((v - u) / P_precision) + 1 )
    """
    return math.ceil(math.log2(((v - u) / P_precision) + 1))

# ==========================================
# DECODIFICACIÓN ESTÁNDAR 1D
# ==========================================
def decodificar_variable(subcadena_bits, u, v):
    """
    Implementa la fórmula exacta de la diapositiva para una variable:
    x_i = u_i + ((v_i - u_i) / (2^(l_i) - 1)) * Sumatoria
    """
    l_i = len(subcadena_bits)
    if l_i == 0: 
        return u
        
    # La sumatoria de a_i * 2^j es la conversión binaria a decimal
    sumatoria = int("".join(str(b) for b in subcadena_bits), 2)
    
    # Aplicación de la fórmula de la imagen
    x_i = u + ((v - u) / ((2**l_i) - 1)) * sumatoria
    return x_i

def decodificar_binario(bits, a, b):
    return decodificar_variable(bits, a, b)

def gray_a_binario(bits_gray):
    """Convierte un arreglo de bits Gray a Binario estándar."""
    bits_bin = [bits_gray[0]]
    for i in range(1, len(bits_gray)):
        bits_bin.append(bits_bin[i-1] ^ bits_gray[i])
    return bits_bin

def decodificar_gray(bits, a, b):
    bits_binarios = gray_a_binario(bits)
    return decodificar_variable(bits_binarios, a, b)

# ==========================================
# DECODIFICACIÓN MULTIVARIABLE (2D: X, Y)
# ==========================================
def decodificar_binario_2d(cadena_completa, u, v):
    """
    Extrae la subcadena correspondiente a cada variable de la cadena completa 
    y aplica la decodificación.
    """
    l_total = len(cadena_completa)
    l_i = l_total // 2  # Longitud de subcadena por variable
    
    # 1. Extraer subcadenas
    subcadena_x = cadena_completa[:l_i]
    subcadena_y = cadena_completa[l_i:]
    
    # 2. Decodificar variables (Límites iguales para X y Y en este caso)
    x1 = decodificar_variable(subcadena_x, u, v)
    x2 = decodificar_variable(subcadena_y, u, v)
    
    return (x1, x2)

def decodificar_gray_2d(cadena_completa, u, v):
    """
    Extrae la subcadena en código Gray, la convierte a binario y decodifica.
    """
    l_total = len(cadena_completa)
    l_i = l_total // 2  
    
    subcadena_x = cadena_completa[:l_i]
    subcadena_y = cadena_completa[l_i:]
    
    # Decodificamos cada variable transformando primero de Gray a Binario
    x1 = decodificar_variable(gray_a_binario(subcadena_x), u, v)
    x2 = decodificar_variable(gray_a_binario(subcadena_y), u, v)
    
    return (x1, x2)