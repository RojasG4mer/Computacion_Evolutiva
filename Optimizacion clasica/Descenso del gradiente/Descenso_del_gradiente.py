import numpy as np
import matplotlib.pyplot as plt


print("Descenso del gradiente")
def Desc_Grad_Cauchy_2D(fun, inicio=(0, 0), tol=1e-4, max_iter=10, alpha_init=0.1):
    
    x_n, y_n = inicio
    h = 1e-5  # Diferencial para derivada

    for i in range(max_iter):
        
        # Derivada en cada dirección (gradiente por partes)
        df_dx = (fun(x_n + h, y_n) - fun(x_n - h, y_n)) / (2 * h)
        df_dy = (fun(x_n, y_n + h) - fun(x_n, y_n - h)) / (2 * h)
        
        # si el gradiente es ~0, ya estamos en un punto crítico
        if (df_dx**2 + df_dy**2)**0.5 < tol:
            # print(f"Gradiente nulo. Punto crítico (probable mínimo) encontrado en {i} iteraciones.")
            return (x_n, y_n)

        # Función para evaluar el metodo
        def g(alpha):
            return fun(x_n - alpha * df_dx, y_n - alpha * df_dy)

        # OPTIMIZACIÓN DEL PASO
        # Buscamos la raíz de la derivada de g(alpha), es decir, g'(alpha) = 0
        alpha_opt = alpha_init  # Suposición inicial
        
        for _ in range(10): 
            # Primera derivada de g respecto a alpha
            g_prime = (g(alpha_opt + h) - g(alpha_opt - h)) / (2 * h)
            
            # Segunda derivada de g respecto a alpha
            g_double_prime = (g(alpha_opt + h) - 2 * g(alpha_opt) + g(alpha_opt - h)) / (h**2)
            
            if abs(g_double_prime) < 1e-8:
                break # Evitar división por cero si la pendiente se vuelve plana
                
            # Actualizamos alpha 
            alpha_opt = alpha_opt - (g_prime / g_double_prime)

        # ACTUALIZAR EL PUNTO CON EL ALPHA ÓPTIMO
        x_next = x_n - alpha_opt * df_dx
        y_next = y_n - alpha_opt * df_dy
        
        print(f"Iteración {i+1}: λ = {alpha_opt:.4f} -> x = {x_next:.4f}, y = {y_next:.4f}")

        # Nos detenemos cuando se llegue al mínimo
        distancia = ((x_next - x_n)**2 + (y_next - y_n)**2)**0.5
        if distancia < tol:
            print(f"Mínimo encontrado en {i+1} iteraciones.")
            return (x_next, y_next)
            
        # Preparar siguiente iteración
        x_n = x_next
        y_n = y_next

    print("Error: Se alcanzó el número máximo de iteraciones sin converger.")
    return None

def fxy2D(x, y):
    return 4*x**3 - 2*x**2*y + 5*x*y**2 + 12*x**2 + 2*x + 2*y + 10


Desc_Grad_Cauchy_2D(fxy2D, inicio=(10, 10), max_iter=20, alpha_init=0.01)
