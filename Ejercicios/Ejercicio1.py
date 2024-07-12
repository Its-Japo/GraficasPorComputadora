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
rend.glColor(1, 0, 0)


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
    for x in range(0, width, 20):
        rend.glLine((0, 0), (x, height))
        rend.glLine((0, height - 1), (x, 0))
        rend.glLine((width - 1, 0), (x, height))
        rend.glLine((width - 1, height - 1), (x, 0))

rend.glGenerateFrameBuffer("output.bmp")

pygame.quit()
