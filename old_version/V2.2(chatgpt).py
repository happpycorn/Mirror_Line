import os
import cv2
import threading
import turtle as t
import pygame as py
from math import sin, cos
from cv2 import flip, resize
from statistics import mean
from random import randrange

# Constants
GRAY = (100, 100, 100)
RED = (220, 20, 60)
BLUE = (0, 127, 255)
GREEN = (50, 205, 50)

XSIZE = 1200
YSIZE = int(XSIZE * 0.75)

PART = 100
LINE = 100
PENFAT = 5
BLACKWHITE = False

BUTTON_INFO = [
    [0,5,GRAY],                           #GRAY
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

# Pygame initialization
py.init()
cap = cv2.VideoCapture(0)
mirro_screen = py.display.set_mode((XSIZE, YSIZE - 90))
screen_rect = mirro_screen.get_rect()
mirro_screen.fill((255,255,255))
py.display.set_caption("mirro")

# Turtle graphics setup
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

def write(x, y, word):
    wrt = t.clone()
    wrt.up()
    wrt.goto(x, y)
    wrt.write(word, move=False, align='left', font=('Arial', 8, 'normal'))

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
    button(BUTTON_INFO[i][0],BUTTON_INFO[i][1],BUTTON_INFO[i][2])

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

longline(45,GRAY)
longline(85,GRAY)
longline(125,GRAY)

def draw_inline(y,color,long):
    btn = t.clone()
    btn.penup()
    btn.color(GRAY)
    btn.fillcolor(GRAY)
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

draw_inline(45,RED,PART)
draw_inline(85,BLUE,LINE)
draw_inline(125,GREEN,PENFAT*49)

t.update()

def set_camera():
    global frame
    ret, frame = cap.read()
    frame = flip(frame, 1)
    frame = resize(frame, (XSIZE, YSIZE))

def find_color():
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
            if 0<x1<XSIZE and 0<y1<YSIZE-90:
                bcolor.append(frame[y1,x1,0])
                gcolor.append(frame[y1,x1,1])
                rcolor.append(frame[y1,x1,2])
            x1 = int(x-(cos(c)*i))
            y1 = int(y-(sin(c)*i))
            if 0<x1<XSIZE and 0<y1<YSIZE-90:
                bcolor.append(frame[y1,x1,0])
                gcolor.append(frame[y1,x1,1])
                rcolor.append(frame[y1,x1,2])
        if (c>=90 and c<180) or (c>=270 and c<=360):
            x1 = int(x+(cos(c)*i))
            y1 = int(y-(sin(c)*i))
            if 0<x1<XSIZE and 0<y1<YSIZE-90:
                bcolor.append(frame[y1,x1,0])
                gcolor.append(frame[y1,x1,1])
                rcolor.append(frame[y1,x1,2])
            x1 = int(x-(cos(c)*i))
            y1 = int(y+(sin(c)*i))
            if 0<x1<XSIZE and 0<y1<YSIZE-90:                
                bcolor.append(frame[y1,x1,0])
                gcolor.append(frame[y1,x1,1])
                rcolor.append(frame[y1,x1,2])
    
    if len(rcolor)!=0:
        rave = mean(rcolor)

    if len(gcolor)!=0:
        gave = mean(gcolor)
    
    if len(bcolor)!=0:
        bave = mean(bcolor)
    
    if BLACKWHITE:
        ave = rave*0.2989 + gave * 0.5870 + bave * 0.1140
        rave,gave,bave = ave,ave,ave
    
    return (rave,gave,bave)

def randomize_position(i,j):
    global x, y, c, l
    x = i+randrange(0, PART)
    y = j+randrange(0, PART)
    c = randrange(0, 360)
    l = randrange(0, LINE)

def draw_lines():
    for i in range(0, XSIZE, PART):
        for j in range(0, YSIZE - 90, PART):
            randomize_position(i,j)
            py.draw.line(mirro_screen, find_color(), get_point1(), get_point2(), PENFAT)

def get_point1():
    if 0 <= c < 90 or 180 <= c < 270:
        x1 = int(x + cos(c) * l)
        y1 = int(y + sin(c) * l)
    else:
        x1 = int(x - cos(c) * l)
        y1 = int(y - sin(c) * l)
    return x1, y1

def get_point2():
    if 0 <= c < 90 or 180 <= c < 270:
        x2 = int(x - cos(c) * l)
        y2 = int(y - sin(c) * l)
    else:
        x2 = int(x + cos(c) * l)
        y2 = int(y + sin(c) * l)
    return x2, y2

def click_handler(x, y):
    global PART, LINE, PENFAT, BLACKWHITE

    x, y = int(x), int(y)

    if 5 < y < 35:
        if 0 < x < 40:
            BLACKWHITE = not BLACKWHITE
        for c in range(1, 10):
            if BUTTON_INFO[c][0] < x < BUTTON_INFO[c][0] + 40:
                PART, LINE, PENFAT = BUTTON_INFO[c][3], BUTTON_INFO[c][4], BUTTON_INFO[c][5]
                draw_inline(45, RED, PART)
                draw_inline(85, BLUE, LINE)
                draw_inline(125, GREEN, 490 if PENFAT * 49 > 490 else PENFAT * 49)
    if 45 < y < 75 and 0 < x < 490:
        PART = x
        draw_inline(45, RED, x)
    if 85 < y < 115 and 0 < x < 490:
        LINE = x
        draw_inline(85, BLUE, x)
    if 125 < y < 155 and 0 < x < 490:
        PENFAT = int(x / 49)
        draw_inline(125, GREEN, x)

    t.update()

def main_loop():
    while True:
        set_camera()
        draw_lines()
        py.display.flip()
        for event in py.event.get():
            if event.type == py.QUIT:
                os._exit(0)

# Multithreading
p = threading.Thread(target=main_loop)
p.start()

window.onclick(click_handler)
t.mainloop()
