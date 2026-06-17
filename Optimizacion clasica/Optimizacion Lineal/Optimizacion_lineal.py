import numpy as np

def optimizar_naranjas():
    
    # Restricciones de forma Ax + By = C
    # 1. 0.5*x_A + 0.8*x_B = 500 (Presupuesto)
    # 2. 1.0*x_A + 1.0*x_B = 700 (Capacidad)
    
    # Lista para almacenar todos los vértices posibles (intersecciones)
    vertices_potenciales = []
    
    # Origen (del eje x, y)
    vertices_potenciales.append(np.array([0.0, 0.0]))
    
    # Intersecciones con los ejes (x_A = 0 o x_B = 0)
    # Restricción de presupuesto:
    vertices_potenciales.append(np.array([500.0 / 0.5, 0.0]))
    vertices_potenciales.append(np.array([0.0, 500.0 / 0.8]))
    
    # Restricción de capacidad:
    vertices_potenciales.append(np.array([700.0 / 1.0, 0.0]))
    vertices_potenciales.append(np.array([0.0, 700.0 / 1.0]))
    
    # 3. Intersección entre las dos rectas (Resolución del sistema 2x2)
    a1, b1, c1 = 0.5, 0.8, 500.0
    a2, b2, c2 = 1.0, 1.0, 700.0
    
    determinante = (a1 * b2) - (a2 * b1)
    if determinante != 0:
        x_A_int = (c1 * b2 - c2 * b1) / determinante
        x_B_int = (a1 * c2 - a2 * c1) / determinante
        vertices_potenciales.append(np.array([x_A_int, x_B_int]))

    # Evaluar los vértices factibles
    mejor_beneficio = -1.0
    mejor_compra = None
    
    # Tolerancia para evitar errores de precisión de punto flotante
    tol = 1e-6 

    for vertice in vertices_potenciales:
        x_A = vertice[0]
        x_B = vertice[1]
        
        # Validar si el vértice cumple todas las restricciones (factibilidad)
        cond_negatividad = (x_A >= -tol) and (x_B >= -tol)
        cond_presupuesto = (0.5 * x_A + 0.8 * x_B) <= (500.0 + tol)
        cond_capacidad = (x_A + x_B) <= (700.0 + tol)
        
        if cond_negatividad and cond_presupuesto and cond_capacidad:
            # Calcular función objetivo
            beneficio = 0.08 * x_A + 0.10 * x_B
            
            if beneficio > mejor_beneficio:
                mejor_beneficio = beneficio
                mejor_compra = (x_A, x_B)

    print(f"La compra óptima es: {round(mejor_compra[0], 2)} kg de Tipo A y {round(mejor_compra[1], 2)} kg de Tipo B.")
    print(f"El beneficio máximo obtenido será de: {round(mejor_beneficio, 2)} Pesos.\n")

optimizar_naranjas()