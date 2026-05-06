import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

rotation = 0.0
# Variables globales para la cámara
camera_pos = [4.0, 3.0, 8.0]  # Posición de la cámara
camera_target = [0.0, 1.0, 0.0]  # Punto al que mira
camera_up = [0.0, 1.0, 0.0]  # Vector hacia arriba

# Variables para el movimiento
camera_speed = 0.2  # Velocidad de movimiento
keys = {}  # Diccionario para controlar el estado de las teclas



def draw_sphere(radius, slices=30, stacks=30):
    """Dibuja una esfera usando primitivas OpenGL (sin GLUT)"""
    for i in range(stacks):
        lat1 = math.pi * (-0.5 + i / stacks)
        lat2 = math.pi * (-0.5 + (i + 1) / stacks)
        
        glBegin(GL_QUAD_STRIP)
        for j in range(slices + 1):
            lng = 2 * math.pi * j / slices
            x1 = math.cos(lat1) * math.cos(lng)
            y1 = math.sin(lat1)
            z1 = math.cos(lat1) * math.sin(lng)
            x2 = math.cos(lat2) * math.cos(lng)
            y2 = math.sin(lat2)
            z2 = math.cos(lat2) * math.sin(lng)
            
            glNormal3f(x1, y1, z1)
            glVertex3f(x1 * radius, y1 * radius, z1 * radius)
            
            glNormal3f(x2, y2, z2)
            glVertex3f(x2 * radius, y2 * radius, z2 * radius)
        glEnd()


def process_input():
    """Procesa el estado de las teclas para mover la cámara"""
    global camera_pos

    if keys.get(glfw.KEY_W, False):  # Mover hacia adelante
        camera_pos[2] -= camera_speed
    if keys.get(glfw.KEY_S, False):  # Mover hacia atrás
        camera_pos[2] += camera_speed
    if keys.get(glfw.KEY_A, False):  # Mover a la izquierda
        camera_pos[0] -= camera_speed
    if keys.get(glfw.KEY_D, False):  # Mover a la derecha
        camera_pos[0] += camera_speed
    if keys.get(glfw.KEY_UP, False):  # Subir
        camera_pos[1] += camera_speed
    if keys.get(glfw.KEY_DOWN, False):  # Bajar
        camera_pos[1] -= camera_speed


def key_callback(window, key, scancode, action, mods):
    """Actualiza el estado de las teclas"""
    if action == glfw.PRESS:
        keys[key] = True
    elif action == glfw.RELEASE:
        keys[key] = False


        
def draw_eye():
    """Dibuja dos esferas simples"""
    glPushMatrix()
   
    # Primera esfera (roja) a la izquierda
    glColor3f(0.85, 0.67, 0.65)  # Rojo
    glPushMatrix()
    glTranslatef(0.7, 0, 0)
    draw_sphere(0.54, 30, 30)
    glPopMatrix()

    glColor3f(1, 1, 1)  # Blanco
    glPushMatrix()
    glTranslatef(0.56, 0, 0)
    draw_sphere(0.6, 30, 30)
    glPopMatrix()
    
    
    # Segunda esfera (azul) a la derecha
    glColor3f(0.84, 0.85, 0.92)  # Azul
    glPushMatrix()
    glTranslatef(0.49, 0, 0)
    draw_sphere(0.55, 30, 30)
    glPopMatrix()

    glColor3f(0, 0, 0)  # Negro
    glPushMatrix()
    glTranslatef(0.3, 0, 0)
    draw_sphere(0.4, 30, 30)
    glPopMatrix()

    glPopMatrix()

def setup_lighting():
    """Configura iluminación básica"""
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    
    light_position = [1.0, 1.0, 1.0, 0.2]
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

def draw_scene():
    """Dibuja la escena completa"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Configuración de la cámara
    gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2],  # Posición de la cámara
              camera_target[0], camera_target[1], camera_target[2],  # Punto al que mira
              camera_up[0], camera_up[1], camera_up[2])  # Vector hacia arriba

    draw_eye()

    glfw.swap_buffers(window)

def init():
    """Configuración inicial de OpenGL"""
    glClearColor(0.5, 0.8, 1.0, 1.0)  # Fondo azul cielo
    glEnable(GL_DEPTH_TEST)           # Activar prueba de profundidad

    # Configuración de la perspectiva
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 1.0, 0.1, 100.0)  # Campo de visión más amplio
    glMatrixMode(GL_MODELVIEW)

    

    
def main():
    global window
    if not glfw.init():
        sys.exit()
    
    # Crear ventana de GLFW
    width, height = 800, 600
    window = glfw.create_window(width, height, "Mover Escena Completa", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()

    # Configurar callback de teclado
    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        #glMatrixMode(GL_PROJECTION)
        #glLoadIdentity()
        #gluPerspective(45, 800/600, 0.1, 100.0)
        
        #glMatrixMode(GL_MODELVIEW)
        #glLoadIdentity()
        #glTranslatef(0, 0, -5)
        
        # Rotar la escena
        #rotation += 0.5
        #glRotatef(rotation, 0, 1, 0)
        #process_input()  # Procesar teclas presionadas
       
        #draw_eye()
        #draw_scene()
        #glfw.swap_buffers(window)
        #glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()