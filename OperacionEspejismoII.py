import cv2
import numpy as np

img = cv2.imread("C:\\Users\\adria\\Desktop\\entorno\\TareasGrafi\\m1_oscura 1.png", cv2.IMREAD_GRAYSCALE)

# MODO RAW (Ciclos Anidados)
# Este metodo es educativo para entender como se procesa cada pixel
h, w = img.shape
img_raw = np.zeros((h, w), dtype=np.uint8)

for i in range(h):
    for j in range(w):
        # Aplicamos el operador inverso (Multiplicacion por 50)
        nuevo_valor = int(img[i, j]) * 50
        
        # Clipping manual: Si supera 255, se queda en 255 (blanco total)
        if nuevo_valor > 255:
            nuevo_valor = 255
            
        img_raw[i, j] = nuevo_valor

# MODO OPENCV / NUMPY (Vectorizado)
# Opcion A: Usando NumPy con clip
img_numpy = np.clip(img.astype(np.uint16) * 50, 0, 255).astype(np.uint8)

# Opcion B: Usando OpenCV (el metodo mas directo)
img_opencv = cv2.multiply(img, 50)

#  RESULTADOS 
cv2.imshow('Mensaje Original (Oscuro)', img)
cv2.imshow('Recuperado - Modo Raw', img_raw)
cv2.imshow('Recuperado - Modo OpenCV', img_opencv)

print("Misoón completada. Pixeles restaurados.")
cv2.waitKey(0)
cv2.destroyAllWindows()