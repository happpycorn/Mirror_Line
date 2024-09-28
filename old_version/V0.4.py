import cv2
import pygame as py
from math import sin
from math import cos
from statistics import mean
from xyc import xy
from xyc import random
from cv2 import flip
from cv2 import resize
from cv2 import imshow
from cv2 import cvtColor
from cv2 import COLOR_BGR2GRAY
from sys import exit

xsize = 1000
ysize = int(xsize*0.75)

cap = cv2.VideoCapture(0)
py.init()
mirro_screen = py.display.set_mode((xsize,ysize))
screen_rect = mirro_screen.get_rect()

py.display.set_caption("mirro")

def set():
    global frame,x,y,c,l,x1,y1,x2,y2
    ret,frame = cap.read()
    frame = cvtColor(frame, COLOR_BGR2GRAY)
    frame = flip(frame,1)
    frame = resize(frame, (256,192))
    imshow("frame",frame)
    frame = resize(frame, (xsize,ysize))
    x,y,c,l = random(xsize,ysize)
    x1,y1,x2,y2 = xy(x,y,c,l)

def avecolor(x,y,c,l):

    color = []

    for i in range(0,l,1):
        if (c>=0 and c<90) or (c>=180 and c<270):
            x1 = int(x+(cos(c)*i))
            y1 = int(y+(sin(c)*i))
            if 0<x1<xsize and 0<y1<ysize:
                color.append(frame[y1,x1])
            x1 = int(x-(cos(c)*i))
            y1 = int(y-(sin(c)*i))
            if 0<x1<xsize and 0<y1<ysize:
                color.append(frame[y1,x1])
        if (c>=90 and c<180) or (c>=270 and c<=360):
            x1 = int(x+(cos(c)*i))
            y1 = int(y-(sin(c)*i))
            if 0<x1<xsize and 0<y1<ysize:
                color.append(frame[y1,x1])
            x1 = int(x-(cos(c)*i))
            y1 = int(y+(sin(c)*i))
            if 0<x1<xsize and 0<y1<ysize:
                color.append(frame[y1,x1])
    if len(color)!=0:
        ave = mean(color)
    return ave

def draw(ave):

    py.draw.line(mirro_screen,(ave,ave,ave),(x1, y1),(x2,y2),5)
    py.display.flip()


while True:

    set()

    draw(avecolor(x,y,c,l))

    for event in py.event.get():
        if event.type == py.QUIT:
            exit()