import pygame as py
import cv2
from statistics import mean
from math import sin
from math import cos
from random import randrange
from cv2 import flip
from cv2 import resize
from pygame.locals import *
from pygame import MOUSEBUTTONDOWN
from pygame import QUIT

xsize = 900
ysize = int(xsize*0.75)+90

part = 50
line = 200
penfat = 5
rect_height = 30

def create_scales(height, joints_num=3):

    surface_list = []
    for _ in range(joints_num):
        surface = py.surface.Surface((xsize,height))
        surface_list.append(surface)

    for x in range(xsize):
        co = int((x/xsize)*100+55)
        red = (co+100,co+30,co+30)
        green = (co,co+100,co+50)
        blue = (co+30,co,co+100)
        color_list = [red, green, blue]
        line_rect = Rect(x,0,1,height)
        for i in range(joints_num):
            py.draw.rect(surface_list[i], color_list[i], line_rect)

    return surface_list

def drawText(screen,text,posx,posy,textHeight=15,fontColor=(0,0,0),backgroudColor=(255,255,255)):
    fontObj = py.font.Font('freesansbold.ttf', textHeight)
    textSurfaceObj = fontObj.render(text, True,fontColor,backgroudColor)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (posx, posy)
    screen.blit(textSurfaceObj, textRectObj)


py.init()
cap = cv2.VideoCapture(0)
mirro_screen = py.display.set_mode((xsize,ysize))
screen_rect = mirro_screen.get_rect()
mirro_screen.fill((255,255,255))
py.display.set_caption("mirro")
surface_list = create_scales(rect_height, joints_num=3)
color=[127,63,127]
joint_list = [50,25,5]
max_list = [100,100,10]
txt_font = py.font.SysFont(None,48)
txt_image = txt_font.render(' Happy mode ',True,(0,0,0),(255,255,255))
txt_rect = txt_image.get_rect()
txt_rect.x = 20
txt_rect.y = 120
happymode = False


def setsc():
    global frame
    ret,frame = cap.read()
    frame = flip(frame,1)
    frame = resize(frame, (xsize,ysize-90))

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

def rrxy(inx,iny):
    global x,y,c,l
    x = inx+randrange(0,part)
    y = iny+randrange(0,part)
    c = randrange(0,360)
    l = randrange(0,line)

def x1y1():
    if (c>=0 and c<90) or (c>=180 and c<270):
        x1 = int(x+(cos(c)*l))
        y1 = int(y+(sin(c)*l))+90
    if (c>=90 and c<180) or (c>=270 and c<=360):
        x1 = int(x+(cos(c)*l))
        y1 = int(y-(sin(c)*l))+90
    return (x1,y1)

def x2y2():
    if (c>=0 and c<90) or (c>=180 and c<270):
        x2 = int(x-(cos(c)*l))
        y2 = int(y-(sin(c)*l))+90
    if (c>=90 and c<180) or (c>=270 and c<=360):
        x2 = int(x-(cos(c)*l))
        y2 = int(y+(sin(c)*l))+90
    return (x2,y2)

def draw():
    for i in range(0,xsize,part):
        for j in range(0,ysize,part):
            rrxy(i,j)
            py.draw.line(mirro_screen,findcolor(),x1y1(),x2y2(),penfat)

while True:
    setsc()
    draw()
    py.draw.rect(mirro_screen, (100, 100, 100), txt_rect)
    mirro_screen.blit(txt_image, txt_rect)
    py.display.flip()

    for i, surface in enumerate(surface_list):
        mirro_screen.blit(surface,(0, rect_height*i))

    x, y=py.mouse.get_pos()

    if py.mouse.get_pressed()[0]:            
        for component in range(3):
            if y > component*rect_height and y < (component+1)*rect_height:
                color[component] = int((x/(xsize-1))*255)            
    for component in range(3):
        pos = ( int((color[component]/255)*(xsize-1)), component*rect_height+rect_height//2 )
        py.draw.circle(mirro_screen, (255, 255, 255), pos[:3], rect_height//2)           
        joint_list[component] = int(round(max_list[component] * (pos[0])/xsize))
        drawText(mirro_screen, str(joint_list[component]), pos[0], pos[1])

    part = abs(joint_list[0])+10
    line = abs(joint_list[1])+1
    penfat = abs(joint_list[2])

    for event in py.event.get():
        if event.type == QUIT:
            exit()
        if event.type == MOUSEBUTTONDOWN:
            if happymode:
                happymode = True if not txt_rect.collidepoint(event.pos) else False
            else:
                happymode = True if txt_rect.collidepoint(event.pos) else False
    
    if happymode:
        penfat = 100
        txt_image = txt_font.render(' Normal mode ',True,(0,0,0),(255,255,255))
    else:
        txt_image = txt_font.render(' Happy mode ',True,(0,0,0),(255,255,255))