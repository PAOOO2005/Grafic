import cv2
import numpy as np

# Cargamos los pedazos del QR
parte1 = cv2.imread("C:\\Users\\adria\\Desktop\\entorno\\TareasGrafi\\Examen2\\m2_mitad1.png")
parte2 = cv2.imread("C:\\Users\\adria\\Desktop\\entorno\\TareasGrafi\\Examen2\\m2_mitad2.png")

# Creamos el fondo blanco de 400x400 como pide el profe
fondo = np.full((400, 400, 3), 255, dtype=np.uint8)

# --- 1. ACOMODAR LA MITAD SUPERIOR ---
# Matriz para mover la pieza de arriba y dejarla en su lugar (origen)
matriz_arriba = np.float32([[1, 0, -80], [0, 1, 0]])
mitad1_lista = cv2.warpAffine(parte1, matriz_arriba, (400, 400))

# --- 2. ENDEREZAR Y ACOMODAR LA MITAD INFERIOR ---
alto, ancho = parte2.shape[:2]
centro_pieza = (ancho // 2, alto // 2)

# Matriz para quitarle la rotación de 180 grados
matriz_giro = cv2.getRotationMatrix2D(centro_pieza, 180, 1.0)
mitad2_derecha = cv2.warpAffine(parte2, matriz_giro, (ancho, alto))

# Matriz para mandar la pieza ya derecha a la parte de abajo del lienzo
matriz_abajo = np.float32([[1, 0, 80], [0, 1, 200]])
mitad2_lista = cv2.warpAffine(mitad2_derecha, matriz_abajo, (400, 400))

# --- 3. ENSAMBLAR EL QR ---
# Juntamos las dos partes usando cv2.add para que se fusionen en el fondo
qr_armado = cv2.add(mitad1_lista, mitad2_lista)

# Guardamos el resultado con el nombre exacto que nos pidieron
cv2.imwrite("m2_qr_reconstruido.png", qr_armado)

# Mostramos cómo quedó en pantalla
cv2.imshow("QR Reconstruido", qr_armado)
cv2.waitKey(0)
cv2.destroyAllWindows()