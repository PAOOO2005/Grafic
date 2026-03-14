import cv2
import numpy as np

# espacio de trabajo 500x500 y el color azul oscuro se aplica directamente al crear la matriz
sello = np.full((500, 500, 3), (50, 20, 20), dtype=np.uint8)

# definimos los tonos
AMARILLO = (0, 255, 255)
ROJO = (0, 0, 255)
BLANCO = (255, 255, 255)

# circulo amarillo
cv2.circle(sello, (250, 250), 100, AMARILLO, 3)

# rectangulo rojo 
cv2.rectangle(sello, (200, 200), (300, 300), ROJO, -1)

# lineas en X qeu cruzan de esquina a esquina
cv2.line(sello, (0, 0), (500, 500), BLANCO, 2)
cv2.line(sello, (500, 0), (0, 500), BLANCO, 2)

# Almacenamiento y visualizacion
cv2.imwrite("m3_sello_forjado.png", sello)
cv2.imshow("Sistema Biometrico", sello)

cv2.waitKey(0)
cv2.destroyAllWindows()