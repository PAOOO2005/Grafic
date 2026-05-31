import sys
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

# Variables globales para el control de la animación y el estado de la luz
rotation = 0.0
light_mode = 0  # Modos: 0=Básica, 1=Múltiple, 2=Direccional, 3=Spotlight, 4=Colores

def draw_two_spheres():
    """
    Dibuja un modelo jerárquico compuesto por varias esferas 
    que simulan la estructura de un ojo humano.
    """
    glPushMatrix()
    
    # --- Esclerótica (La parte blanca del ojo) ---
    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()
    glTranslatef(0.56, 0, 0)
    glutSolidSphere(0.6, 40, 40) # Radio 0.6, 40 subdivisiones para suavidad
    glPopMatrix()
    
    # --- Iris (Capa azul grisácea) ---
    glColor3f(0.84, 0.85, 0.92)
    glPushMatrix()
    glTranslatef(0.49, 0, 0)
    glutSolidSphere(0.55, 35, 35)
    glPopMatrix()
    
    # --- Detalle del Iris (Parte rosada/transición) ---
    glColor3f(0.85, 0.67, 0.65)
    glPushMatrix()
    glTranslatef(0.7, 0, 0)
    glutSolidSphere(0.54, 35, 35)
    glPopMatrix()

    # --- Pupila (El centro negro) ---
    glColor3f(0.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(0.3, 0, 0)
    glutSolidSphere(0.4, 30, 30)
    glPopMatrix()
    
    glPopMatrix()

# =========================================================
# CONFIGURACIONES DE ILUMINACIÓN (Pipeline Fijo de OpenGL)
# =========================================================

def setup_lighting_basic():
    """Configuración estándar con una sola fuente de luz puntual."""
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glDisable(GL_LIGHT1)
    glDisable(GL_LIGHT2)
    
    light_position = [3.0, 2.0, 3.0, 1.0] # El último valor 1.0 indica luz puntual
    light_diffuse = [1.0, 1.0, 1.0, 1.0]  # Luz blanca pura
    light_ambient = [0.3, 0.3, 0.3, 1.0]  # Luz de relleno para evitar sombras negras
    
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)

def setup_lighting_multiple():
    """Activa tres fuentes de luz distintas para iluminar varios ángulos."""
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0); glEnable(GL_LIGHT1); glEnable(GL_LIGHT2)
    
    # Luz Principal (Blanca)
    glLightfv(GL_LIGHT0, GL_POSITION, [3.0, 4.0, 3.0, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    
    # Luz de Relleno (Azulada)
    glLightfv(GL_LIGHT1, GL_POSITION, [-2.0, 1.0, -3.0, 1.0])
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.3, 0.4, 0.6, 1.0])
    
    # Luz de Contraste (Cálida)
    glLightfv(GL_LIGHT2, GL_POSITION, [4.0, 0.0, 1.0, 1.0])
    glLightfv(GL_LIGHT2, GL_DIFFUSE, [0.9, 0.6, 0.3, 1.0])

def setup_lighting_directional():
    """Simula una fuente de luz infinitamente lejana (como el sol)."""
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glDisable(GL_LIGHT1); glDisable(GL_LIGHT2)
    
    # El valor W=0.0 en la posición convierte la coordenada en un VECTOR de dirección
    light_direction = [1.0, -1.0, 1.0, 0.0] 
    glLightfv(GL_LIGHT0, GL_POSITION, light_direction)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 0.95, 0.8, 1.0]) # Tono cálido

def setup_lighting_spotlight():
    """Configura una luz cónica con dirección y apertura definida."""
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    
    light_position = [0.0, 4.0, 2.0, 1.0]
    spot_direction = [0.0, -1.0, -0.5]
    
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, spot_direction)
    glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 30.0)    # Ángulo de apertura del cono
    glLightf(GL_LIGHT0, GL_SPOT_EXPONENT, 20.0)  # Concentración de la luz en el centro

def setup_lighting_colored():
    """Usa tres luces de colores primarios (RGB) en distintas posiciones."""
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0); glEnable(GL_LIGHT1); glEnable(GL_LIGHT2)
    
    glLightfv(GL_LIGHT0, GL_POSITION, [-3.0, 1.0, 2.0, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 0.2, 0.2, 1.0]) # Rojo
    
    glLightfv(GL_LIGHT1, GL_POSITION, [3.0, 1.0, 2.0, 1.0])
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.2, 1.0, 0.3, 1.0]) # Verde
    
    glLightfv(GL_LIGHT2, GL_POSITION, [0.0, 3.0, 0.0, 1.0])
    glLightfv(GL_LIGHT2, GL_DIFFUSE, [0.3, 0.3, 1.0, 1.0]) # Azul

def setup_lighting():
    """Selector maestro para aplicar el modo de iluminación actual."""
    glEnable(GL_DEPTH_TEST)      # Activa el búfer de profundidad (Z-buffer)
    glEnable(GL_COLOR_MATERIAL)  # Permite que glColor afecte a los materiales
    
    if light_mode == 0: setup_lighting_basic()
    elif light_mode == 1: setup_lighting_multiple()
    elif light_mode == 2: setup_lighting_directional()
    elif light_mode == 3: setup_lighting_spotlight()
    elif light_mode == 4: setup_lighting_colored()

def draw_light_indicators():
    """
    Dibuja representaciones visuales (esferas de alambre) para saber
    dónde están ubicadas las fuentes de luz físicamente.
    """
    glDisable(GL_LIGHTING) # Desactivamos luz para que el indicador brille con su propio color
    glColor3f(1.0, 1.0, 0.0)
    
    if light_mode == 0:
        glPushMatrix(); glTranslatef(3.0, 2.0, 3.0); glutWireSphere(0.1, 8, 8); glPopMatrix()
    elif light_mode == 1:
        glPushMatrix(); glTranslatef(3.0, 4.0, 3.0); glutWireSphere(0.1, 8, 8); glPopMatrix()
        glPushMatrix(); glTranslatef(-2.0, 1.0, -3.0); glutWireSphere(0.1, 8, 8); glPopMatrix()
    elif light_mode == 4:
        # Indicadores con colores correspondientes a la luz que emiten
        glColor3f(1, 0, 0); glPushMatrix(); glTranslatef(-3.0, 1.0, 2.0); glutWireSphere(0.1, 8, 8); glPopMatrix()
        glColor3f(0, 1, 0); glPushMatrix(); glTranslatef(3.0, 1.0, 2.0); glutWireSphere(0.1, 8, 8); glPopMatrix()
        glColor3f(0, 0, 1); glPushMatrix(); glTranslatef(0.0, 3.0, 0.0); glutWireSphere(0.1, 8, 8); glPopMatrix()
    
    glEnable(GL_LIGHTING)

def key_callback(window, key, scancode, action, mods):
    """Maneja las entradas de teclado para cambiar entre los modos de luz."""
    global light_mode
    if action == glfw.PRESS:
        if glfw.KEY_0 <= key <= glfw.KEY_4:
            light_mode = key - glfw.KEY_0
            print(f"Cambio a Modo de Luz: {light_mode}")
            setup_lighting()

def main():
    global rotation
    
    # Inicialización del entorno de ventana
    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "Tipos de Iluminación OpenGL", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    # Inicializar GLUT (necesario para las esferas sólidas y de alambre)
    glutInit(sys.argv)

    # Configuración de estado inicial de OpenGL
    glClearColor(0.1, 0.1, 0.1, 1.0) # Gris muy oscuro
    setup_lighting()
    
    # Propiedades de material globales (brillo especular)
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 100.0)

    print("Controles: Teclas 0, 1, 2, 3, 4 para cambiar modos de iluminación.")

    # Bucle principal de renderizado
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Configurar Cámara/Proyección
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 800/600, 0.1, 100.0)
        
        # Configurar Transformaciones del Modelo
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0, 0, -5) # Alejar la escena para verla completa
        
        # Rotación automática
        rotation += 0.5
        glRotatef(rotation, 0, 1, 0)
        glRotatef(20, 1, 0, 0)
        
        # Dibujo de elementos
        draw_two_spheres()
        draw_light_indicators()
        
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()