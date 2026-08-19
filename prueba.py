import numpy as np
import cv2
import matplotlib.pyplot as plt
import time

# ==========================================
# 1. GENERACIÓN DE DATOS SINTÉTICOS (Ground Truth)
# ==========================================
# Simulamos un tablero ChArUco de 5x5 esquinas en el espacio 3D (Z=0)
obj_points = np.zeros((25, 3), np.float32)
x, y = np.meshgrid(np.arange(5), np.arange(5))
obj_points[:, 0] = x.flatten() * 30  # Cuadros de 30 mm
obj_points[:, 1] = y.flatten() * 30

# Parámetros "Reales" de la cámara (lo que el AG debe descubrir)
true_fx, true_fy = 800.0, 800.0
true_cx, true_cy = 320.0, 240.0 # Resolución simulada 640x480
true_k1, true_k2 = -0.1, 0.05
true_rvec = np.array([[0.2], [0.2], [0.0]], dtype=np.float32)
true_tvec = np.array([[10.0], [-10.0], [150.0]], dtype=np.float32) # A 150mm de distancia

true_camera_matrix = np.array([[true_fx, 0, true_cx], [0, true_fy, true_cy], [0, 0, 1]], dtype=np.float32)
true_dist_coeffs = np.array([true_k1, true_k2, 0, 0, 0], dtype=np.float32)

# Puntos 2D "Detectados" en la imagen (nuestro objetivo)
img_points_target, _ = cv2.projectPoints(obj_points, true_rvec, true_tvec, true_camera_matrix, true_dist_coeffs)
img_points_target = img_points_target.reshape(-1, 2)

# ==========================================
# 2. DEFINICIÓN DEL ALGORITMO GENÉTICO
# ==========================================
# Cromosoma: [fx, fy, cx, cy, k1, k2, rx, ry, rz, tx, ty, tz] (12 parámetros)
BOUNDS = [
    (500, 1100), (500, 1100),    # fx, fy
    (160, 480), (120, 360),      # cx, cy
    (-0.5, 0.5), (-0.5, 0.5),    # k1, k2
    (-0.5, 0.5), (-0.5, 0.5), (-0.5, 0.5), # rotaciones
    (-50, 50), (-50, 50), (50, 250)        # traslaciones
]

def create_individual():
    """Genera un cromosoma aleatorio dentro de los límites ópticos."""
    return np.array([np.random.uniform(low, high) for low, high in BOUNDS])

def calculate_fitness(individual):
    """Calcula el Error Cuadrático Medio de reproyección."""
    fx, fy, cx, cy, k1, k2, rx, ry, rz, tx, ty, tz = individual
    cam_matrix = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]], dtype=np.float32)
    dist = np.array([k1, k2, 0, 0, 0], dtype=np.float32)
    rvec = np.array([[rx], [ry], [rz]], dtype=np.float32)
    tvec = np.array([[tx], [ty], [tz]], dtype=np.float32)
    
    try:
        proj_points, _ = cv2.projectPoints(obj_points, rvec, tvec, cam_matrix, dist)
        proj_points = proj_points.reshape(-1, 2)
        # Error de reproyección (distancia euclidiana promedio)
        mse = np.mean(np.linalg.norm(img_points_target - proj_points, axis=1))
        return 1.0 / (mse + 1e-6), proj_points # Retornamos la aptitud y los puntos para graficar
    except:
        return 1e-6, np.zeros_like(img_points_target) # Penalización si las matemáticas colapsan

def crossover(p1, p2):
    """Cruza aritmética: crea un hijo promediando los genes de los padres."""
    alpha = np.random.rand()
    return alpha * p1 + (1 - alpha) * p2

def mutate(individual, mutation_rate=0.1, generation_progress=0):
    """Mutación Gaussiana con decaimiento (simulated annealing ligero)."""
    mutated = individual.copy()
    # A medida que avanzan las generaciones, la mutación es más fina
    mutation_strength = 1.0 - generation_progress 
    
    for i, (low, high) in enumerate(BOUNDS):
        if np.random.rand() < mutation_rate:
            rango = high - low
            ruido = np.random.normal(0, rango * 0.05 * mutation_strength)
            mutated[i] = np.clip(mutated[i] + ruido, low, high)
    return mutated

# ==========================================
# 3. EJECUCIÓN Y VISUALIZACIÓN INTERACTIVA
# ==========================================
POP_SIZE = 100
GENERATIONS = 150
population = [create_individual() for _ in range(POP_SIZE)]

plt.ion() # Modo interactivo para animaciones
fig, ax = plt.subplots(figsize=(10, 7))

# Mostrar solo los puntos detectados inicialmente
ax.set_title("Paso 1: Puntos detectados del ChArUco (Target)")
ax.scatter(img_points_target[:, 0], img_points_target[:, 1], c='red', s=50, marker='x', label='Puntos Reales (Detección)')
ax.set_xlim(0, 640)
ax.set_ylim(480, 0) # Invertimos Y para que coincida con coordenadas de imagen
ax.legend()
plt.draw()
print("Mostrando los puntos iniciales... (Esperando 3 segundos)")
plt.pause(3)



for gen in range(GENERATIONS):
    # 1. Evaluar población
    evaluations = [calculate_fitness(ind) for ind in population]
    fitness_scores = [eval[0] for eval in evaluations]
    proj_points_list = [eval[1] for eval in evaluations]
    
    # 2. Ordenar de mejor a peor
    sorted_indices = np.argsort(fitness_scores)[::-1]
    population = [population[i] for i in sorted_indices]
    proj_points_list = [proj_points_list[i] for i in sorted_indices]
    best_error = (1.0 / fitness_scores[sorted_indices[0]]) - 1e-6

    # 3. Visualizar cada 10 generaciones
    if gen % 10 == 0 or gen == GENERATIONS - 1:
        ax.clear()
        ax.set_xlim(0, 640)
        ax.set_ylim(480, 0)
        ax.set_title(f"Generación {gen} | Mejor Error de Reproyección: {best_error:.2f} px")
        
        # Graficar target
        ax.scatter(img_points_target[:, 0], img_points_target[:, 1], c='red', s=80, marker='X', label='Puntos Reales')
        
        # Graficar los mejores 5 individuos
        colors = ['blue', 'green', 'purple', 'orange', 'cyan']
        for i in range(5):
            pts = proj_points_list[i]
            # Solo graficar si los puntos tienen sentido (no están en el infinito)
            if not np.all(pts == 0):
                ax.scatter(pts[:, 0], pts[:, 1], c=colors[i], s=20, alpha=0.6, 
                           label=f'Individuo Top {i+1}' if i==0 else "")
                
        ax.legend(loc='upper right')
        plt.draw()
        plt.pause(0.5)

    # 4. Selección, Cruza y Muta (Generar nueva población)
    new_population = [population[0], population[1]] # Elitismo: guardar a los 2 mejores
    
    # Progreso de 0.0 a 1.0 para disminuir la fuerza de mutación
    progress = gen / GENERATIONS 
    
    while len(new_population) < POP_SIZE:
        # Selección por torneo (elegir al azar 5, tomar el mejor)
        torneo1 = np.random.choice(POP_SIZE, 5)
        padre1 = population[min(torneo1)] # El índice más bajo es el mejor
        
        torneo2 = np.random.choice(POP_SIZE, 5)
        padre2 = population[min(torneo2)]
        
        hijo = crossover(padre1, padre2)
        hijo = mutate(hijo, mutation_rate=0.2, generation_progress=progress)
        new_population.append(hijo)
        
    population = new_population

# ==========================================
# 4. RESULTADO FINAL
# ==========================================
print("¡Optimización terminada!")
best_individual = population[0]
print(f"Distancia Focal encontrada: fx={best_individual[0]:.2f}, fy={best_individual[1]:.2f}")
print(f"Punto Principal encontrado: cx={best_individual[2]:.2f}, cy={best_individual[3]:.2f}")

plt.ioff()
plt.show()