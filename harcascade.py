import cv2 as cv 

# Asegúrate de tener el archivo en esa ruta
rostro = cv.CascadeClassifier('C:\\Users\\adria\\Desktop\\entorno\\TareasGrafi\\haarcascade_frontalface_alt2.xml')
cap = cv.VideoCapture(0)

while True:
    ret, img = cap.read()
    if not ret: break
    
    gris = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gris, 1.3, 5)
    
    for (x, y, w, h) in rostros:
        # --- OJOS (Ya los tenías) ---
        # Blanco de los ojos
        cv.circle(img, (x + int(w*0.3), y + int(h*0.4)), 20, (255, 255, 255), -1)
        cv.circle(img, (x + int(w*0.7), y + int(h*0.4)), 20, (255, 255, 255), -1)
        # Pupilas
        cv.circle(img, (x + int(w*0.3), y + int(h*0.4)), 5, (255, 0, 0), -1)
        cv.circle(img, (x + int(w*0.7), y + int(h*0.4)), 5, (255, 0, 0), -1)

        #NARIz
        # Un pequeño círculo rojo como de payaso
        cv.circle(img, (x + int(w*0.5), y + int(h*0.55)), 12, (203,134 , 255), -1)

        #BOCA
        # Dibujamos una media luna para la sonrisa
        # Los parámetros son: centro, (ancho, alto), rotación, inicio, fin, color, grosor
        cv.ellipse(img, (x + int(w*0.5), y + int(h*0.75)), (int(w*0.5), 20), 0, 0, 180, (0, 0, 0), 10)

        # Tu rectángulo original
        cv.rectangle(img, (x, y), (x + w, y + h), (234, 23, 23), 5)
        
        img2 = img[y:y+h, x:x+w]
        cv.imshow('Recorte', img2)

    cv.imshow('Camara', img)
    
    if cv.waitKey(1) == ord('q'):
        break

cap.release() # No olvides los paréntesis aquí
cv.destroyAllWindows()