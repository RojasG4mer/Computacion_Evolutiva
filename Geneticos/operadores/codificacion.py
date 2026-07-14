def decodificar_binario(bits, a, b):
    """Convierte una lista de bits en binario estándar a decimal interpolado."""
    n = len(bits) #[cite: 1]
    decimal = int("".join(str(bit) for bit in bits), 2) #[cite: 1]
    return a + decimal * (b - a) / ((2**n) - 1) #[cite: 1]

def gray_a_binario(bits_gray):
    """
    Convierte una lista de bits en código Gray a binario estándar.
    La regla: el primer bit baja igual, los siguientes son el XOR 
    del bit binario anterior y el bit Gray actual.
    """
    bits_bin = [bits_gray[0]]
    for i in range(1, len(bits_gray)):
        # Operador ^ es el XOR en Python
        bit_convertido = bits_bin[i-1] ^ bits_gray[i]
        bits_bin.append(bit_convertido)
    return bits_bin

def decodificar_gray(bits, a, b):
    """
    Decodifica asumiendo que los genes están en código Gray.
    Primero pasa de Gray a Binario, y luego reutiliza la función estándar.
    """
    bits_binarios = gray_a_binario(bits)
    return decodificar_binario(bits_binarios, a, b)

# Extra: Función que tenías en tu notebook para convertir de binario a Gray
def binario_a_gray(bits_bin):
    """
    Convierte binario estándar a Gray (Útil si quieres inicializar 
    una población con un valor específico).
    """
    bits_gray = [bits_bin[0]]
    for i in range(1, len(bits_bin)):
        bit_convertido = bits_bin[i-1] ^ bits_bin[i]
        bits_gray.append(bit_convertido)
    return bits_gray #[cite: 1]