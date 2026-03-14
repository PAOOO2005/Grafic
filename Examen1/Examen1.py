import cv2
import numpy as np

img = cv2.imread('C:\\Users\\adria\\Desktop\\entorno\\TareasGrafi\\Examen1\\m1_oscura.png', cv2.IMREAD_GRAYSCALE)
# --- MODO RAW ---
h, w = img.shape
img_raw = np.zeros((h, w), dtype=np.uint8)
# Recorre con un for y multiplica por 50
for i in range(h):
    for j in range(w):
        img_raw[i, j] = np.clip(int(img[i, j]) * 50, 0, 255)
# --- MODO OPENCV ---
# Usa la magia de la vectorización 
img_opencv = cv2.multiply(img, 50)

cv2.imshow('Mensaje Raw', img_raw)
cv2.imshow('Mensaje OpenCV', img_opencv)
cv2.waitKey(0)
cv2.destroyAllWindows()