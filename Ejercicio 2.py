import pygame
from gl import Renderer, POINTS, LINES,TRANGLES
from pygame.locals import *
from modelo import Model
from shaders import vertexShader

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
rend.vertexShader = vertexShader

modelo1 = Model("ship.obj")
modelo1.translate[0] = width / 2
modelo1.translate[1] = height / 2

modelo1.scale[0] = 100
modelo1.scale[1] = 100
modelo1.scale[2] = 100


rend.models.append(modelo1)

while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

            elif event.key == pygame.K_RIGHT:
                modelo1.rotate[1] += 10
            elif event.key == pygame.K_LEFT:
                modelo1.rotate[1] -= 10

            elif event.key == pygame.K_1:
                rend.primitiveType = POINTS
            elif event.key == pygame.K_2:
                rend.primitiveType = LINES

    rend.glClear()

    rend.glRender()

    pygame.display.flip()
    clock.tick(60)


rend.glGenerateFrameBuffer("output.bmp")

pygame.quit()
