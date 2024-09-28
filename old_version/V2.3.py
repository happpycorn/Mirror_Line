import cv2
import numpy as np
from math import sin, cos
from statistics import mean
from random import randrange

class MirroDrawer:
    def __init__(self, xsize=1200, ysize=900, part=100, line=100, penfat=5):
        self.xsize = xsize
        self.ysize = ysize
        self.part = part
        self.line = line
        self.penfat = penfat
        self.canvas = np.zeros((self.ysize,self.xsize,3),dtype=np.uint8)

        self.cap = cv2.VideoCapture(0)
        self.mirro_screen = cv2.namedWindow("mirro", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("mirro", self.xsize, self.ysize)

    def set_camera(self):
        ret, self.frame = self.cap.read()
        self.frame = cv2.flip(self.frame, 1)
        self.frame = cv2.resize(self.frame, (self.xsize, self.ysize))

    def find_color(self, x, y, c, l):
        rcolor, gcolor, bcolor = [], [], []

        for i in range(0, l, 1):
            x1 = int(x + (cos(c) * i))
            y1 = int(y + (sin(c) * i))
            if 0 < x1 < self.xsize and 0 < y1 < self.ysize:
                bcolor.append(self.frame[y1, x1, 0])
                gcolor.append(self.frame[y1, x1, 1])
                rcolor.append(self.frame[y1, x1, 2])

            x1 = int(x - (cos(c) * i))
            y1 = int(y - (sin(c) * i))
            if 0 < x1 < self.xsize and 0 < y1 < self.ysize:
                bcolor.append(self.frame[y1, x1, 0])
                gcolor.append(self.frame[y1, x1, 1])
                rcolor.append(self.frame[y1, x1, 2])

        r = int(mean(rcolor)) if len(rcolor) != 0 else 0
        g = int(mean(gcolor)) if len(gcolor) != 0 else 0
        b = int(mean(bcolor)) if len(bcolor) != 0 else 0

        return b, g, r

    def randomize_position(self, i, j):
        x = i + randrange(0, self.part)
        y = j + randrange(0, self.part)
        c = randrange(0, 360)
        l = randrange(0, self.line)
        return x, y, c, l

    def draw_lines(self):
        for i in range(0, self.xsize, self.part):
            for j in range(0, self.ysize, self.part):
                x, y, c, l = self.randomize_position(i, j)
                color = self.find_color(x, y, c, l)
                cv2.line(self.canvas, self.get_point1(x, y, c, l), self.get_point2(x, y, c, l), color, self.penfat)
        
    def get_point1(self, x, y, c, l):
        x1 = int(x + cos(c) * l) if 0 <= c < 90 or 180 <= c < 270 else int(x - cos(c) * l)
        y1 = int(y + sin(c) * l) if 0 <= c < 90 or 180 <= c < 270 else int(y - sin(c) * l)
        return x1, y1

    def get_point2(self, x, y, c, l):
        x2 = int(x - cos(c) * l) if 0 <= c < 90 or 180 <= c < 270 else int(x + cos(c) * l)
        y2 = int(y - sin(c) * l) if 0 <= c < 90 or 180 <= c < 270 else int(y + sin(c) * l)
        return x2, y2

    def run(self):
        while True:
            self.set_camera()
            self.draw_lines()
            cv2.imshow("mirro", self.canvas)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    drawer = MirroDrawer()
    drawer.run()