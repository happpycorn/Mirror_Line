# Import

import threading
import turtle as t
import pygame as py
from math import sin, cos
from statistics import mean
from cv2 import flip, resize, VideoCapture
from random import randrange, uniform

# Constant

XSIZE = 1000
YSIZE = int(XSIZE * 0.75)

width = 5
block = 100
length = 80
gray = False

coords = [(i, j) for i in range(0, XSIZE, block) for j in range(0, YSIZE, block)]

WORD_INFO = [(14, "偵率"), (22, "線長"), (30, "線寬")]

SCALEBAR_INFO = [(9, (220, 20, 60), block//10), (17, (0, 127, 255), length//10), (25, (50, 205, 50), width*2)]

BUTTON_INFO = [
    [0,  (100, 100, 100), 'Gray'],              #gray
    [10, (220, 20, 60),   (100, 100, 5)],       #red
    [20, (255, 140, 0),   (490, 490, 10)],      #org
    [30, (255, 219, 88),  (50, 30, 100)],      #yellow
    [40, (50, 205, 50),   (100, 10, 10)],        #green
    [50, (64, 224, 208),  (250, 250, 2)],       #lightblue
    [60, (0, 71, 171),    (50, 1, 100)],        #blue
    [70, (106, 90, 205),  (100, 3, 100)],       #blue and purple
    [80, (180, 0, 230),   (100, 3, 10)],        #purple
    [90, (238, 130, 238), (50, 20, 3)],         #lightpurple
]

# Setting

py.init()
cap = VideoCapture(0)
mirro_screen = py.display.set_mode((XSIZE, YSIZE))
py.display.set_caption("mirro")

controlor = t.Screen()
controlor.setup(470,160)
controlor.screensize(470,160)
controlor.setworldcoordinates(-10,32,100,0)
controlor.setup(500,170)
controlor.colormode(255)

t.delay(0)
t.speed(0)
t.tracer(0)

t.up()
t.pensize(3)
t.hideturtle()

# Define

class clicker:
        
    def __init__(self, x, y, color, width, height) -> None:

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, color, width, height):

        btn = t.clone()
        btn.goto(self.x, self.y)
        btn.color(color)
        btn.fillcolor(color)
        btn.pendown()
        btn.begin_fill()
        for _ in range(2):
            btn.forward(width)
            btn.left(90)
            btn.forward(height)
            btn.left(90)
        btn.end_fill()
    
    def isclick(self, x, y):
        return self.x<x<self.x+self.width and self.y<y<self.y+self.height

class Button(clicker):

    def __init__(self, x, color, setting) -> None:

        super().__init__(x, 1, color, 8, 6)
        self.setting = setting
        self.draw(self.color, self.width, self.height)

class ScaleBar(clicker):

    def __init__(self, y, color, oriduty) -> None:

        super().__init__(0, y, color, 98, 6)
        self.duty = oriduty
        self.draw(self.duty, self.color, self.width, self.height)

    def draw(self, duty, color, width, height):
        
        super().draw((100,100,100), width, height)
        super().draw(color, min(duty, width), height)

def click(x, y):

    global length, block, width, gray, coords

    oblock = block

    for btn in buttons:
        if not btn.isclick(x, y):
            continue

        if btn.setting == 'Gray':
            gray = not gray
            return
        
        block, length, width = btn.setting
        fps.draw(block//10, fps.color, fps.width, fps.height)
        long.draw(length//10, long.color, long.width, long.height)
        fat.draw(width*2, fat.color, fat.width, fat.height)

    if fps.isclick(x, y):
        block = int(x*10)
        fps.draw(block//10, fps.color, fps.width, fps.height)

    if long.isclick(x, y):
        length = int(x*10)
        long.draw(length//10, long.color, long.width, long.height)

    if fat.isclick(x, y):
        width = int(x/2)
        fat.draw(width*2, fat.color, fat.width, fat.height)
    
    if oblock!=block:
        coords = [(i, j) for i in range(0, XSIZE, block) for j in range(0, YSIZE, block)]
    
    t.update()

def write(y, word):
    wrt = t.clone()
    wrt.goto(-8, y)
    wrt.write(word, move=False, align='left', font=('Arial', 8, 'normal'))

def getFrame():

    ret, frame = cap.read()
    frame = flip(frame, 1)
    frame = resize(frame, (XSIZE, YSIZE))

    return frame

def draw(frame, i, j):

    x = i+randrange(0, block)
    y = j+randrange(0, block)
    c = uniform(0, 7)
    l = randrange(0, length)

    cos_c = cos(c)
    sin_c = sin(c)

    points = [(int(x + cos_c * i), int(y + sin_c * i)) for i in range(-l, l+1)]
    valid_points = [(x, y) for x, y in points if (0 < x < XSIZE and 0 < y < YSIZE)]

    if not valid_points:
        return
    
    rcolor, gcolor, bcolor = [], [], []

    for i, j in valid_points:
        bcolor.append(frame[j, i, 0])
        gcolor.append(frame[j, i, 1])
        rcolor.append(frame[j, i, 2])
    
    rave, gave, bave = mean(rcolor), mean(gcolor), mean(bcolor)

    if gray:
        ave = rave*0.2989 + gave * 0.5870 + bave * 0.1140
        rave, gave, bave = ave, ave, ave

    py.draw.line(
        mirro_screen, 
        (rave, gave, bave), 
        points[0], points[-1], width
        )

def main():
    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                exit()

        frame = getFrame()

        for i, j in coords:
            draw(frame, i, j)

        py.display.flip()

# Draw

for y, word in WORD_INFO:
    write(y, word)

fps = ScaleBar(*SCALEBAR_INFO[0])
long = ScaleBar(*SCALEBAR_INFO[1])
fat = ScaleBar(*SCALEBAR_INFO[2])

buttons = [Button(x, color, setting) for x, color, setting in BUTTON_INFO]

t.update()

# Main

p = threading.Thread(target=main)
p.start()

controlor.onclick(click)
t.mainloop()