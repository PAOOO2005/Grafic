import time
import math
import numpy as np
import cv2

# --- CONFIGURACIÓN GLOBAL ---
W, H = 800, 600
FPS = 30
DURATION = 60.0  # 6 escenas de 10 segundos cada una

def clamp01(x): 
    return 0.0 if x < 0.0 else (1.0 if x > 1.0 else x)

def smoothstep(a, b, x):
    x = clamp01((x - a) / (b - a))
    return x * x * (3 - 2 * x)

def poly_param(fx, fy, t0, t1, n, cx, cy, sx, sy):
    """Genera puntos ordenados para cv2.polylines basados en funciones paramétricas"""
    ts = np.linspace(t0, t1, n, dtype=np.float32)
    xs = fx(ts) * sx + cx
    ys = fy(ts) * sy + cy
    return np.round(np.stack([xs, ys], 1)).astype(np.int32).reshape((-1, 1, 2))

def hsv_to_bgr(h, s, v):
    hsv = np.uint8([[[h % 180, np.clip(s, 0, 255), np.clip(v, 0, 255)]]])
    return tuple(int(x) for x in cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)[0, 0])

def background_gradient(img, t, h0=130, h1=170):
    """Fondo dinámico procedural usando gradiente vertical en HSV"""
    hsv = np.zeros((H, W, 3), np.uint8)
    ys = np.linspace(0, 1, H, dtype=np.float32)
    hue = (h0 + (h1 - h0) * ys + 8 * np.sin(t * 0.5 + ys * 3.0)).astype(np.float32)
    hsv[:, :, 0] = np.clip(hue, 0, 179).astype(np.uint8)[:, None]
    hsv[:, :, 1] = 180
    hsv[:, :, 2] = (30 + 90 * (1 - ys)).astype(np.uint8)[:, None]
    img[:] = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def draw_stars(img, t, rng_seed=42, num_stars=80):
    """Efecto global de fondo: Campo de estrellas titilantes"""
    rng = np.random.default_rng(rng_seed)
    xs = rng.integers(0, W, num_stars)
    ys = rng.integers(0, H, num_stars)
    sizes = rng.integers(1, 3, num_stars)
    for i in range(num_stars):
        # Brillo variable por el tiempo para simular titileo
        blink = int(150 + 105 * math.sin(t * 3.0 + i))
        cv2.circle(img, (int(xs[i]), int(ys[i])), int(sizes[i]), (blink, blink, blink), -1)

# --- POST-PROCESAMIENTO / FILTROS ---
def post_vignette(img, strength=0.75):
    """Filtro de Viñeta (Oscurece los bordes)"""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    nx = (xx - W * 0.5) / (W * 0.5)
    ny = (yy - H * 0.5) / (H * 0.5)
    r2 = nx * nx + ny * ny
    mask = np.clip(1.0 - strength * r2, 0.0, 1.0)
    return (img.astype(np.float32) * mask[..., None]).astype(np.uint8)

# --- ESCENAS ENRIQUECIDAS ---

def scene_1_intro(img, t):
    """Escena 1: Créditos + Estrellas + Círculos Cruzándose + Cuadros Rotatorios"""
    background_gradient(img, t, h0=100, h1=140)
    draw_stars(img, t, rng_seed=111, num_stars=100)
    
    # Cuadros de fondo rotando
    cx, cy = W // 2, H // 2
    for i in range(1, 6):
        size = i * 60 + int(20 * math.sin(t * 2 + i))
        angle = t * 0.5 * (1 if i % 2 == 0 else -1)
        M = cv2.getRotationMatrix2D((cx, cy), math.degrees(angle), 1.0)
        
        rect_box = np.array([[cx-size, cy-size], [cx+size, cy-size], [cx+size, cy+size], [cx-size, cy+size]], np.int32)
        temp = np.zeros_like(img)
        cv2.polylines(temp, [rect_box], True, hsv_to_bgr(120 + i*10, 200, 140), 2, cv2.LINE_AA)
        
        rotated = cv2.warpAffine(temp, M, (W, H))
        img[:] = cv2.addWeighted(img, 1.0, rotated, 0.5, 0)

    # Elemento extra: Círculos cruzándose dinámicamente en las esquinas
    offset_c = int(40 * math.sin(t * 2.0))
    cv2.circle(img, (100 + offset_c, 100), 60, (200, 255, 200), 2, cv2.LINE_AA)
    cv2.circle(img, (150 - offset_c, 100), 60, (255, 200, 200), 2, cv2.LINE_AA)
    
    cv2.circle(img, (W - 100 + offset_c, H - 100), 60, (200, 255, 255), 2, cv2.LINE_AA)
    cv2.circle(img, (W - 150 - offset_c, H - 100), 60, (255, 200, 255), 2, cv2.LINE_AA)

    # Textos solicitados
    cv2.putText(img, "PROCEDUAL DEMO GRAFICACION", (50, H//2 - 20), cv2.FONT_HERSHEY_TRIPLEX, 1.1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(img, "OPEN CV", (50, H//2 + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (200, 255, 200), 2, cv2.LINE_AA)


def scene_2_butterfly(img, t):
    """Escena 2: Múltiples Mariposas Matemáticas (¡No solo una!) + Estrellas de fondo"""
    background_gradient(img, t, h0=140, h1=179)
    draw_stars(img, t, rng_seed=222, num_stars=60)
    
    # Ecuación base de la mariposa de Fay
    fx = lambda th: np.sin(th) * (np.exp(np.cos(th)) - 2 * np.cos(4 * th) - np.sin(th / 12.0) ** 5)
    fy = lambda th: -np.cos(th) * (np.exp(np.cos(th)) - 2 * np.cos(4 * th) - np.sin(th / 12.0) ** 5)
    
    # Mariposa 1: La Central (Grande)
    t_mod1 = 1.0 + 0.15 * math.sin(t * 3.0)
    pts1 = poly_param(lambda th: fx(th) * t_mod1, fy, 0, 4 * math.pi, 1000, W // 2, H // 2 - 20, 70, 70)
    cv2.polylines(img, [pts1], False, hsv_to_bgr(150, 220, 255), 2, cv2.LINE_AA)
    
    # Mariposa 2: Órbita Izquierda (Mediana y rápido aleteo)
    t_mod2 = 1.0 + 0.25 * math.sin(t * 5.0)
    cx2 = int(W * 0.22 + 30 * math.sin(t))
    cy2 = int(H * 0.4 + 40 * math.cos(t))
    pts2 = poly_param(lambda th: fx(th) * t_mod2, fy, 0, 4 * math.pi, 600, cx2, cy2, 35, 35)
    cv2.polylines(img, [pts2], False, hsv_to_bgr(130, 240, 230), 1, cv2.LINE_AA)
    
    # Mariposa 3: Órbita Derecha (Pequeña)
    t_mod3 = 1.0 + 0.20 * math.cos(t * 4.0)
    cx3 = int(W * 0.78 + 30 * math.cos(t))
    cy3 = int(H * 0.6 + 40 * math.sin(t))
    pts3 = poly_param(lambda th: fx(th) * t_mod3, fy, 0, 4 * math.pi, 600, cx3, cy3, 25, 25)
    cv2.polylines(img, [pts3], False, hsv_to_bgr(170, 200, 245), 1, cv2.LINE_AA)
    
    cv2.putText(img, "Curva 1: Fay's Butterflies (Multiples)", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1, cv2.LINE_AA)


def scene_3_rhombus_matrix(img, t):
    """Escena 3: Muchos Rombos + Espirales Giratorias de fondo"""
    background_gradient(img, t, h0=10, h1=40)
    
    cx, cy = W // 2, H // 2
    
    # Elemento extra: Espirales decorativas de fondo (como engranajes)
    f_esp_x = lambda th: (0.5 * th) * np.cos(th + t * 2.0)
    f_esp_y = lambda th: (0.5 * th) * np.sin(th + t * 2.0)
    for esp_cx, esp_cy in [(150, 150), (W-150, 150), (150, H-150), (W-150, H-150)]:
        pts_esp = poly_param(f_esp_x, f_esp_y, 0, 6*math.pi, 300, esp_cx, esp_cy, 6, 6)
        cv2.polylines(img, [pts_esp], False, hsv_to_bgr(30, 180, 100), 1, cv2.LINE_AA)

    # Rejilla de rombos con transformación afín global
    shear_x = 0.5 * math.sin(t * 1.5)
    scale = 0.8 + 0.2 * math.cos(t * 2.0)
    M = np.array([
        [scale, shear_x * scale, cx * (1 - scale)],
        [0.0,   scale,           cy * (1 - scale)]
    ], dtype=np.float32)
    
    layer = np.zeros_like(img)
    r_size = 25
    for x in range(100, W, 120):
        for y in range(80, H, 120):
            pts_rombo = np.array([[x, y - r_size], [x + r_size, y], [x, y + r_size], [x - r_size, y]], np.int32)
            color_r = hsv_to_bgr(int(20 + x*0.05), 240, 200)
            cv2.fillPoly(layer, [pts_rombo], color_r, cv2.LINE_AA)
            cv2.polylines(layer, [pts_rombo], True, (255,255,255), 1, cv2.LINE_AA)
            
    transformed = cv2.warpAffine(layer, M, (W, H))
    img[:] = cv2.addWeighted(img, 1.0, transformed, 0.9, 0)
    
    cv2.putText(img, "Transformaciones: Escala + Shear + Espirales", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1, cv2.LINE_AA)


def scene_4_circles_pulsar(img, t):
    """Escena 4: Círculos múltiples cruzándose en interferencia + Lemniscatas"""
    background_gradient(img, t, h0=60, h1=95)
    draw_stars(img, t, rng_seed=333, num_stars=50)
    
    # Dos emisores de círculos cruzándose para crear patrones geométricos complejos
    cx1, cy1 = int(W * 0.35), H // 2
    cx2, cy2 = int(W * 0.65), H // 2
    
    for i in range(6):
        radius = int((t * 70 + i * 60) % 280)
        alpha = max(0, 1.0 - (radius / 280.0))
        
        # Emisor izquierdo
        cv2.circle(img, (cx1, cy1), radius, hsv_to_bgr(75, 210, int(230 * alpha)), 2, cv2.LINE_AA)
        # Emisor derecho (se cruza con el anterior)
        cv2.circle(img, (cx2, cy2), radius, hsv_to_bgr(90, 210, int(230 * alpha)), 2, cv2.LINE_AA)
        
    # Curva 2: Lemniscata de Gerono
    fx2 = lambda th: np.sin(th)
    fy2 = lambda th: np.sin(th) * np.cos(th)
    pts_gerono = poly_param(fx2, fy2, 0, 2*math.pi, 400, W//4, H//4, 100, 100)
    cv2.polylines(img, [pts_gerono], True, (255, 180, 255), 2, cv2.LINE_AA)
    
    # Curva 3: Lemniscata de Bernoulli
    fx3 = lambda th: np.cos(th) / (1 + np.sin(th)**2)
    fy3 = lambda th: (np.sin(th) * np.cos(th)) / (1 + np.sin(th)**2)
    pts_bernoulli = poly_param(fx3, fy3, 0, 2*math.pi, 400, 3*W//4, 3*H//4, 120, 120)
    cv2.polylines(img, [pts_bernoulli], True, (200, 255, 255), 2, cv2.LINE_AA)

    cv2.putText(img, "Curvas 2 y 3: Circulos Cruzados en Interferencia", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1, cv2.LINE_AA)


def scene_5_geometry_storm(img, t, rng):
    """Escena 5: Tormenta densa de cuadros y rombos geométricos + Estrellas veloces"""
    background_gradient(img, t, h0=0, h1=30)
    
    # Fondo extra: Estrellas moviéndose horizontalmente rápidas
    num_fast_stars = 40
    state_rng = np.random.default_rng(555)
    st_xs = (state_rng.integers(0, W, num_fast_stars) + int(t * 180)) % W
    st_ys = state_rng.integers(0, H, num_fast_stars)
    for i in range(num_fast_stars):
        cv2.line(img, (st_xs[i], st_ys[i]), (st_xs[i] + 4, st_ys[i]), (200, 200, 255), 1, cv2.LINE_AA)

    # Campo denso de primitivas combinadas
    n_particles = 220
    for i in range(n_particles):
        seed_x = (i * 8.2)
        seed_y = (i * 11.7)
        
        x = int((seed_x + t * 50 + 60 * math.sin(t + seed_y)) % W)
        y = int((seed_y + t * 30 + 50 * math.cos(t * 0.6 + seed_x)) % H)
        
        size = int(6 + 5 * math.sin(t + i))
        color_p = hsv_to_bgr(int(t*12 + i), 230, 240)
        
        if i % 2 == 0:
            cv2.rectangle(img, (x - size, y - size), (x + size, y + size), color_p, -1)
        else:
            pts_p = np.array([[x, y - size], [x + size, y], [x, y + size], [x - size, y]], np.int32)
            cv2.fillPoly(img, [pts_p], color_p, cv2.LINE_AA)
            
    cv2.putText(img, "Primitivas Colectivas: Tormenta de Poligonos", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1, cv2.LINE_AA)


def scene_6_final_math(img, t):
    """Escena 6: Clímax avanzado con 3 curvas, elipse central y anillo de mini-rombos"""
    background_gradient(img, t, h0=110, h1=160)
    draw_stars(img, t, rng_seed=777, num_stars=90)
    cx, cy = W // 2, H // 2
    
    # Curva 4: Epicicloide
    fx4 = lambda th: 5 * np.cos(th) - np.cos(5 * th)
    fy4 = lambda th: 5 * np.sin(th) - np.sin(5 * th)
    pts_epi = poly_param(fx4, fy4, 0, 2*math.pi, 600, cx, cy, 25, 25)
    cv2.polylines(img, [pts_epi], True, (150, 255, 255), 3, cv2.LINE_AA)
    
    # Curva 5: Cardioide
    fx5 = lambda th: 2 * np.cos(th) * (1 - np.cos(th))
    fy5 = lambda th: 2 * np.sin(th) * (1 - np.cos(th))
    pts_cardio = poly_param(fx5, fy5, 0, 2*math.pi, 400, cx - 180, cy + 120, 45, 45)
    cv2.polylines(img, [pts_cardio], True, (200, 200, 255), 2, cv2.LINE_AA)
    
    # Curva 6: Espiral de Arquímedes
    fx6 = lambda th: (0.8 * th) * np.cos(th + t)
    fy6 = lambda th: (0.8 * th) * np.sin(th + t)
    pts_espiral = poly_param(fx6, fy6, 0, 8*math.pi, 800, cx + 200, cy + 120, 10, 10)
    cv2.polylines(img, [pts_espiral], False, (255, 180, 200), 2, cv2.LINE_AA)

    # Adición estética: Anillo orbital exterior hecho de pequeños rombos
    num_orbit_rombos = 12
    for i in range(num_orbit_rombos):
        ang = (t * 0.8) + (i * (2 * math.pi / num_orbit_rombos))
        rx = int(cx + 160 * math.cos(ang))
        ry = int(cy + 160 * math.sin(ang))
        r_pts = np.array([[rx, ry - 8], [rx + 8, ry], [rx, ry + 8], [rx - 8, ry]], np.int32)
        cv2.fillPoly(img, [r_pts], (255, 255, 255), cv2.LINE_AA)

    # Elipse central rotatoria
    cv2.ellipse(img, (cx, cy), (int(80 + 10*math.sin(t*4)), 40), math.degrees(t), 0, 360, (255,255,255), 2, cv2.LINE_AA)

    cv2.putText(img, "Fin del Demo - Matematicas Completas", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1, cv2.LINE_AA)

# --- SISTEMA DE CONTROL DE TIMELINE Y TRANSICIONES ---

def render_scene_router(buf, scene_id, t, rng):
    if scene_id == 0:
        scene_1_intro(buf, t)
    elif scene_id == 1:
        scene_2_butterfly(buf, t)
    elif scene_id == 2:
        scene_3_rhombus_matrix(buf, t)
    elif scene_id == 3:
        scene_4_circles_pulsar(buf, t)
    elif scene_id == 4:
        scene_5_geometry_storm(buf, t, rng)
    else:
        scene_6_final_math(buf, t)

def timeline(t, rng, bufA, bufB):
    block = int(min(5, max(0, t // 10)))
    t_in = t - block * 10
    
    render_scene_router(bufA, block, t, rng)
    frame = bufA
    
    # Transiciones matemáticas limpias (Crossfade)
    if block < 5 and t_in >= 8.8:
        render_scene_router(bufA, block, t, rng)
        render_scene_router(bufB, block + 1, t, rng)
        alpha = smoothstep(8.8, 10.0, t_in)
        frame = cv2.addWeighted(bufA, 1.0 - alpha, bufB, alpha, 0)
        
    # Fade general de entrada y salida
    fade_in = smoothstep(0.0, 2.0, t)
    fade_out = 1.0 - smoothstep(DURATION - 2.0, DURATION, t)
    total_fade = fade_in * fade_out
    
    if total_fade < 0.999:
        frame = (frame.astype(np.float32) * total_fade).astype(np.uint8)
        
    return frame

# --- LOOP PRINCIPAL Y EXPORTACIÓN ---

def main():
    rng = np.random.default_rng(2026)
    bufA = np.zeros((H, W, 3), np.uint8)
    bufB = np.zeros((H, W, 3), np.uint8)
    
    total_frames = int(DURATION * FPS)
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter('renders/demo_final.mp4', fourcc, FPS, (W, H))
    
    print("-> Renderizando y guardando en 'renders/demo_final.mp4'...")
    
    for i in range(total_frames):
        t = i / FPS
        
        frame = timeline(t, rng, bufA, bufB)
        frame = post_vignette(frame, 0.75)
        
        video_writer.write(frame)
        
        cv2.imshow("Proyecto 1: Demo Procedura", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # Salir con la tecla ESC
            break
            
    video_writer.release()
    cv2.destroyAllWindows()
    print("¡Listo! El demo se ha renderizado")

if __name__ == "__main__":
    main()