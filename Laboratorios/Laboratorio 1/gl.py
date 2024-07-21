import struct


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
        _, _, self.width, self.height = screen.get_rect()

        self.glColor(1, 1, 1)
        self.glClearColor(0, 0, 0)
        self.glClear()

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

        self.frameBufer = [
            [self.clearColor for y in range(self.height)] for x in range(self.width)
        ]

    def glPoint(self, x, y, color=None):
        # PyGame empieza a renderizar desde la esquina
        # superior izquierda. Hay que voltear el valor 'y'

        if (0 <= x < self.width) and (0 <= y < self.height):
            # Pygame recibe los colores en un rango de 0 a 255
            color = [int(i * 255) for i in (color or self.currColor)]

            self.screen.set_at((x, self.height - 1 - y), color)
            self.frameBufer[x][y] = color

    def glLine(self, v0: int, v1: int, color=None):
        # y = mx + b ssi m <= 1
        # x = my + b ssi m > 1

        x0 = int(v0[0])
        y0 = int(v0[1])
        x1 = int(v1[0])
        y1 = int(v1[1])

        if x0 == x1 and y0 == y1:
            self.glPoint(x0, y0)
            return

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        m = dy / dx

        offset = 0
        limit = 0.75

        y = y0

        points: set = set()

        for x in range(x0, x1 + 1):
            if steep:
                self.glPoint(y, x, color or self.currColor)
                points.add((y, x))
            else:
                self.glPoint(x, y, color or self.currColor)
                points.add((x, y))

            offset += m
            if offset >= limit:
                if y0 < y1:
                    y += 1
                else:
                    y -= 1
                limit += 1
        return points

    def glPoligono(self, listadoPuntos: list):
        points: set = set()
        for i in range(len(listadoPuntos)):

            points.update(
                self.glLine(
                    v0=listadoPuntos[i],
                    v1=(listadoPuntos[(i + 1) % len(listadoPuntos)]),
                )
            )
        return points

    def glFill(self, points: set[tuple[int, int]]):
        points = list(points)

        sortedPoints = sorted(points, key=lambda point: (point[0], point[1]))

        for i in range(len(sortedPoints) - 1):
            if sortedPoints[i][0] == sortedPoints[i + 1][0]:
                for j in range(sortedPoints[i][1] + 1, sortedPoints[i + 1][1]):
                    # Menor X
                    puntoX = [
                        (x_i, y_i)
                        for (x_i, y_i) in sortedPoints
                        if x_i < sortedPoints[i][0] and y_i == j
                    ]
                    if len(puntoX) == 0:
                        break
                    # Mayor X
                    puntoX = [
                        (x_i, y_i)
                        for (x_i, y_i) in sortedPoints
                        if x_i > sortedPoints[i][0] and y_i == j
                    ]
                    if len(puntoX) == 0:
                        break
                    # Menor Y
                    puntoY = [
                        (x_i, y_i)
                        for (x_i, y_i) in sortedPoints
                        if x_i == sortedPoints[i][0] and y_i < j
                    ]
                    if len(puntoY) == 0:
                        break
                    # Mayor Y
                    puntoY = [
                        (x_i, y_i)
                        for (x_i, y_i) in sortedPoints
                        if x_i == sortedPoints[i][0] and y_i > j
                    ]
                    if len(puntoY) == 0:
                        break

                    self.glPoint(sortedPoints[i][0], j)

    def glGenerateFrameBuffer(self, filename):
        with open(filename, "wb") as file:
            file.write(char("B"))
            file.write(char("M"))
            file.write(dword(14 + 40 + ((self.width * self.height) * 3)))
            file.write(dword(0))
            file.write(dword(14 + 40))

            # Infoheader
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
                    color = self.frameBufer[x][y]
                    color = bytes([color[2], color[1], color[0]])

                    file.write(color)
