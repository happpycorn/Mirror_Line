import cv2
import pygame as py
from math import sin, cos
from cv2 import flip, resize
from statistics import mean
from random import randrange, uniform

XSIZE = 1200
YSIZE = int(XSIZE * 0.75)

width = 5
block = 100
length = 75

coords = [(i, j) for i in range(0, XSIZE, block) for j in range(0, YSIZE, block)]

py.init()
cap = cv2.VideoCapture(0)
mirro_screen = py.display.set_mode((XSIZE, YSIZE))
py.display.set_caption("mirro")

def set_camera():

    ret, frame = cap.read()
    frame = flip(frame, 1)
    frame = resize(frame, (XSIZE, YSIZE))

    return frame

def draw(frame, i, j):

    x = i+randrange(0, block)
    y = j+randrange(0, block)
    c = uniform(0, 7)
    l = randrange(1, length)

    cos_c = cos(c)
    sin_c = sin(c)

    points = [(int(x + cos_c * i), int(y + sin_c * i)) for i in range(-l, l)]
    valid_points = [(x, y) for x, y in points if (0 < x < XSIZE and 0 < y < YSIZE)]

    if not valid_points:
        return
    
    rcolor, gcolor, bcolor = [], [], []

    for i, j in valid_points:
        bcolor.append(frame[j, i, 0])
        gcolor.append(frame[j, i, 1])
        rcolor.append(frame[j, i, 2])

    py.draw.line(
        mirro_screen, 
        (mean(rcolor), mean(gcolor), mean(bcolor)), 
        points[0], points[-1], width
        )

while True:
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            exit()

    frame = set_camera()

    for i, j in coords:
        draw(frame, i, j)

    py.display.flip()