import pygame
from gl import Renderer
from pygame.locals import *

# Variables de dimensiones de la pantalla
width = 960
height = 540
# Inicializa la pantalla de Pygame
screen = pygame.display.set_mode((width, height))

# Refresh rate / FPS
clock = pygame.time.Clock()

# Loop donde todo va a estar corriendo
isRunning = True

rend = Renderer(screen)

poligonos = [
    [
        (165, 380),
        (185, 360),
        (180, 330),
        (207, 345),
        (233, 330),
        (230, 360),
        (250, 380),
        (220, 385),
        (205, 410),
        (193, 383),
    ],
    [(321, 335), (288, 286), (339, 251), (374, 302)],
    [(377, 249), (411, 197), (436, 249)],
    [
        (413, 177),
        (448, 159),
        (502, 88),
        (553, 53),
        (535, 36),
        (676, 37),
        (660, 52),
        (750, 145),
        (761, 179),
        (672, 192),
        (659, 214),
        (615, 214),
        (632, 230),
        (580, 230),
        (597, 215),
        (552, 214),
        (517, 144),
        (466, 180),
    ],
    [(682, 175), (708, 120), (735, 148), (739, 170)],
]

colors = [(1, 1, 1), (1, 1, 1), (1, 1, 1), (1, 1, 1), (0, 0, 0)]


while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
    pygame.display.flip()
    clock.tick(60)

    rend.glClear()
    for i in range(len(poligonos)):
        rend.glColor(colors[i][0], colors[i][1], colors[i][2])
        rend.glFill(rend.glPoligono(poligonos[i]))

rend.glGenerateFrameBuffer("output.bmp")

pygame.quit()
