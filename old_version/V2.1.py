import cv2
import turtle as t
from math import sin
from math import cos
from cv2 import flip
from turtle import up
from cv2 import resize
from turtle import down
from turtle import goto
from turtle import update
from turtle import pensize
from turtle import pencolor
from statistics import mean
from random import randrange

xsize = 800
ysize = int(xsize*0.75)

part = 100
line = 100
penfat = 5

cap = cv2.VideoCapture(0)
screen = t.Screen()
screen.setup(xsize,ysize)
screen.setworldcoordinates(xsize,ysize-100,0,0)
t.getscreen().colormode(255)
t.speed(0)
t.delay(0)
t.tracer(False)
t.pensize(penfat)
t.up()

def findframe():
    global frame
    ret,frame = cap.read()
    frame = flip(frame,1)
    frame = resize(frame, (xsize,ysize-90))

def rrxy(inx,iny):
    global x,y,c,l
    x = inx+randrange(0,part)
    y = iny+randrange(0,part)
    c = randrange(0,360)
    l = randrange(0,line)

def x1y1():
    if (c>=0 and c<90) or (c>=180 and c<270):
        x1 = int(x+(cos(c)*l))
        y1 = int(y+(sin(c)*l))
    if (c>=90 and c<180) or (c>=270 and c<=360):
        x1 = int(x+(cos(c)*l))
        y1 = int(y-(sin(c)*l))
    return x1,y1

def x2y2():
    if (c>=0 and c<90) or (c>=180 and c<270):
        x2 = int(x-(cos(c)*l))
        y2 = int(y-(sin(c)*l))
    if (c>=90 and c<180) or (c>=270 and c<=360):
        x2 = int(x-(cos(c)*l))
        y2 = int(y+(sin(c)*l))
    return x2,y2

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
            if 0<x1<xsize and 0<y1<ysize-90:
                bcolor.append(frame[y1,x1,0])
                gcolor.append(frame[y1,x1,1])
                rcolor.append(frame[y1,x1,2])
            x1 = int(x-(cos(c)*i))
            y1 = int(y-(sin(c)*i))
            if 0<x1<xsize and 0<y1<ysize-90:
                bcolor.append(frame[y1,x1,0])
                gcolor.append(frame[y1,x1,1])
                rcolor.append(frame[y1,x1,2])
        if (c>=90 and c<180) or (c>=270 and c<=360):
            x1 = int(x+(cos(c)*i))
            y1 = int(y-(sin(c)*i))
            if 0<x1<xsize and 0<y1<ysize-90:
                bcolor.append(frame[y1,x1,0])
                gcolor.append(frame[y1,x1,1])
                rcolor.append(frame[y1,x1,2])
            x1 = int(x-(cos(c)*i))
            y1 = int(y+(sin(c)*i))
            if 0<x1<xsize and 0<y1<ysize-90:                
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
        for j in range(0,ysize-part,part):
            rrxy(i,j)
            pencolor(findcolor())
            pensize(penfat)
            goto(x1y1())
            down()
            goto(x2y2())
            up()

while True:
    findframe()
    draw()
    update()