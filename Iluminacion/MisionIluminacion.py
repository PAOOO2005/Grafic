import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

rotation = 0.0

def draw_sphere(radius, slices=30, stacks=30):
    """Dibuja una esfera. GLU genera las normales automáticamente."""
    quad = gluNewQuadric()
    # Importante: Generar normales para que la luz funcione
    gluQuadricNormals(quad, GLU_SMOOTH) 
    gluSphere(quad, radius, slices, stacks)
    gluDeleteQuadric(quad)

def set_material(r, g, b, shininess=50):
    """
    Configura el material del objeto actual.
    Sustituye al glColor3f cuando el GL_LIGHTING está activo.
    """
    color = [r, g, b, 1.0]
    specular = [1.0, 1.0, 1.0, 1.0] # Brillo blanco
    
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, color)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specular)
    glMaterialf(GL_FRONT, GL_SHININESS, shininess)

def draw_eye():
    glPushMatrix()
    
    # 1. Piel
    set_material(0.85, 0.67, 0.65, 10)
    glPushMatrix()
    glTranslatef(0.7, 0, 0)
    draw_sphere(0.54)
    glPopMatrix()
    
    # 2. Blanco del ojo
    set_material(1.0, 1.0, 1.0, 80)
    glPushMatrix()
    glTranslatef(0.56, 0, 0)
    draw_sphere(0.6)
    glPopMatrix()
    
    # 3. Iris
    set_material(0.4, 0.5, 0.9, 100) # Azulado
    glPushMatrix()
    glTranslatef(0.49, 0, 0)
    draw_sphere(0.55)
    glPopMatrix()
    
    # 4. Pupila
    set_material(0.05, 0.05, 0.05, 120)
    glPushMatrix()
    glTranslatef(0.3, 0, 0)
    draw_sphere(0.4)
    glPopMatrix()
    
    glPopMatrix()

def setup_lighting():
    """Configuración total de la Misión 1"""
    # Activar el motor de iluminación
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST) # Para que las esferas no se traslapen mal
    glShadeModel(GL_SMOOTH) # Sombreado suave

    # Propiedades de la Luz 0
    ambient = [0.2, 0.2, 0.2, 1.0]  # Luz ambiental tenue
    diffuse = [1.0, 1.0, 1.0, 1.0]  # Luz direccional fuerte (blanca)
    specular = [1.0, 1.0, 1.0, 1.0] # Brillo intenso
    light_pos = [2.0, 2.0, 5.0, 1.0] # Posicional (w=1.0) desde arriba/derecha

    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)

def main():
    global rotation
    if not glfw.init():
        return
    
    window = glfw.create_window(800, 600, "Misión 1: Ojo Iluminado - Maria", None, None)
    if not window:
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    glClearColor(0.1, 0.1, 0.15, 1.0) # Fondo oscuro para resaltar la luz
    
    setup_lighting()
    
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 800/600, 0.1, 100.0)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # Cámara
        glTranslatef(0, 0, -5)
        
        # Animación
        rotation += 0.10
        glRotatef(rotation, 0, 1, 0)
        
        # Dibujo
        draw_eye()
        
        glfw.swap_buffers(window)
        glfw.poll_events()
        
    glfw.terminate()

if __name__ == "__main__":
    main()