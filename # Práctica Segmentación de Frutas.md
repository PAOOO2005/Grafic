# Práctica: Segmentación de Frutas usando Máscara HSV
**Nombre:** Paola [Tu Apellido]  
**Grupo:** [Tu Grupo]  

## 1. Objetivo
[cite_start]Aplicar el modelo de color HSV para segmentar objetos y analizar los resultados directamente sobre una máscara binaria[cite: 2].

## 2. Desarrollo (Capturas de Pantalla)

### Color Verde (Ya lo tienes)
* ![Original](ruta/a/tu/imagen_original.png)
* ![HSV](ruta/a/tu/imagen_hsv.png)
* ![Máscara](ruta/a/tu/mascara_verde.png)

### Color Rojo (Pendiente)
* (Inserta aquí tus capturas)

### Color Amarillo (Pendiente)
* (Inserta aquí tus capturas)

## 3. Tabla Comparativa
| Color | Número Detectado | Observaciones |
| :--- | :--- | :--- |
| Verde | [Número] | [Ej: Se segmentó fácil pero quedó ruido pequeño] |
| Rojo | [Número] | [Ej: El rojo fue difícil por estar en dos rangos] |
| Amarillo | [Número] | [Ej: Se confundía un poco con la iluminación] |

## 4. Respuestas al Análisis Crítico
1. [cite_start]**¿Por qué HSV es mejor que RGB?** Porque separa la información del color (croma) de la iluminación (brillo), lo que lo hace más robusto a sombras[cite: 17, 18].
2. [cite_start]**¿Cómo afecta la luz al canal V?** El canal V representa el valor/brillo; si hay mucha luz, el valor sube, y si hay sombras, baja, lo que puede "romper" la máscara si el rango es muy estrecho[cite: 18].
3. [cite_start]**¿Qué sucede si dos frutas tienen tonos similares?** La máscara podría unirlas en una sola región conectada, falseando el conteo[cite: 18].
4. [cite_start]**¿Limitaciones?** Depende totalmente de que el color sea distinto al fondo y es sensible a cambios bruscos de iluminación[cite: 19].

## 5. Conclusión
(Aquí debes redactar media cuartilla sobre lo que aprendiste de la limpieza de ruido y la segmentación) [cite_start][cite: 20, 23].