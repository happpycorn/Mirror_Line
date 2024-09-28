import cv2
import turtle as t
import random as r
import math as m

cap = cv2.VideoCapture(0)
screen = t.Screen()
screen.setup(1280,960)
screen.setworldcoordinates(0,0,1280,960)
t.getscreen().colormode(255)
t.speed(0)
t.delay(0)
t.tracer(False)
t.isvisible()

while True:
    ret,frame = cap.read()
    frame = cv2.resize(frame, (1280,960))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.flip(frame,1)
    color = []

    x = r.randrange(0,1180)
    y = r.randrange(0,860)
    c = r.randrange(0,360)
    l = r.randrange(0,100)
    c = m.radians(c)

    for i in range(0,l,1):
        if (c>=0 and c<90) or (c>=180 and c<270):
            x1 = int(x+(m.cos(c)*i))
            y1 = int(y+(m.sin(c)*i))
            color.append(frame[y1,x1])
            x1 = int(x-(m.cos(c)*i))
            y1 = int(y-(m.sin(c)*i))
            color.append(frame[y1,x1])
        if (c>=90 and c<180) or (c>=270 and c<=360):
            x1 = int(x+(m.cos(c)*i))
            y1 = int(y-(m.sin(c)*i))
            color.append(frame[y1,x1])
            x1 = int(x-(m.cos(c)*i))
            y1 = int(y+(m.sin(c)*i))
            color.append(frame[y1,x1])

    sum = 0
    for i in color:
        sum += i
    
    t.up()

    if (c>=0 and c<90) or (c>=180 and c<270):
        x1 = int(x+(m.cos(c)*l))
        y1 = int(y+(m.sin(c)*l))
        x2 = int(x-(m.cos(c)*l))
        y2 = int(y-(m.sin(c)*l))
    if (c>=90 and c<180) or (c>=270 and c<=360):
        x1 = int(x+(m.cos(c)*l))
        y1 = int(y-(m.sin(c)*l))
        x2 = int(x-(m.cos(c)*l))
        y2 = int(y+(m.sin(c)*l))

    if len(color)!=0:
        ave = int(sum/len(color))
    t.color(ave,ave,ave)
    t.goto(x1,y1)
    t.down()
    t.goto(x2,y2)

    t.update()