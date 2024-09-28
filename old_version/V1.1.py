import pygame as py
import cv2
from statistics import mean
from math import sin
from math import cos
from random import randrange
from cv2 import flip
from cv2 import resize

xsize = 1000
ysize = int(xsize*0.75)

part = 100
line = 50
penfat = 5

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

def rrxy(inx,iny):
    global x,y,c,l
    x = inx+randrange(0,part)
    y = iny+randrange(0,part)
    c = randrange(0,360)
    l = randrange(line-1,line)

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

def findcolor():

    rave = 0
    bave = 0
    gave = 0

    rcolor = []
    gcolor = []
    bcolor = []

    for i in range(0,l+1,1):
        if (c>=0 and c<90) or (c>=180 and c<270):
            x1 = int(x+(cos(c)*i))
            y1 = int(y+(sin(c)*i))
            if 0<x1<xsize and 0<y1<ysize:
                bcolor.append(frame[y1,x1,0])
                gcolor.append(frame[y1,x1,1])
                rcolor.append(frame[y1,x1,2])
            x1 = int(x-(cos(c)*i))
            y1 = int(y-(sin(c)*i))
            if 0<x1<xsize and 0<y1<ysize:
                bcolor.append(frame[y1,x1,0])
                gcolor.append(frame[y1,x1,1])
                rcolor.append(frame[y1,x1,2])
        if (c>=90 and c<180) or (c>=270 and c<=360):
            x1 = int(x+(cos(c)*i))
            y1 = int(y-(sin(c)*i))
            if 0<x1<xsize and 0<y1<ysize:
                bcolor.append(frame[y1,x1,0])
                gcolor.append(frame[y1,x1,1])
                rcolor.append(frame[y1,x1,2])
            x1 = int(x-(cos(c)*i))
            y1 = int(y+(sin(c)*i))
            if 0<x1<xsize and 0<y1<ysize:                
                bcolor.append(frame[y1,x1,0])
                gcolor.append(frame[y1,x1,1])
                rcolor.append(frame[y1,x1,2])
    
    if len(rcolor)!=0:
        rave = mean(rcolor)

    if len(gcolor)!=0:
        gave = mean(gcolor)
    
    if len(bcolor)!=0:
        bave = mean(bcolor)
    
    return (rave,gave,bave)

def draw():
    for i in range(0,xsize,part):
        for j in range(0,ysize,part):
            rrxy(i,j)
            py.draw.line(mirro_screen,findcolor(),x1y1(),x2y2(),penfat)

while True:
    setsc()
    draw()
    py.display.flip()
    for event in py.event.get():
        if event.type == py.QUIT:
            exit()