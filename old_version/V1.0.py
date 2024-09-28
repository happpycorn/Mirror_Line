import pygame as py
import cv2
from statistics import mean
from math import sin
from math import cos
from random import randrange
from cv2 import flip
from cv2 import resize
from cv2 import cvtColor

xsize = 1000
ysize = int(xsize*0.75)

py.init()
cap = cv2.VideoCapture(0)
mirro_screen = py.display.set_mode((xsize,ysize))
screen_rect = mirro_screen.get_rect()
mirro_screen.fill((255,255,255))
py.display.set_caption("mirro")

def setsc():
    global frame
    ret,frame = cap.read()
    frame = flip(frame,1)
    frame = resize(frame, (xsize,ysize))
    frame = cvtColor(frame,cv2.COLOR_BGR2GRAY)

def findcolor():

    ave = 0
    acolor = []

    for i in range(0,l,1):
        if (c>=0 and c<90) or (c>=180 and c<270):
            x1 = int(x+(cos(c)*i))
            y1 = int(y+(sin(c)*i))
            if 0<x1<xsize and 0<y1<ysize:
                acolor.append(frame[y1,x1])
            x1 = int(x-(cos(c)*i))
            y1 = int(y-(sin(c)*i))
            if 0<x1<xsize and 0<y1<ysize:
                acolor.append(frame[y1,x1])
        if (c>=90 and c<180) or (c>=270 and c<=360):
            x1 = int(x+(cos(c)*i))
            y1 = int(y-(sin(c)*i))
            if 0<x1<xsize and 0<y1<ysize:
                acolor.append(frame[y1,x1])
            x1 = int(x-(cos(c)*i))
            y1 = int(y+(sin(c)*i))
            if 0<x1<xsize and 0<y1<ysize:                
                acolor.append(frame[y1,x1])
    
    if len(acolor)!=0:
        ave = mean(acolor)
    
    return (ave,ave,ave)

def rrxy(inx,iny):
    global x,y,c,l
    x = inx+randrange(0,50)
    y = iny+randrange(0,50)
    c = randrange(0,360)
    l = randrange(0,25)

def x1y1():
    if (c>=0 and c<90) or (c>=180 and c<270):
        x1 = int(x+(cos(c)*l))
        y1 = int(y+(sin(c)*l))
    if (c>=90 and c<180) or (c>=270 and c<=360):
        x1 = int(x+(cos(c)*l))
        y1 = int(y-(sin(c)*l))
    return (x1,y1)

def x2y2():
    if (c>=0 and c<90) or (c>=180 and c<270):
        x2 = int(x-(cos(c)*l))
        y2 = int(y-(sin(c)*l))
    if (c>=90 and c<180) or (c>=270 and c<=360):
        x2 = int(x-(cos(c)*l))
        y2 = int(y+(sin(c)*l))
    return (x2,y2)

def draw():
    for i in range(0,xsize,50):
        for j in range(0,ysize,50):
            rrxy(i,j)
            py.draw.line(mirro_screen,findcolor(),x1y1(),x2y2(),5)

while True:
    setsc()
    draw()
    py.display.flip()
    for event in py.event.get():
        if event.type == py.QUIT:
            exit()