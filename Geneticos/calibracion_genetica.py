import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import time

# Importamos tu fábrica de operadores genéticos modulares
import operadores as op

def capturar_imagen_webcam():
    cap = cv2.VideoCapture(0) 
    if not cap.isOpened():
        print("Error: No se pudo establecer conexión con la cámara web.")
        return None

    print("\n" + "="*30)
    print(" CÁMARA INICIADA (VISTA EN VIVO)")
    print("="*30)
    print("  > Presiona 'ESPACIO' para tomar la foto.")
    print("  > Presiona 'ESC' para cancelar.")
    print("="*30 + "\n")

    frame_capturado = None
    while True:
        ret, frame = cap.read()
        if not ret: break
        cv2.imshow("Calibracion Optica - ESPACIO para foto", frame)
        tecla = cv2.waitKey(1) & 0xFF
        if tecla == 32: 
            frame_capturado = frame.copy()
            break
        elif tecla == 27: 
            break

    cap.release()
    cv2.destroyAllWindows()
    return frame_capturado

# ==========================================
# 1. INICIALIZACIÓN DE VARIABLES GLOBALES
# ==========================================
obj_points = None
img_points_target = None
img_shape = None

# Límite genético para los 8 parámetros INTRÍNSECOS
# (Se ajustarán al tamaño de tu foto más abajo)
BOUNDS = [
    (500, 1100), (500, 1100),    # fx, fy
    (160, 480), (120, 360),      # cx, cy
    (-0.5, 0.5), (-0.5, 0.5),    # k1, k2
    (-0.05, 0.05), (-0.05, 0.05) # p1, p2
]

def decodificar_cromosoma_real(individuo_normalizado):
    return [low + gen * (high - low) for gen, (low, high) in zip(individuo_normalizado, BOUNDS)]

def evaluar_aptitud_cv(individuo_normalizado):
    """
    El AG solo optimiza los 8 parámetros INTRÍNSECOS.
    OpenCV calcula la posición extrínseca perfecta (solvePnP) para evaluar el error.
    """
    params = decodificar_cromosoma_real(individuo_normalizado)
    fx, fy, cx, cy, k1, k2, p1, p2 = params
    
    cam_matrix = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]], dtype=np.float32)
    dist = np.array([k1, k2, p1, p2, 0], dtype=np.float32)
    
    try:
        # OpenCV resuelve la pose 3D (rotación y traslación) analíticamente
        exito, rvec, tvec = cv2.solvePnP(obj_points, img_points_target, cam_matrix, dist)
        if not exito: return 1e-6, np.zeros_like(img_points_target), 9999.0
            
        proj_points, _ = cv2.projectPoints(obj_points, rvec, tvec, cam_matrix, dist)
        proj_points = proj_points.reshape(-1, 2)
        
        mse = np.mean(np.linalg.norm(img_points_target - proj_points, axis=1))
        aptitud = 1.0 / (mse + 1e-6)
        return aptitud, proj_points, mse
    except:
        return 1e-6, np.zeros_like(img_points_target), 9999.0

# ==========================================
# 2. CAPTURA DE IMAGEN Y DETECCIÓN REAL (OPENCV 4.8+)
# ==========================================
imagen_real = capturar_imagen_webcam()
if imagen_real is None:
    print("Saliendo. No se tomó fotografía.")
    exit()

print("Detectando esquinas ChArUco reales...")

# --- CONFIGURACIÓN DE TU TABLETA ---
cuadros_x, cuadros_y = 5, 7       
tamano_cuadro = 0.04              
tamano_marcador = 0.02            

diccionario = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
tablero = cv2.aruco.CharucoBoard((cuadros_x, cuadros_y), tamano_cuadro, tamano_marcador, diccionario)

gray = cv2.cvtColor(imagen_real, cv2.COLOR_BGR2GRAY)
img_shape = gray.shape

# --- SOLUCIÓN PARA EL ERROR DE VERSIÓN: Usar CharucoDetector ---
charuco_detector = cv2.aruco.CharucoDetector(tablero)
charuco_corners, charuco_ids, _, _ = charuco_detector.detectBoard(gray)

if charuco_corners is not None and len(charuco_corners) > 3:
    print(f"¡Éxito! Se detectaron {len(charuco_corners)} puntos reales en la foto.")
    
    # 1. Obtenemos los puntos 3D de la tableta (Z=0)
    obj_points = tablero.getChessboardCorners()[charuco_ids.flatten()]
    
    # 2. Obtenemos los puntos 2D (píxeles) detectados en la foto
    img_points_target = charuco_corners.reshape(-1, 2)
    
    # 3. Ajustamos los límites de la cámara al tamaño de tu fotografía
    alto, ancho = img_shape
    BOUNDS[0] = (ancho * 0.5, ancho * 2.0) # fx
    BOUNDS[1] = (ancho * 0.5, ancho * 2.0) # fy
    BOUNDS[2] = (ancho * 0.4, ancho * 0.6) # cx
    BOUNDS[3] = (alto * 0.4, alto * 0.6)   # cy
    print(f"Límites de cámara ajustados a: {ancho}x{alto}")
else:
    print("Error: No se detectaron suficientes esquinas ChArUco en la tableta.")
    print("Asegúrate de que la tableta se vea bien, con brillo alto para evitar reflejos.")
    exit()

# ==========================================
# 3. CICLO EVOLUTIVO PASO A PASO
# ==========================================
POP_SIZE = 100
GENERATIONS = 1500   
PROB_MUTACION = 0.2
PASO_REPORTE = max(1, GENERATIONS // 10) 

print("\nInicializando Población (8 Parámetros Intrínsecos)...")
# El cromosoma ahora tiene 8 genes (quitamos rotación/traslación porque solvePnP lo hace por nosotros)
poblacion = [[np.random.rand() for _ in range(8)] for _ in range(POP_SIZE)]
historial_reporte = []

print("--- INICIANDO OPTIMIZACIÓN EVOLUTIVA ---")
for gen in range(GENERATIONS):
    
    datos_pob = []
    suma_apt = 0.0
    for ind in poblacion:
        apt, pts, mse = evaluar_aptitud_cv(ind)
        datos_pob.append({'bits': ind, 'aptitud': apt, 'pts': pts, 'mse': mse})
        suma_apt += apt

    for d in datos_pob:
        d['probabilidad'] = d['aptitud'] / suma_apt if suma_apt > 0 else 0

    datos_pob.sort(key=lambda x: x['aptitud'], reverse=True)
    mejor_gen = datos_pob[0]

    if gen % PASO_REPORTE == 0 or gen == GENERATIONS - 1:
        historial_reporte.append({
            'gen': gen, 
            'mse': mejor_gen['mse'], 
            'pts': mejor_gen['pts'].copy()
        })
        
    if gen % (PASO_REPORTE // 2) == 0 or gen == GENERATIONS - 1:
        print(f"Generación {gen:04d} | RMSE Reproyección: {mejor_gen['mse']:.4f} px")

    # Selección Boltzmann
    temp_actual = max(1.0, 100.0 * (1.0 - (gen / GENERATIONS)))
    padres = op.SELECCION['boltzmann'](datos_pob, POP_SIZE, temperatura=temp_actual)

    # Cruza y Elitismo
    siguiente_generacion = [mejor_gen['bits'].copy()]
    for i in range(0, len(padres) - 1, 2):
        p1 = padres[i]['bits'].copy()
        p2 = padres[i+1]['bits'].copy()
        h1, h2 = op.CRUZA['aritmetica_real'](p1, p2, 8, alpha=0.35)
        siguiente_generacion.extend([h1, h2])

    siguiente_generacion = siguiente_generacion[:POP_SIZE]

    # Mutación
    for i in range(1, len(siguiente_generacion)): 
        if np.random.rand() < PROB_MUTACION:
            ind_mutado = op.MUTACION['gaussiana'](siguiente_generacion[i], media=0.0, desviacion=0.1)
            siguiente_generacion[i] = [np.clip(val, 0.0, 1.0) for val in ind_mutado]

    poblacion = siguiente_generacion

# ==========================================
# 4. GENERACIÓN DE REPORTE PDF FINAL
# ==========================================
print("\nGenerando Reporte PDF de Calibración...")
nombre_pdf = "Reporte_Calibracion_Metrologia.pdf"

fondo_rgb = cv2.cvtColor(imagen_real, cv2.COLOR_BGR2RGB) if imagen_real is not None else None

with PdfPages(nombre_pdf) as pdf:
    
    # PÁGINA 1: PORTADA
    fig_portada, ax_portada = plt.subplots(figsize=(8.5, 11))
    ax_portada.axis('off')
    texto = "REPORTE DE CALIBRACIÓN ESTENOPEICA\n"
    texto += "VÍA ALGORITMOS GENÉTICOS\n"
    texto += "="*40 + "\n\n"
    texto += "Configuración Modular Utilizada:\n"
    texto += "  > Codificación:\tVectores Reales (Normalizados [0, 1])\n"
    texto += "  > Función Fitness:\tMinimización RMSE (Reproyección OpenCV)\n"
    texto += "  > Selección:\t\tBoltzmann (Enfriamiento Dinámico)\n"
    texto += "  > Cruza:\t\tAritmética Real (alpha=0.35)\n"
    texto += "  > Mutación:\t\tGaussiana (desv=0.1)\n"
    texto += "  > Elitismo:\t\tActivado (1 individuo)\n\n"
    texto += "="*40 + "\nCentro de Investigaciones en Óptica\nMaestría en Optomecatrónica"
    
    ax_portada.text(0.1, 0.8, texto, transform=ax_portada.transAxes, fontsize=14, family='monospace', verticalalignment='top')
    pdf.savefig(fig_portada)
    plt.close(fig_portada)

    # PÁGINAS MEDIAS: PROGRESO DINÁMICO
    for snap in historial_reporte[:-1]:
        fig, ax = plt.subplots(figsize=(10, 7))
        ax.set_title(f"Avance - Generación {snap['gen']} | RMSE: {snap['mse']:.4f} px", weight='bold')
        
        if fondo_rgb is not None:
            ax.imshow(fondo_rgb)
        
        ax.scatter(img_points_target[:, 0], img_points_target[:, 1], c='red', s=80, marker='x', label='Esquinas Detectadas (Target)')
        ax.scatter(snap['pts'][:, 0], snap['pts'][:, 1], c='cyan', s=40, alpha=0.9, label='Proyección Algoritmo')
        
        ax.grid(False)
        ax.legend()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)

    # PÁGINA FINAL: CONVERGENCIA ABSOLUTA
    snap_final = historial_reporte[-1]
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_title(f"CONVERGENCIA FINAL (Gen {snap_final['gen']}) | RMSE: {snap_final['mse']:.4f} px", weight='bold', color='green')
    
    if fondo_rgb is not None:
        ax.imshow(fondo_rgb)
        
    ax.scatter(img_points_target[:, 0], img_points_target[:, 1], c='red', s=120, marker='X', label='Esquinas Reales de la Foto')
    ax.scatter(snap_final['pts'][:, 0], snap_final['pts'][:, 1], c='lime', s=60, edgecolors='black', label='Proyección Final Optimizada')
    
    for t_pt, p_pt in zip(img_points_target, snap_final['pts']):
        ax.plot([t_pt[0], p_pt[0]], [t_pt[1], p_pt[1]], 'w-', alpha=0.6, linewidth=1)

    ax.grid(False)
    ax.legend()
    pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)

print(f"\n¡Optimización terminada! Revisa el archivo '{nombre_pdf}' para ver el reporte visual.")