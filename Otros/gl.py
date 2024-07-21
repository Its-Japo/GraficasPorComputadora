import struct
import random
def char(c):
    # 1 byte
    return struct.pack("=c", c.encode("ascii"))

def word(w):
    # 2 bytes
    return struct.pack("=h", w)

def dword(d):
    # 4 bytes
    return struct.pack("=l", d)



class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        # No se toman las primeras dos, el screen.get_rect nos da las posiciones de origen y unicamente queremos width + height
        _, _, self.width, self.height = screen.get_rect()

        self.glColor(1, 1, 1)
        self.glClearColor(0, 0, 0)
        self.glClear()

    def glGenerateFrameBuffer(self, filename):
        with open(filename, "wb") as file:
            # Header
            file.write(char("B"))
            file.write(char("M"))
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(14 + 40))

            # Info Header
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            # Color table
            for y in range(self.height):
                for x in range(self.width):
                    color = self.frameBuffer[x][y]
                    color = bytes([color[2],
                                   color[1],
                                   color[0]])
                    file.write(color)

    def glColor(self, r, g, b):
        r = min(1, max(0, r))
        g = min(1, max(0, g))
        b = min(1, max(0, b))

        self.currColor = [r, g, b]

    def glClearColor(self, r, g, b):
        r = min(1, max(0, r))
        g = min(1, max(0, g))
        b = min(1, max(0, b))

        self.clearColor = [r, g, b]

    def glClear(self):
        color = [int(i * 255) for i in self.clearColor]
        self.screen.fill(color)

        self.frameBuffer = [[self.clearColor for y in range(self.height)]
                            for x in range(self.width)]

    # Pygame dibuja desde superior izquierda
    def glPoint(self, x, y, color=None):
        # Pygame recibe colores de 0 a 255
        if (0 <= x < self.width and (0 <= y < self.height)):
            color = [int(i * 255) for i in (color or self.currColor)]
            self.screen.set_at((x, self.height - 1 - y), color)
            self.frameBuffer[x][y] = color

    #Implementacion de scanline
    def glFill(self, listaPuntos, color):
        print(listaPuntos)
        pol_color = [int(i * 255) for i in color]
        for i in range(len(listaPuntos)):
            self.glLine(listaPuntos[i], listaPuntos[(i + 1) % len(listaPuntos)], color)
            print(f"Linea de + {listaPuntos[i]} hasta {listaPuntos[(i + 1) % len(listaPuntos)]}")
        #Encuentra las coordenadas X y Y
        coords_x = [coord[0] for coord in listaPuntos]
        coords_y = [coord[1] for coord in listaPuntos]

        #Encuentra los minimos y maximos en X y Y para crear el "Boundry Box"
        min_x = min(coords_x)
        max_x = max(coords_x)
        min_y = min(coords_y)
        max_y = max(coords_y)

        no_point = True
        #Busca un punto adentro del poligono dentro de Boundry Box aleatoriamente
        for i in range(min_y, max_y + 1):
            for j in range(min_x, max_x + 1):
                if self.pointInPolygon(listaPuntos, j, i):
                    self.glPoint(j, i, color)

    def pointInPolygon(self, listaPuntos, x, y):
        n = len(listaPuntos)
        inside = False
        x1, y1 = listaPuntos[0]

        for i in range(n + 1):
            x2, y2 = listaPuntos[i % n]
            if min(y1, y2) < y <= max(y1, y2):
                if x <= max(x1, x2):
                    if y1 != y2:
                        interx = (y - y1) * (x2 - x1) / (y2 - y1) + x1
                    if x1 == x2 or x <= interx:
                        inside = not inside
            x1, y1 = x2, y2
        return inside
    #glLine pero retorna una lista de tuplas con los puntos que dibujo
    def glLineWithPoints(self, v0, v1, color):
        points = []
        x0 = int(v0[0])
        x1 = int(v1[0])
        y0 = int(v0[1])
        y1 = int(v1[1])

        # Algoritmo de Lineas de Bresenham

        if x0 == x1 and y0 == y1:
            self.glPoint(x0, y0, color)

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x1 < x0:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0
        limit = 0.5
        m = dy / dx
        y = y0
        for x in range(x0, x1 + 1):
            if steep:
                self.glPoint(y, x, color or self.currColor)
                points.append((y,x))
            else:
                self.glPoint(x, y, color or self.currColor)
                points.append((x,y))
            offset += m
            if offset >= limit:
                if y0 < y1:
                    y += 1
                else:
                    y -= 1
                limit += 1
        return points

    def glLine(self, v0, v1, color):
        x0 = int(v0[0])
        x1 = int(v1[0])
        y0 = int(v0[1])
        y1 = int(v1[1])

        # Algoritmo de Lineas de Bresenham

        if x0 == x1 and y0 == y1:
            self.glPoint(x0, y0, color)

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x1 < x0:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0
        limit = 0.5
        m = dy / dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                self.glPoint(y, x, color or self.currColor)
            else:
                self.glPoint(x, y, color or self.currColor)
            offset += m
            if offset >= limit:
                if y0 < y1:
                    y += 1
                else:
                    y -= 1
                limit += 1

    def getPixelColor(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.frameBuffer[x][y]
        return None