import cv2
import numpy as np
import math

# --- Funcion de proyeccion isometrica --
def iso_transform(x, y, z=0):
    angle_x = math.radians(30)
    angle_y = math.radians(30)
    iso_x = (x - y) * math.cos(angle_x)
    iso_y = (x + y) * math.sin(angle_y) - z
    return int(iso_x + 300), int(iso_y + 300)

# Crear lienzo en blanco
canvas = np.ones((600, 600, 3), dtype=np.uint8) * 255

# --- Cuerpo de la casa (Cubo) ---
# Base en el suelo (z=0)
base = [iso_transform(0,0,0), iso_transform(100,0,0),
        iso_transform(100,100,0), iso_transform(0,100,0)]
# Parte superior de las paredes (z=100)
techo_base = [iso_transform(0,0,100), iso_transform(100,0,100),
              iso_transform(100,100,100), iso_transform(0,100,100)]

# Dibujar base y bordes superiores
cv2.polylines(canvas, [np.array(base)], True, (0,0,0), 2)
cv2.polylines(canvas, [np.array(techo_base)], True, (0,0,0), 2)

# Unir esquinas de paredes verticales
for i in range(4):
    cv2.line(canvas, base[i], techo_base[i], (0,0,0), 2)

# --- Techo a dos aguas --
punta_frontal = iso_transform(50, 0, 150)
punta_trasera = iso_transform(50, 100, 150)

# Linea superior del techo
cv2.line(canvas, punta_frontal, punta_trasera, (0,0,0), 2)

# Unir la cumbrera con las esquinas de las paredes
cv2.line(canvas, techo_base[0], punta_frontal, (0,0,0), 2)
cv2.line(canvas, techo_base[1], punta_frontal, (0,0,0), 2)
cv2.line(canvas, techo_base[2], punta_trasera, (0,0,0), 2)
cv2.line(canvas, techo_base[3], punta_trasera, (0,0,0), 2)

# --Puerta ---
puerta = [iso_transform(35,0,0), iso_transform(65,0,0),
          iso_transform(65,0,60), iso_transform(35,0,60)]
cv2.polylines(canvas, [np.array(puerta)], True, (0,0,0), 2)

# Mostrar resultado
cv2.imshow("Casita Isometrica de Pao :)", canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()