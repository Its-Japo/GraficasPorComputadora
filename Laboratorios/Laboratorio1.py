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

poligono1 = [
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
]


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

    rend.glPoligono(poligono1)

rend.glGenerateFrameBuffer("output.bmp")

pygame.quit()
