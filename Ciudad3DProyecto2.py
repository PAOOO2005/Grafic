import os
import sys
import math
import glfw
import cv2
import numpy as np
import mediapipe as mp
from OpenGL.GL import *
from OpenGL.GLU import *

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
os.environ.setdefault("GLOG_minloglevel", "2")

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hand_landmarker.task")

HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4), (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12), (9, 13), (13, 14), (14, 15),
    (15, 16), (13, 17), (0, 17), (17, 18), (18, 19), (19, 20),
]

# Posición de la cámara
cam_eye_x, cam_eye_y, cam_eye_z = 15.0, 45.0, 75.0
cam_center_x, cam_center_y, cam_center_z = 15.0, 0.0, 10.0

def draw_generic_cube(w, h, d, r, g, b):
    w_h, d_h = w / 2.0, d / 2.0
    glBegin(GL_QUADS)
    glColor3f(r, g, b)
    glVertex3f(-w_h, 0, d_h); glVertex3f(w_h, 0, d_h); glVertex3f(w_h, h, d_h); glVertex3f(-w_h, h, d_h)
    glColor3f(r * 0.8, g * 0.8, b * 0.8)
    glVertex3f(-w_h, 0, -d_h); glVertex3f(w_h, 0, -d_h); glVertex3f(w_h, h, -d_h); glVertex3f(-w_h, h, -d_h)
    glColor3f(r * 0.7, g * 0.7, b * 0.7)
    glVertex3f(-w_h, 0, -d_h); glVertex3f(-w_h, 0, d_h); glVertex3f(-w_h, h, d_h); glVertex3f(-w_h, h, -d_h)
    glVertex3f(w_h, 0, -d_h); glVertex3f(w_h, 0, d_h); glVertex3f(w_h, h, d_h); glVertex3f(w_h, h, -d_h)
    glColor3f(r * 0.9, g * 0.9, b * 0.9)
    glVertex3f(-w_h, h, -d_h); glVertex3f(w_h, h, -d_h); glVertex3f(w_h, h, d_h); glVertex3f(-w_h, h, d_h)
    glEnd()

def draw_pyramid(w, h, d, r, g, b):
    w_h, d_h = w / 2.0, d / 2.0
    glBegin(GL_TRIANGLES)
    glColor3f(r, g, b)
    glVertex3f(-w_h, 0, d_h); glVertex3f(w_h, 0, d_h); glVertex3f(0, h, 0)
    glColor3f(r * 0.8, g * 0.8, b * 0.8)
    glVertex3f(-w_h, 0, -d_h); glVertex3f(w_h, 0, -d_h); glVertex3f(0, h, 0)
    glColor3f(r * 0.7, g * 0.7, b * 0.7)
    glVertex3f(-w_h, 0, -d_h); glVertex3f(-w_h, 0, d_h); glVertex3f(0, h, 0)
    glVertex3f(w_h, 0, -d_h); glVertex3f(w_h, 0, d_h); glVertex3f(0, h, 0)
    glEnd()

def draw_windows(w, h, d, rows, cols):
    w_half, d_half = w / 2.0, d / 2.0
    win_w = w / (cols * 2)
    win_h = h / (rows * 2)
    glColor3f(0.95, 0.95, 0.4) 
    glBegin(GL_QUADS)
    z_f = d_half + 0.01
    for r in range(rows):
        for c in range(cols):
            if (r + c) % 3 == 0: continue 
            x = -w_half + (c * (w / cols)) + win_w / 2
            y = (r * (h / rows)) + win_h / 2
            glVertex3f(x, y, z_f)
            glVertex3f(x + win_w, y, z_f)
            glVertex3f(x + win_w, y + win_h, z_f)
            glVertex3f(x, y + win_h, z_f)
    glEnd()

def draw_detailed_house(w, h, d, r, g, b):
    draw_generic_cube(w, h, d, r, g, b)
    glPushMatrix()
    glTranslatef(0, 0.3, 0)
    draw_windows(w * 0.8, h * 0.6, d, 2, 2)
    glPopMatrix()
    w_h, d_h = (w + 0.2) / 2.0, (d + 0.2) / 2.0
    roof_y = h + 0.8
    glBegin(GL_TRIANGLES)
    glColor3f(0.85, 0.35, 0.1)
    glVertex3f(-w_h, h, d_h); glVertex3f(w_h, h, d_h); glVertex3f(0, roof_y, 0)
    glVertex3f(-w_h, h, -d_h); glVertex3f(w_h, h, -d_h); glVertex3f(0, roof_y, 0)
    glEnd()

def draw_cafe():
    draw_generic_cube(4.0, 2.5, 3.5, 0.75, 0.6, 0.45)
    glBegin(GL_QUADS)
    glColor3f(0.9, 0.9, 0.5)
    glVertex3f(-1.5, 0.5, 1.76); glVertex3f(1.5, 0.5, 1.76); glVertex3f(1.5, 1.8, 1.76); glVertex3f(-1.5, 1.8, 1.76)
    glEnd()
    glPushMatrix()
    glTranslatef(0, 2.3, 0.3)
    draw_generic_cube(4.4, 0.2, 4.0, 0.4, 0.25, 0.15)
    glTranslatef(0, 0.5, 1.6)
    draw_generic_cube(2.0, 0.5, 0.1, 0.9, 0.85, 0.7)
    glPopMatrix()

def draw_traffic_light(is_green):
    # Poste gris oscuro
    draw_generic_cube(0.15, 3.5, 0.15, 0.25, 0.25, 0.25)
    glPushMatrix()
    glTranslatef(0, 3.5, 0)
    # Cuerpo del semáforo
    draw_generic_cube(0.4, 1.0, 0.4, 0.1, 0.1, 0.1)
    
    r_light = 1.0 if not is_green else 0.15
    g_light = 1.0 if is_green else 0.15

    glPushMatrix()
    glTranslatef(0, 0.25, 0.21)
    draw_generic_cube(0.2, 0.2, 0.02, r_light, 0.0, 0.0)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, -0.25, 0.21)
    draw_generic_cube(0.2, 0.2, 0.02, 0.0, g_light, 0.0)
    glPopMatrix()
    glPopMatrix()

def draw_pink_motorcycle():
    glPushMatrix()
    draw_generic_cube(0.25, 0.4, 1.0, 1.0, 0.4, 0.7)
    glPushMatrix()
    glTranslatef(0, -0.05, 0.4)
    draw_generic_cube(0.12, 0.25, 0.25, 0.12, 0.12, 0.12)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0, -0.05, -0.4)
    draw_generic_cube(0.12, 0.25, 0.25, 0.12, 0.12, 0.12)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0, 0.4, 0.1)
    draw_generic_cube(0.2, 0.12, 0.3, 0.2, 0.2, 0.2)
    glPopMatrix()
    glPopMatrix()

def draw_school():
    draw_generic_cube(9.0, 4.5, 4.5, 0.7, 0.7, 0.7)
    glPushMatrix()
    glTranslatef(2.5, 0, 3.0)
    draw_generic_cube(3.0, 4.5, 3.0, 0.65, 0.65, 0.65)
    glPopMatrix()
    draw_windows(8.0, 3.5, 4.5, 2, 4)

def draw_church():
    draw_generic_cube(5.0, 5.5, 8.0, 0.85, 0.82, 0.75)
    glPushMatrix()
    glTranslatef(0, 0, 3.2)
    draw_generic_cube(2.5, 10.0, 2.5, 0.75, 0.72, 0.65)
    glTranslatef(0, 10.0, 0)
    draw_pyramid(2.8, 2.5, 2.8, 0.3, 0.3, 0.35)
    glTranslatef(0, 2.5, 0)
    draw_generic_cube(0.15, 1.0, 0.15, 0.9, 0.8, 0.2)
    glTranslatef(0, 0.3, 0)
    draw_generic_cube(0.6, 0.15, 0.15, 0.9, 0.8, 0.2)
    glPopMatrix()

def draw_small_playground():
    glBegin(GL_QUADS)
    glColor3f(0.35, 0.65, 0.3)
    glVertex3f(-4.5, 0.02, -4.5); glVertex3f(4.5, 0.02, -4.5); glVertex3f(4.5, 0.02, 4.5); glVertex3f(-4.5, 0.02, 4.5)
    glEnd()
    glPushMatrix()
    glTranslatef(-2.0, 0, -1.0)
    draw_generic_cube(0.1, 1.8, 0.1, 0.2, 0.2, 0.2)
    glTranslatef(2.5, 0, 0)
    draw_generic_cube(0.1, 1.8, 0.1, 0.2, 0.2, 0.2)
    glTranslatef(-1.25, 1.8, 0)
    draw_generic_cube(2.7, 0.1, 0.1, 0.2, 0.2, 0.2)
    glTranslatef(0, -1.0, 0)
    draw_generic_cube(0.8, 0.08, 0.3, 0.8, 0.2, 0.2)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(1.8, 0, -1.5)
    draw_generic_cube(0.6, 1.4, 0.6, 0.2, 0.4, 0.8)
    glPushMatrix()
    glTranslatef(0, 0.5, 0.8)
    glRotatef(30, 1, 0, 0)
    draw_generic_cube(0.5, 0.1, 1.6, 0.8, 0.8, 0.8)
    glPopMatrix()
    glPopMatrix()

def draw_kiosk():
    glPushMatrix()
    draw_generic_cube(2.6, 0.5, 2.6, 0.5, 0.35, 0.25)
    for sx in [-1.1, 1.1]:
        for sz in [-1.1, 1.1]:
            glPushMatrix()
            glTranslatef(sx, 0.5, sz)
            draw_generic_cube(0.12, 1.8, 0.12, 0.8, 0.7, 0.5)
            glPopMatrix()
    glTranslatef(0, 2.3, 0)
    draw_pyramid(3.0, 1.2, 3.0, 0.7, 0.2, 0.2)
    glPopMatrix()

def draw_dog():
    glPushMatrix()
    draw_generic_cube(0.25, 0.25, 0.5, 0.55, 0.27, 0.07)
    glPushMatrix()
    for ox in [-0.08, 0.08]:
        for oz in [-0.18, 0.18]:
            glPushMatrix()
            glTranslatef(ox, -0.12, oz)
            draw_generic_cube(0.06, 0.15, 0.06, 0.4, 0.2, 0.0)
            glPopMatrix()
    glPopMatrix()
    glTranslatef(0, 0.2, 0.2)
    draw_generic_cube(0.2, 0.2, 0.2, 0.55, 0.27, 0.07)
    glPopMatrix()

def draw_car(r, g, b):
    glPushMatrix()
    draw_generic_cube(1.0, 0.38, 1.8, r, g, b)
    glPushMatrix()
    glTranslatef(0, 0.38, -0.1)
    draw_generic_cube(0.8, 0.32, 1.0, r * 0.6, g * 0.6, b * 0.6)
    glPopMatrix()
    glPopMatrix()

def draw_truck():
    glPushMatrix()
    draw_generic_cube(1.4, 1.6, 3.6, 0.85, 0.85, 0.85)
    glTranslatef(0, 0, 1.3)
    draw_generic_cube(1.3, 1.0, 1.0, 0.8, 0.1, 0.1)
    glPopMatrix()

def draw_volleyball_court():
    glBegin(GL_QUADS)
    glColor3f(0.9, 0.5, 0.2)
    glVertex3f(-3.5, 0.02, -5.5); glVertex3f(3.5, 0.02, -5.5); glVertex3f(3.5, 0.02, 5.5); glVertex3f(-3.5, 0.02, 5.5)
    glColor3f(0.1, 0.4, 0.7)
    glVertex3f(-2.8, 0.025, -4.8); glVertex3f(2.8, 0.025, -4.8); glVertex3f(2.8, 0.025, 4.8); glVertex3f(-2.8, 0.025, 4.8)
    glEnd()
    draw_generic_cube(0.08, 1.8, 0.08, 0.6, 0.6, 0.6)
    glPushMatrix(); glTranslatef(0, 1.1, 0); draw_generic_cube(5.4, 0.5, 0.02, 0.9, 0.9, 0.9); glPopMatrix()

def draw_basketball_court():
    glBegin(GL_QUADS)
    glColor3f(0.75, 0.52, 0.3)
    glVertex3f(-3.5, 0.02, -6.0); glVertex3f(3.5, 0.02, -6.0); glVertex3f(3.5, 0.02, 6.0); glVertex3f(-3.5, 0.02, 6.0)
    glEnd()
    glPushMatrix(); glTranslatef(0, 0, -5.6); draw_generic_cube(0.12, 2.5, 0.12, 0.2, 0.2, 0.2); glTranslatef(0, 2.5, 0.15); draw_generic_cube(1.5, 0.9, 0.04, 1.0, 1.0, 1.0); glPopMatrix()
    glPushMatrix(); glTranslatef(0, 0, 5.6); draw_generic_cube(0.12, 2.5, 0.12, 0.2, 0.2, 0.2); glTranslatef(0, 2.5, -0.15); draw_generic_cube(1.5, 0.9, 0.04, 1.0, 1.0, 1.0); glPopMatrix()

def draw_tree_round():
    draw_generic_cube(0.2, 0.8, 0.2, 0.4, 0.25, 0.15)
    glPushMatrix(); glTranslatef(0, 0.8, 0); draw_generic_cube(1.0, 0.9, 1.0, 0.2, 0.55, 0.2); glPopMatrix()

def draw_tree_pine():
    draw_generic_cube(0.2, 0.6, 0.2, 0.4, 0.25, 0.15)
    glPushMatrix()
    glTranslatef(0, 0.5, 0); draw_pyramid(1.2, 0.8, 1.2, 0.1, 0.38, 0.15)
    glTranslatef(0, 0.5, 0); draw_pyramid(0.9, 0.7, 0.9, 0.12, 0.42, 0.18)
    glPopMatrix()

def draw_animated_helicopter(t):
    glPushMatrix()
    draw_generic_cube(1.4, 1.0, 3.0, 0.2, 0.2, 0.8)
    glPushMatrix(); glTranslatef(0, 0.2, -2.0); draw_generic_cube(0.3, 0.3, 1.5, 0.2, 0.2, 0.8); glPopMatrix()
    glPushMatrix(); glTranslatef(0, 1.1, 0); glRotatef(t * 800, 0, 1, 0); draw_generic_cube(4.0, 0.04, 0.25, 0.9, 0.9, 0.9); glPopMatrix()
    glPopMatrix()

def draw_scenery(t):
    glBegin(GL_QUADS)
    glColor3f(0.14, 0.14, 0.15)
    glVertex3f(-55, -0.01, 55); glVertex3f(55, -0.01, 55); glVertex3f(55, -0.01, -55); glVertex3f(-55, -0.01, -55)
    glEnd()

    manzanas = [
        (-32.0, -30.0, 24.0, 24.0), (-32.0, 5.0, 24.0, 20.0), (-32.0, 38.0, 24.0, 22.0),
        (0.0, -30.0, 30.0, 24.0),   (0.0, 5.0, 30.0, 20.0),   (0.0, 38.0, 30.0, 22.0),
        (35.0, -30.0, 30.0, 24.0),  (35.0, 5.0, 30.0, 20.0),  (35.0, 38.0, 30.0, 22.0)
    ]
    
    glBegin(GL_QUADS)
    for mx, mz, mw, md in manzanas:
        glColor3f(0.08, 0.08, 0.09) 
        w_h, d_h = mw / 2.0, md / 2.0
        glVertex3f(mx - w_h, 0.005, mz + d_h)
        glVertex3f(mx + w_h, 0.005, mz + d_h)
        glVertex3f(mx + w_h, 0.005, mz - d_h)
        glVertex3f(mx - w_h, 0.005, mz - d_h)
    glEnd()

    # --- UBICACIÓN FIJA DE SEMÁFOROS EN LAS ESQUINAS GRISES ---
    traffic_phase = int(t / 6.0) % 2
    vertical_green = (traffic_phase == 0)
    horizontal_green = not vertical_green

    # Semáforo 1: Intersección vertical (sobre la esquina gris de la banqueta)
    glPushMatrix()
    glTranslatef(-17.0, 0, 14.0)
    draw_traffic_light(vertical_green)
    glPopMatrix()

    # Semáforo 2: Intersección horizontal (sobre la esquina gris de la banqueta orientada correctamente)
    glPushMatrix()
    glTranslatef(-13.0, 0, 17.5)
    glRotatef(90, 0, 1, 0)
    draw_traffic_light(horizontal_green)
    glPopMatrix()

    # Parque / Zona Recreativa
    glPushMatrix()
    glTranslatef(-32.0, 0, 5.0)
    glBegin(GL_QUADS)
    glColor3f(0.2, 0.45, 0.22)
    glVertex3f(-11.5, 0.01, 9.5); glVertex3f(11.5, 0.01, 9.5); glVertex3f(11.5, 0.01, -9.5); glVertex3f(-11.5, 0.01, -9.5)
    glEnd()
    glPushMatrix(); glTranslatef(-5.5, 0, -3.0); draw_volleyball_court(); glPopMatrix()
    glPushMatrix(); glTranslatef(-5.5, 0, 4.5); draw_small_playground(); glPopMatrix()
    glPushMatrix(); glTranslatef(-1.0, 0.2, 2.5); draw_dog(); glPopMatrix()
    glPushMatrix(); glTranslatef(4.5, 0, 0.0); draw_kiosk(); glPopMatrix()
    for az in range(-8, 9, 4):
        glPushMatrix(); glTranslatef(-10.0, 0, az); draw_tree_round(); glPopMatrix()
        glPushMatrix(); glTranslatef(9.5, 0, az); draw_tree_pine(); glPopMatrix()
    glPopMatrix()

    # Zona Comunitaria
    glPushMatrix()
    glTranslatef(0.0, 0, -30.0)
    glPushMatrix(); glTranslatef(-7.0, 0, -4.0); draw_school(); glPopMatrix()
    glPushMatrix(); glTranslatef(1.0, 0, 2.0); draw_church(); glPopMatrix()
    glPushMatrix(); glTranslatef(9.0, 0, -2.0); draw_basketball_court(); glPopMatrix()
    glPopMatrix()

    # Edificios Grandes
    skyscrapers = [
        (-32.0, -30.0, 4.5, 18.0, 4.5, 0.25, 0.35, 0.5), (-25.0, -26.0, 4.0, 14.0, 4.0, 0.3, 0.3, 0.35),
        (0.0, 38.0, 5.0, 26.0, 5.0, 0.15, 0.4, 0.45), (8.0, 42.0, 4.5, 22.0, 4.5, 0.2, 0.2, 0.3),
        (-8.0, 35.0, 4.0, 17.0, 4.0, 0.35, 0.35, 0.4), (35.0, 38.0, 5.5, 29.0, 5.5, 0.1, 0.25, 0.5),
        (42.0, 44.0, 4.0, 20.0, 4.0, 0.22, 0.45, 0.4), (28.0, 34.0, 4.2, 15.0, 4.2, 0.4, 0.4, 0.45),
    ]
    for x, z, w, h, d, r, g, b in skyscrapers:
        glPushMatrix(); glTranslatef(x, 0, z); draw_generic_cube(w, h, d, r, g, b); draw_windows(w, h, d, int(h // 1.5), 4); glPopMatrix()

    # Casas
    house_positions = [
        (-38.0, 32.0), (-32.0, 32.0), (-26.0, 32.0), (-35.0, 42.0), (-29.0, 42.0),
        (-10.0, 2.0), (-4.0, 2.0), (-10.0, 9.0), (-4.0, 9.0),
        (22.0, 1.0), (28.0, 1.0), (34.0, 1.0), (25.0, 9.0), (31.0, 9.0),
        (24.0, -35.0), (30.0, -35.0), (38.0, -35.0), (32.0, -25.0)
    ]
    house_colors = [(0.85, 0.45, 0.45), (0.45, 0.65, 0.85), (0.55, 0.75, 0.55), (0.85, 0.80, 0.55), (0.75, 0.60, 0.80)]
    for idx, (hx, hz) in enumerate(house_positions):
        r_c, g_c, b_c = house_colors[idx % len(house_colors)]
        glPushMatrix(); glTranslatef(hx, 0, hz); draw_detailed_house(2.4, 2.0, 2.4, r_c, g_c, b_c); glPopMatrix()

    glPushMatrix(); glTranslatef(4.0, 0, 5.0); draw_cafe(); glPopMatrix()

    # Vías e Integración de Tráfico
    vias_verticales = [-15.0, 15.0, 49.0]
    for idx, x_lane in enumerate(vias_verticales):
        v_speed = 9.0 + (idx % 2) * 3.0
        z_pos1 = -50.0 + ((t * v_speed) % 100.0)
        z_pos2 = -50.0 + (((t * v_speed) + 50.0) % 100.0)
        z_pos3 = -50.0 + (((t * v_speed) + 25.0) % 100.0)
        
        if x_lane == -15.0 and not vertical_green:
            if 4.0 < z_pos1 < 16.0: z_pos1 = 4.0
            if 4.0 < z_pos2 < 16.0: z_pos2 = 4.0
            if 4.0 < z_pos3 < 16.0: z_pos3 = 4.0

        glPushMatrix(); glTranslatef(x_lane - 0.7, 0.15, z_pos1); draw_car(0.85, 0.1, 0.1); glPopMatrix()
        glPushMatrix(); glTranslatef(x_lane + 0.7, 0.15, z_pos2); draw_truck(); glPopMatrix()
        glPushMatrix(); glTranslatef(x_lane + 0.0, 0.15, z_pos3); draw_pink_motorcycle(); glPopMatrix()

    vias_horizontales = [-18.0, 16.0, 49.0]
    for idx, z_lane in enumerate(vias_horizontales):
        h_speed = 10.0 + (idx % 2) * 3.0
        x_pos1 = -50.0 + ((t * h_speed) % 100.0)
        x_pos2 = -50.0 + (((t * h_speed) + 50.0) % 100.0)
        x_pos3 = -50.0 + (((t * h_speed) + 75.0) % 100.0)
        
        if z_lane == 16.0 and not horizontal_green:
            if -27.0 < x_pos1 < -15.0: x_pos1 = -27.0
            if -27.0 < x_pos2 < -15.0: x_pos2 = -27.0
            if -27.0 < x_pos3 < -15.0: x_pos3 = -27.0

        glPushMatrix(); glTranslatef(x_pos1, 0.15, z_lane - 0.7); glRotatef(90, 0, 1, 0); draw_car(0.9, 0.8, 0.1); glPopMatrix()
        glPushMatrix(); glTranslatef(x_pos2, 0.15, z_lane + 0.7); glRotatef(90, 0, 1, 0); draw_car(0.15, 0.65, 0.22); glPopMatrix()
        glPushMatrix(); glTranslatef(x_pos3, 0.15, z_lane + 0.0); glRotatef(90, 0, 1, 0); draw_pink_motorcycle(); glPopMatrix()

    glPushMatrix()
    glRotatef(t * 22, 0, 1, 0)
    glTranslatef(15.0, 24.0, 10.0)
    draw_animated_helicopter(t)
    glPopMatrix()

def draw_hand_overlay(frame, keypoints, handedness):
    color_node = (255, 120, 0) if handedness == "Right" else (0, 120, 255)
    for pt in keypoints:
        cv2.circle(frame, pt, 4, color_node, cv2.FILLED)
    for c in HAND_CONNECTIONS:
        cv2.line(frame, keypoints[c[0]], keypoints[c[1]], (80, 255, 80), 2)

def process_thumb_gestures(results):
    """Mapeo directo del pulgar hacia la dirección del movimiento de la pantalla"""
    global cam_eye_x, cam_eye_z, cam_center_x, cam_center_z
    
    if not results.hand_landmarks:
        return

    for idx, hand_lm in enumerate(results.hand_landmarks):
        thumb_tip = hand_lm[4]
        index_base = hand_lm[5]
        wrist = hand_lm[0]

        # Desplazamientos directos relativos
        dx = thumb_tip.x - index_base.x
        dy = thumb_tip.y - wrist.y

        step = 0.9  # Velocidad de movimiento lineal

        # Control Horizontal (Pulgar Izquierda / Derecha)
        if dx > 0.05:
            cam_eye_x += step
            cam_center_x += step
        elif dx < -0.05:
            cam_eye_x -= step
            cam_center_x -= step

        # Control Vertical (Pulgar Arriba / Abajo)
        if dy < -0.20:
            cam_eye_z -= step
            cam_center_z -= step
        elif dy > -0.08:
            cam_eye_z += step
            cam_center_z += step

def main():
    global cam_eye_x, cam_eye_y, cam_eye_z, cam_center_x, cam_center_y, cam_center_z

    if not os.path.exists(MODEL_PATH):
        print(f"Error: No se encontró el archivo del modelo en {MODEL_PATH}")
        sys.exit(1)

    if not glfw.init():
        sys.exit(1)

    win_w, win_h = 1100, 850
    window = glfw.create_window(win_w, win_h, "Simulador Urbano - Control Directo de Esquinas y Gestos", None, None)
    if not window:
        glfw.terminate()
        sys.exit(1)

    glfw.make_context_current(window)
    glViewport(0, 0, win_w, win_h)
    glClearColor(0.06, 0.08, 0.12, 1.0) 
    glEnable(GL_DEPTH_TEST)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, win_w / win_h, 1.0, 350.0)
    glMatrixMode(GL_MODELVIEW)

    options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=VisionRunningMode.IMAGE,
        num_hands=2,
        min_hand_detection_confidence=0.55,
    )

    cap = cv2.VideoCapture(0)

    with HandLandmarker.create_from_options(options) as landmarker:
        while not glfw.window_should_close(window):
            if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
                break

            ret, frame = cap.read()
            if not ret: break

            frame = cv2.flip(frame, 1)
            f_h, f_w, _ = frame.shape
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            
            results = landmarker.detect(mp_image)
            process_thumb_gestures(results)

            if results.hand_landmarks:
                for idx, hand_lm in enumerate(results.hand_landmarks):
                    side = results.handedness[idx][0].category_name if results.handedness else "Right"
                    pts = [(int(lm.x * f_w), int(lm.y * f_h)) for lm in hand_lm]
                    draw_hand_overlay(frame, pts, side)

            cv2.imshow("Camara de Control Gestual", frame)
            cv2.waitKey(1)

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            t = glfw.get_time()

            gluLookAt(cam_eye_x, cam_eye_y, cam_eye_z, 
                      cam_center_x, cam_center_y, cam_center_z, 
                      0.0, 1.0, 0.0)

            draw_scenery(t)

            glfw.swap_buffers(window)
            glfw.poll_events()

    cap.release()
    cv2.destroyAllWindows()
    glfw.terminate()

if __name__ == "__main__":
    main()