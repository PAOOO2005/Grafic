import cv2
import numpy as np
import math

# Crear el lienzo de 600x600 con el color base BGR(40, 20, 20)
img = np.zeros((600, 600, 3), dtype=np.uint8)
img[:] = (40, 20, 20)

# Centro del lienzo
centro_x, centro_y = 300, 300

# 1. Dibujar círculo exterior amarillo (radio 170, grosor 3)
cv2.circle(img, (centro_x, centro_y), 170, (0, 255, 255), 3)

# 2. Dibujar círculo interior amarillo (radio 110, grosor 2)
cv2.circle(img, (centro_x, centro_y), 110, (0, 255, 255), 2)

# 3. Dibujar rectángulo rojo relleno (-1 o cv2.FILLED indica que es sólido)
cv2.rectangle(img, (250, 260), (350, 340), (0, 0, 255), -1)

# 4. Dibujar las 2 diagonales blancas (X) de esquina a esquina
cv2.line(img, (0, 0), (600, 600), (255, 255, 255), 2)
cv2.line(img, (0, 600), (600, 0), (255, 255, 255), 2)

# 5. Colocar 8 círculos verdes alrededor del centro a distancia 140
distancia = 140
radio_verde = 8
color_verde = (0, 255, 0)

for i in range(8):
    # Calcular el ángulo para cada uno de los 8 puntos (360 grados / 8 = 45 grados o pi/4 radianes)
    angulo = i * (2 * math.pi / 8)
    
    # Calcular las coordenadas x e y usando seno y coseno
    x = int(centro_x + distancia * math.cos(angulo))
    y = int(centro_y + distancia * math.sin(angulo))
    
    # Dibujar el círculo verde relleno (-1)
    cv2.circle(img, (x, y), radio_verde, color_verde, -1)

# 6. Escribir el texto "SECTOR-9" en la parte baja (centrado aprox)
texto = "SECTOR-9"
fuente = cv2.FONT_HERSHEY_SIMPLEX
escala = 1
color_blanco = (255, 255, 255)
grosor_texto = 2

# Calculamos el tamaño del texto para que quede perfectamente centrado en x
tamaño_texto = cv2.getTextSize(texto, fuente, escala, grosor_texto)[0]
texto_x = centro_x - (tamaño_texto[0] // 2)
texto_y = 560

cv2.putText(img, texto, (texto_x, texto_y), fuente, escala, color_blanco, grosor_texto, cv2.LINE_AA)

# 7. Guardar como m3_sello_forjado_v2.png
cv2.imwrite('m3_sello_forjado_v2.png', img)

# Opcional: Mostrar la imagen en pantalla para revisar que todo esté bien
cv2.imshow('Sello Biometrico II', img)
cv2.waitKey(0)
cv2.destroyAllWindows()