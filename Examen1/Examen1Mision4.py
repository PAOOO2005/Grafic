import cv2
import numpy as np

foto_ruidosa = cv2.imread('C:\\Users\\adria\\Desktop\\entorno\\TareasGrafi\Examen1\\m4_ruido.png')

# La pasamos a HSV para que se deje filtrar
color_hsv = cv2.cvtColor(foto_ruidosa, cv2.COLOR_BGR2HSV)

#rango sugerido 
el_bajo = np.array([80, 100, 100])
el_alto = np.array([100, 255, 255])

# filtramos para que solo quede lo que nos sirve
solo_cyan = cv2.inRange(color_hsv, el_bajo, el_alto)

# a ver si ya se ve la clave :)
cv2.imshow("Original con ruido", foto_ruidosa)
cv2.imshow("Clave revelada", solo_cyan)

cv2.waitKey(0)
cv2.destroyAllWindows()