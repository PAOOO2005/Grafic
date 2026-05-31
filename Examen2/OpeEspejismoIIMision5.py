import cv2
import numpy as np

# ==========================================
# 1. GENERACIÓN DEL MENSAJE (m5_tricolor.png)
# ==========================================

# Crear imagen de 300x700 con ruido aleatorio en BGR (valores entre 0 y 255)
# Nota: La estructura de tamaño en numpy es (alto, ancho, canales) -> (300, 700, 3)
img_ruido = np.random.randint(0, 256, (300, 700, 3), dtype=np.uint8)

# Configuración del texto "tramposo"
texto_secreto = "S1ST3M4S-ITM"
fuente = cv2.FONT_HERSHEY_SIMPLEX
escala = 1.8
grosor = 5

# Calcular coordenadas para centrar el texto
tamaño_texto = cv2.getTextSize(texto_secreto, fuente, escala, grosor)[0]
x_texto = (700 - tamaño_texto[0]) // 2
y_texto = (300 + tamaño_texto[1]) // 2

# TINTA TRAMPOSA: Usaremos un color donde G = 255, B = 0, R = 128
# Al ojo humano se verá como un verde/oliva mezclado con el ruido, 
# pero la diferencia matemática entre G y B será enorme (255 - 0 = 255).
color_tramposo = (0, 255, 128) # Formato BGR

cv2.putText(img_ruido, texto_secreto, (x_texto, y_texto), fuente, escala, color_tramposo, grosor, cv2.LINE_AA)

# Guardar la evidencia generada
cv2.imwrite("m5_tricolor.png", img_ruido)
print("¡Imagen 'm5_tricolor.png' generada con el mensaje oculto!")


# ==========================================
# 2. RECUPERACIÓN DEL MENSAJE
# ==========================================

# Volvemos a cargar la imagen para simular la intercepción
img = cv2.imread("m5_tricolor.png")

# Separar los canales B, G, R
b, g, r = cv2.split(img)

# Probar la combinación matemática: Valor absoluto de la diferencia entre G y B
# Como en el texto G=255 y B=0, la diferencia será 255 (Blanco puro)
combinacion_gb = cv2.absdiff(g, b)

# Para asegurar que el texto sea perfectamente legible y contrastado,
# aplicamos una umbralización (Thresholding). En este caso, el método de Otsu
# calculará automáticamente el mejor umbral para separar el texto del fondo.
_, mensaje_umbralizado = cv2.threshold(combinacion_gb, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Guardar el resultado final recuperado
cv2.imwrite("m5_mensaje.png", mensaje_umbralizado)
print("¡Mensaje recuperado con éxito y guardado como 'm5_mensaje.png'!")


# ==========================================
# 3. VISUALIZACIÓN (Opcional)
# ==========================================
cv2.imshow("Canal B (Azul)", b)
cv2.imshow("Canal G (Verde)", g)
cv2.imshow("Diferencia abs(G - B)", combinacion_gb)
cv2.imshow("Mensaje Descifrado (Otsu)", mensaje_umbralizado)

cv2.waitKey(0)
cv2.destroyAllWindows()