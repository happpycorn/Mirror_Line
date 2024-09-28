import cv2
import turtle as t
import random as r
import math as m
import statistics
import xyc

cap = cv2.VideoCapture(0)
screen = t.Screen()
screen.setup(1280,960)
screen.setworldcoordinates(1280,960,0,0)
t.getscreen().colormode(255)
t.speed(0)
t.delay(0)
t.tracer(False)
t.pensize(5)

def set():
    global frame,x,y,c,l,x1,y1,x2,y2
    ret,frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.flip(frame,1)
    frame = cv2.resize(frame, (256,192))
    cv2.imshow("frame",frame)
    frame = cv2.flip(frame,1)
    frame = cv2.resize(frame, (1280,960))
    x,y,c,l = xyc.random()
    x1,y1,x2,y2 = xyc.xy(x,y,c,l)

def avecolor(x,y,c,l):
    global color,ave

    color = []

    for i in range(0,l,1):
        if (c>=0 and c<90) or (c>=180 and c<270):
            x1 = int(x+(m.cos(c)*i))
            y1 = int(y+(m.sin(c)*i))
            if x1<1280 and y1<960:
                color.append(frame[y1,x1])
            x1 = int(x-(m.cos(c)*i))
            y1 = int(y-(m.sin(c)*i))
            if x1<1280 and y1<960:
                color.append(frame[y1,x1])
        if (c>=90 and c<180) or (c>=270 and c<=360):
            x1 = int(x+(m.cos(c)*i))
            y1 = int(y-(m.sin(c)*i))
            if x1<1280 and y1<960:
                color.append(frame[y1,x1])
            x1 = int(x-(m.cos(c)*i))
            y1 = int(y+(m.sin(c)*i))
            if x1<1280 and y1<960:
                color.append(frame[y1,x1])
    if len(color)!=0:
        ave = statistics.mean(color)

def draw():

    t.up()
    t.color(ave,ave,ave)
    t.goto(x1,y1)
    t.down()
    t.goto(x2,y2)

    t.update()



while True:

    set()

    avecolor(x,y,c,l)

    draw()


