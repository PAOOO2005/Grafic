import cv2
import numpy as np

# 1. Cargar la imagen con ruido
img = cv2.imread("C:\\Users\\adria\\Desktop\\entorno\\TareasGrafi\\Examen2\\m4_ruido 1.png")

if img is None:
    print("Error: No se pudo encontrar la imagen 'm4_ruido.png'. Asegúrate de que esté en la misma carpeta.")
else:
    # 2. Definir kernel promedio 3x3 (float32) y normalizar dividiendo entre 9
    kernel = np.ones((3, 3), dtype=np.float32) / 9.0
    
    # Aplicar la convolución usando cv2.filter2D (-1 mantiene la misma profundidad que la imagen original)
    img_suavizada = cv2.filter2D(img, -1, kernel)
    
    # 3. Guardar la imagen suavizada (Opcional)
    cv2.imwrite("m4_suavizada.png", img_suavizada)
    
    # 4. Convertir la imagen suavizada a espacio de color HSV
    img_hsv = cv2.cvtColor(img_suavizada, cv2.COLOR_BGR2HSV)
    
    # 5. Definir límites low y high para el color Cyan (Cian)
    # Hue en OpenCV va de 0 a 180. El cian está en ~90.
    low_cyan = np.array([70, 50, 50])
    high_cyan = np.array([110, 255, 255])
    
    # 6. Crear la máscara binaria con cv2.inRange
    mask_cyan = cv2.inRange(img_hsv, low_cyan, high_cyan)
    
    # 7. Guardar la máscara resultante
    cv2.imwrite("m4_mask_cyan.png", mask_cyan)
    
    print("¡Misión 4 completada con éxito!")
    print("Se han guardado 'm4_suavizada.png' y 'm4_mask_cyan.png'")

    # Opcional: Mostrar los resultados en pantalla para verificar la limpieza
    cv2.imshow("Original con Ruido", img)
    cv2.imshow("Suavizada (Filtro 3x3)", img_suavizada)
    cv2.imshow("Mascara Cyan Limpia", mask_cyan)
    cv2.waitKey(0)
    cv2.destroyAllWindows()