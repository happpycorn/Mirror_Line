import os
import cv2
import threading
import turtle as t
import pygame as py
from math import sin
from math import cos
from cv2 import flip
from cv2 import resize
from statistics import mean
from random import randrange

gray = (100,100,100)
red = (220, 20, 60)
blue = (0, 127, 255)
green = (50, 205, 50)

xsize = 1200
ysize = int(xsize*0.75)

part = 100
line = 100
penfat = 5
blackwhite = False

buttoninfo = [
    [0,5,gray],                           #gray
    [50,5,(220, 20, 60),100,100,5],       #red
    [100,5,(255, 140, 0),490,490,10],     #org
    [150,5,(255, 219, 88),100,30,100],    #yellow
    [200,5, (50, 205, 50),50,10,10],      #green
    [250,5,(64, 224, 208),250,250,2],     #lightblue
    [300,5,(0, 71, 171),50,1,100],        #blue
    [350,5,(106, 90, 205),100,3,100],     #blue and purple
    [400,5,(180, 0, 230),100,3,10],       #purple
    [450,5,(238, 130, 238),50,20,3],      #lightpurple
]

py.init()
cap = cv2.VideoCapture(0)
mirro_screen = py.display.set_mode((xsize,ysize-90))
screen_rect = mirro_screen.get_rect()
mirro_screen.fill((255,255,255))
py.display.set_caption("mirro")

window = t.Screen()
window.setup(470,160)
window.screensize(470,160)
window.setworldcoordinates(-50,160,500,0)
window.setup(500,170)
window.colormode(255)
t.delay(0)
t.speed(0)
t.hideturtle()
t.tracer(0)

def write(x,y,word):
    wrt = t.clone()
    wrt.up()
    wrt.goto(x,y)
    wrt.write(word,move=False, align='left', font=('Arial', 8, 'normal'))

write(-40,70,"偵率")
write(-40,110,"線長")
write(-40,150,"線寬")

def button(x,y,color):
    btn = t.clone()
    btn.penup()
    btn.goto(x, y)
    btn.color(color)
    btn.fillcolor(color)
    btn.pensize(3)
    btn.pendown()
    btn.begin_fill()
    for i in range(2):
        btn.forward(40)
        btn.left(90)
        btn.forward(30)
        btn.left(90)
    btn.end_fill()
    btn.hideturtle()

for i in range(0,10):
    button(buttoninfo[i][0],buttoninfo[i][1],buttoninfo[i][2])

def longline(y,color):
    btn = t.clone()
    btn.penup()
    btn.goto(0, y)
    btn.color(color)
    btn.fillcolor(color)
    btn.pensize(3)
    btn.pendown()
    btn.begin_fill()
    for i in range(2):
        btn.forward(490)
        btn.left(90)
        btn.forward(30)
        btn.left(90)
    btn.end_fill()
    btn.hideturtle()

longline(45,gray)
longline(85,gray)
longline(125,gray)

def inline(y,color,long):
    btn = t.clone()
    btn.penup()
    btn.color(gray)
    btn.fillcolor(gray)
    btn.pensize(3)
    btn.goto(long,y)
    btn.pendown()
    btn.begin_fill()
    for i in range(2):
        btn.forward(490-long)
        btn.left(90)
        btn.forward(30)
        btn.left(90)
    btn.end_fill()
    btn.color(color)
    btn.fillcolor(color)
    btn.up()
    btn.goto(0,y)
    btn.down()
    btn.begin_fill()
    for i in range(2):
        btn.forward(long)
        btn.left(90)
        btn.forward(30)
        btn.left(90)
    btn.end_fill()
    btn.up()

    btn.hideturtle()

inline(45,red,part)
inline(85,blue,line)
inline(125,green,penfat*49)

t.update()

def setsc():
    global frame
    ret,frame = cap.read()
    frame = flip(frame,1)
    frame = resize(frame, (xsize,ysize))

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
    
    if blackwhite:
        ave = rave*0.2989 + gave * 0.5870 + bave * 0.1140
        rave,gave,bave = ave,ave,ave
    
    return (rave,gave,bave)

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
    for i in range(0,xsize,part):
        for j in range(0,ysize-90,part):
            rrxy(i,j)
            py.draw.line(mirro_screen,findcolor(),x1y1(),x2y2(),penfat)

def click(x,y):
    global part,line,penfat,blackwhite

    x = int(x)
    y = int(y)

    if 5 < y < 35:
        if 0 < x < 40:
            blackwhite = False if blackwhite else True            
        for c in range(1,10):
            if buttoninfo[c][0] < x < buttoninfo[c][0]+40:
                part = buttoninfo[c][3]
                line = buttoninfo[c][4]
                penfat = buttoninfo[c][5]
                inline(45,red,part)
                inline(85,blue,line)
                inline(125,green,490 if penfat*49>490 else penfat*49)
    if 45 < y < 75 and 0 < x < 490:
        part = x
        inline(45,red,x)
    if 85 < y < 115 and 0 < x < 490:
        line = x
        inline(85,blue,x)
    if 125 < y < 155 and 0 < x < 490:
        penfat = int(x/49)
        inline(125,green,x)

    t.update()

def whiletrue():
    while True:
        setsc()
        draw()
        py.display.flip()
        for event in py.event.get():
            if event.type == py.QUIT:
                os._exit(0)

p = threading.Thread(target=whiletrue)

p.start()

window.onclick(click)
t.mainloop()
