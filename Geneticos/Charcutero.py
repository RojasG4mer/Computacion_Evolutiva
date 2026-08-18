import cv2
import numpy as np
import glob
import random

# Importamos tu fábrica de operadores modulares
import operadores as op

# =========================================================
# 1. INTEGRACIÓN CON OPENCV: DETECCIÓN DE PATRÓN CHARUCO
# =========================================================
def obtener_puntos_charuco(ruta_imagenes, squares_x=5, squares_y=7, square_length=0.04, marker_length=0.02):
    """
    Lee las imágenes de calibración y extrae los puntos 3D (objpoints) 
    y 2D (imgpoints) usando el tablero ChArUco.
    """
    print("Detectando esquinas ChArUco en las imágenes...")
    
    # Configuración del diccionario y el tablero
    diccionario = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    tablero = cv2.aruco.CharucoBoard((squares_x, squares_y), square_length, marker_length, diccionario)
    
    objpoints = [] # Puntos 3D en el espacio del mundo real
    imgpoints = [] # Puntos 2D en el plano de la imagen
    
    imagenes = glob.glob(ruta_imagenes)
    tamano_imagen = None

    for fname in imagenes:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if tamano_imagen is None:
            tamano_imagen = gray.shape[::-1] # (Ancho, Alto)

        # 1. Detectar marcadores ArUco
        corners, ids, _ = cv2.aruco.detectMarkers(gray, diccionario)
        
        if len(corners) > 0:
            # 2. Interpolar esquinas interiores del tablero ChArUco
            ret, charuco_corners, charuco_ids = cv2.aruco.interpolateCornersCharuco(corners, ids, gray, tablero)
            
            # 3. Si encontramos suficientes esquinas, las guardamos
            if ret > 3:
                # Obtener las coordenadas 3D de las esquinas detectadas
                objp = tablero.getChessboardCorners()[charuco_ids.flatten()]
                objpoints.append(objp)
                imgpoints.append(charuco_corners)

    print(f"Puntos extraídos con éxito de {len(objpoints)} imágenes. Tamaño imagen: {tamano_imagen}")
    return objpoints, imgpoints, tamano_imagen


# =========================================================
# 2. LA FUNCIÓN FITNESS: ERROR DE REPROYECCIÓN (RMSE)
# =========================================================
def evaluar_error_reproyeccion(cromosoma, objpoints, imgpoints):
    """
    Recibe un cromosoma con 8 genes Reales: [fx, fy, cx, cy, k1, k2, p1, p2].
    Devuelve la aptitud (mayor es mejor).
    """
    fx, fy, cx, cy, k1, k2, p1, p2 = cromosoma
    
    # Construimos la matriz intrínseca K
    camera_matrix = np.array([
        [fx,  0, cx],
        [ 0, fy, cy],
        [ 0,  0,  1]
    ], dtype=np.float32)
    
    # Construimos el vector de distorsión (asumimos k3=0 para este experimento)
    dist_coeffs = np.array([k1, k2, p1, p2, 0.0], dtype=np.float32)

    error_total = 0.0
    puntos_totales = 0

    for objp, imgp in zip(objpoints, imgpoints):
        # solvePnP analítico para calcular rotación y traslación extrínseca
        exito, rvec, tvec = cv2.solvePnP(objp, imgp, camera_matrix, dist_coeffs)
        
        if not exito:
            return 0.0 # Castigo severo si la cámara colapsa matemáticamente
            
        # Proyectamos los puntos 3D de vuelta a la imagen con la cámara propuesta
        imgp_proyectados, _ = cv2.projectPoints(objp, rvec, tvec, camera_matrix, dist_coeffs)
        
        # Calculamos la distancia Euclidiana (L2 Norm) entre puntos reales y proyectados
        error = cv2.norm(imgp, imgp_proyectados, cv2.NORM_L2)
        error_total += error ** 2 # Suma de errores cuadráticos
        puntos_totales += len(objp)

    # Error Cuadrático Medio (RMSE)
    if puntos_totales == 0: return 0.0
    rmse = np.sqrt(error_total / puntos_totales)
    
    # Como el AG busca MAXIMIZAR, invertimos el error. 
    # Si RMSE es 0, la aptitud será 1.0 (Óptimo Perfecto)
    aptitud = 1.0 / (1.0 + rmse)
    return aptitud


# =========================================================
# 3. EL CICLO EVOLUTIVO PRINCIPAL
# =========================================================
def main():
    # A. CONFIGURACIÓN DEL SISTEMA DE VISIÓN
    ruta_dataset = "calibracion_imgs/*.jpg" # <--- CAMBIA ESTO A TU RUTA
    objpoints, imgpoints, img_shape = obtener_puntos_charuco(ruta_dataset)
    
    if not objpoints:
        print("Error: No se encontraron puntos en las imágenes.")
        return

    ancho, alto = img_shape
    
    # B. CONFIGURACIÓN DEL ALGORITMO GENÉTICO
    TAMANO_POBLACION = 100
    GENERACIONES = 50
    PROB_MUTACION = 0.2
    
    # Definimos los límites [Mínimo, Máximo] para inicializar los 8 genes
    # [fx, fy, cx, cy, k1, k2, p1, p2]
    # Se ajustan dependiendo de la resolución de tu cámara
    limites = [
        [ancho * 0.5, ancho * 2.0], # fx (Suele ser entre 0.5 y 2 veces el ancho)
        [ancho * 0.5, ancho * 2.0], # fy
        [ancho * 0.4, ancho * 0.6], # cx (Cerca del centro geométrico)
        [alto * 0.4,  alto * 0.6],  # cy
        [-1.0, 1.0],                # k1 (Distorsión radial 1)
        [-1.0, 1.0],                # k2 (Distorsión radial 2)
        [-0.05, 0.05],              # p1 (Distorsión tangencial muy pequeña)
        [-0.05, 0.05]               # p2
    ]

    # C. INICIALIZACIÓN DE LA POBLACIÓN (Codificación Real)
    print("\nInicializando la población con valores aleatorios continuos...")
    poblacion = []
    for _ in range(TAMANO_POBLACION):
        cromosoma = [random.uniform(lim[0], lim[1]) for lim in limites]
        poblacion.append(cromosoma)

    mejor_global = None

    # D. BUCLE GENERACIONAL
    print("\n--- INICIANDO OPTIMIZACIÓN EVOLUTIVA ---")
    for gen in range(GENERACIONES):
        
        # 1. EVALUACIÓN DE APTITUD
        datos_poblacion = []
        suma_aptitud = 0.0
        
        for cromosoma in poblacion:
            aptitud = evaluar_error_reproyeccion(cromosoma, objpoints, imgpoints)
            datos_poblacion.append({
                "bits": cromosoma, # Aunque se llame 'bits' en tus dicts, aquí guardamos los floats
                "aptitud": aptitud
            })
            suma_aptitud += aptitud
            
        # Calcular probabilidad (Necesario para tus métodos de selección)
        for ind in datos_poblacion:
            ind["probabilidad"] = ind["aptitud"] / suma_aptitud if suma_aptitud > 0 else 0

        # Guardar al mejor de la generación actual
        mejor_gen = max(datos_poblacion, key=lambda x: x["aptitud"])
        if mejor_global is None or mejor_gen["aptitud"] > mejor_global["aptitud"]:
            mejor_global = mejor_gen
            
        rmse_actual = (1.0 / mejor_gen['aptitud']) - 1.0
        print(f"Generación {gen+1:03d} | Mejor Aptitud: {mejor_gen['aptitud']:.6f} | RMSE Reproyección: {rmse_actual:.4f} px")

        # 2. SELECCIÓN (Usando tu módulo)
        num_padres = int(TAMANO_POBLACION / 2)
        # Seleccionamos mediante torneo
        padres = op.SELECCION["torneo"](datos_poblacion, num_padres)

        # 3. CRUZA (Usando vectores reales de tu módulo)
        siguiente_generacion = []
        for i in range(num_padres):
            p1 = padres[i]["bits"].copy()
            p2 = padres[(i + 1) % num_padres]["bits"].copy()
            
            # Cruza Aritmética Continua
            h1, h2 = op.CRUZA["aritmetica_real"](p1, p2, n_bits=8, alpha=0.4)
            siguiente_generacion.extend([h1, h2])

        # 4. MUTACIÓN (Usando ruido gaussiano de tu módulo)
        for i in range(len(siguiente_generacion)):
            if random.random() < PROB_MUTACION:
                # Utilizamos la mutación gaussiana (le suma un ruido al gen seleccionado)
                siguiente_generacion[i] = op.MUTACION["gaussiana"](siguiente_generacion[i], media=0.0, desviacion=0.05)

        # 5. REEMPLAZO
        poblacion = siguiente_generacion

    # E. RESULTADOS FINALES
    rmse_final = (1.0 / mejor_global['aptitud']) - 1.0
    print("\n=======================================================")
    print("CALIBRACIÓN FINALIZADA - MEJOR PARÁMETRO ENCONTRADO")
    print("=======================================================")
    print(f"RMSE Final    : {rmse_final:.4f} píxeles")
    
    m_f = mejor_global['bits']
    print("\nMatriz Intrínseca (K):")
    print(f"fx: {m_f[0]:.2f}  | cx: {m_f[2]:.2f}")
    print(f"          | fy: {m_f[1]:.2f}  | cy: {m_f[3]:.2f}")
    
    print("\nCoeficientes de Distorsión (D):")
    print(f"k1: {m_f[4]:.5f} | k2: {m_f[5]:.5f} | p1: {m_f[6]:.5f} | p2: {m_f[7]:.5f}")
    print("=======================================================")

if __name__ == "__main__":
    main()