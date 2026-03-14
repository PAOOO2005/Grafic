import cv2
import numpy as np
import math

# el lienzo negro que pide la mision
cuadro = np.zeros((500, 500, 3), dtype=np.uint8)

#Empezamos el tiempo en 0
tiempo = 0

#corremos el bucle hasta llegar a 2pi (6.28)
while tiempo <= 6.28:
    
    # Aplicamos las formulas de las pistas para sacar las coordenadas
    # El 250 es para que quede en el centro del cuadro de 500
    pos_x = int(250 + 150 * math.sin(3 * tiempo))
    pos_y = int(250 + 150 * math.sin(2 * tiempo))

    # Dibujamos el punto blanco en la coordenada que salio
    cv2.circle(cuadro, (pos_x, pos_y), 1, (255, 255, 255), -1)

    # Vamos avanzando de poquito en poquito
    tiempo += 0.01

# Mostramos el dibujo de la antena
cv2.imshow("Antena Calibrada", cuadro)
cv2.waitKey(0)
cv2.destroyAllWindows()