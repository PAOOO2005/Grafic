import cv2
import numpy as np

m1 = cv2.imread('C:\\Users\\adria\\Desktop\\entorno\\TareasGrafi\Examen1\\m2_mitad1.png')
m2 = cv2.imread('C:\\Users\\adria\\Desktop\\entorno\\TareasGrafi\\Examen1\\m2_mitad2.png')


output = np.zeros((400, 400, 3), dtype=np.uint8)

# Transformamos lo de arriba 
t_sup = np.float32([[1, 0, -80], [0, 1, 0]])
upper_part = cv2.warpAffine(m1, t_sup, (400, 400))

# rotamos y ubicamos bien para qeu funcione 
h, w = m2.shape[:2]
r_mat = cv2.getRotationMatrix2D((w // 2, h // 2), 180, 1.0)
m2_rotated = cv2.warpAffine(m2, r_mat, (w, h))

#posicionamos en la parte de abajo 
t_inf = np.float32([[1, 0, 80], [0, 1, 200]])
lower_part = cv2.warpAffine(m2_rotated, t_inf, (400, 400))

# juntamso todoo
final_qr = cv2.add(upper_part, lower_part)

#ya todo junto
cv2.imshow("QR Final", final_qr)
cv2.waitKey(0)
cv2.destroyAllWindows()
