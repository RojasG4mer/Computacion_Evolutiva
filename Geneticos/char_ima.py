import cv2

# La misma configuración exacta de tu main.py
cuadros_x, cuadros_y = 5, 7
tamano_cuadro = 0.04      # Estos valores de tamaño físico no afectan la imagen digital,
tamano_marcador = 0.02    # pero OpenCV los pide para construir el objeto lógico.

diccionario = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
tablero = cv2.aruco.CharucoBoard((cuadros_x, cuadros_y), tamano_cuadro, tamano_marcador, diccionario)

# Calculamos una resolución alta (ej. 300 pixeles por cada cuadro) para que se vea nítida
ancho_img = cuadros_x * 300
alto_img = cuadros_y * 300

# Generamos la imagen del tablero
imagen_tablero = tablero.generateImage((ancho_img, alto_img))

# Guardamos la imagen en alta calidad
nombre_archivo = "Tablero_ChArUco_5x7.png"
cv2.imwrite(nombre_archivo, imagen_tablero)

print(f"¡Éxito! El patrón se ha guardado como '{nombre_archivo}'")