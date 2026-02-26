import cv2 as cv
import numpy as np 

# Creamos un lienzo de 500x500 con 3 canales (RGB) para tener colores
img = np.ones((500, 500, 3), np.uint8) * 255 

# --- Partes del Oso ---
# Orejas
cv.circle(img, (180, 150), 60, (0, 0, 0), -1)  # Oreja Izq
cv.circle(img, (320, 150), 60, (0, 0, 0), -1)  # Oreja Der

# Cabeza (Círculo principal)
cv.circle(img, (250, 220), 108, (203, 192, 255), -1) # Color rosa claro
cv.circle(img, (250, 220), 108, (0, 0, 0), 2)       # Contorno

# Hocico
cv.circle(img, (250, 260), 50, (255, 255, 255), -1)
cv.circle(img, (250, 250), 25, (0, 0, 0), -1)       # Nariz

# Ojos
cv.circle(img, (215, 200), 12, (0, 0, 0), -1)       # Ojo Izq
cv.circle(img, (285, 200), 12, (0, 0, 0), -1)       # Ojo Der

# Cuerpo (Rectángulo redondeado o base)
#cv.rectangle(img, (180, 320), (320, 450), (203, 192, 255), -1)
#cv.rectangle(img, (180, 320), (320, 450), (0, 0, 0), 2)
#cuerpo (circulo)
cv.circle(img, (250, 415), 90, (203, 192, 255), -1)
cv.circle(img, (250, 415), 90, (0, 0, 0), 2)
cv.imshow('Oso', img)
cv.waitKey(0)
cv.destroyAllWindows()