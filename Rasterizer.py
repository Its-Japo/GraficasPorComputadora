
import pygame
from pygame.locals import *
from gl import *
from model import Model
from shaders import vertexShader, fragmentShader

width = 900
height = 512

screen = pygame.display.set_mode((width, height), pygame.SCALED  )
clock = pygame.time.Clock()

rend = Renderer(screen)
rend.vertexShader = vertexShader
rend.fragmentShader = fragmentShader


modelo1 = Model("assets/objects/sword.obj")
modelo1.LoadTexture("assets/textures/Sting_Base_Color.bmp")
modelo1.translate[0] = 0
modelo1.translate[1] = 0
modelo1.translate[2] = -50

modelo1.rotate[0] = 90

modelo1.scale[0] = 0.7
modelo1.scale[1] = 0.7
modelo1.scale[2] = 0.7


rend.models.append(modelo1)

isRunning = True
while isRunning:
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			isRunning = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				isRunning = False
				
			elif event.key == pygame.K_1:
				rend.primitiveType = POINTS
				
			elif event.key == pygame.K_2:
				rend.primitiveType = LINES
				
			elif event.key == pygame.K_3:
				rend.primitiveType = TRIANGLES
				

			elif event.key == pygame.K_RIGHT:
				rend.camera.translate[0] += 1
			elif event.key == pygame.K_LEFT:
				rend.camera.translate[0] -= 1
			elif event.key == pygame.K_UP:
				rend.camera.translate[1] += 1
			elif event.key == pygame.K_DOWN:
				rend.camera.translate[1] -= 1
				
					
	rend.glClear()
	rend.glRender()

	pygame.display.flip()
	clock.tick(60)
	
rend.glGenerateFrameBuffer("output.bmp")

pygame.quit()
