import pygame, random, sys, math
from random import randint
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((510, 510))

locale = [255, 255]
clock = pygame.time.Clock()
launch = 0
shrek = 0
autumn = 0

def jump(locale):
    tempx = pygame.mouse.get_pos()[0]-locale[0]
    tempy = pygame.mouse.get_pos()[1]-locale[1]
    dire = int(math.atan(abs(tempy/tempx)) *180/math.pi)
    posx = int(tempx/abs(tempx))
    posy = int(-1*tempy/abs(tempy))
    
    if posx == -1 and posy == 1:
        dire = 180-dire
    if posx == -1 and posy == -1:
        dire += 180
    if posx == 1 and posy == -1:
        dire = 360 - dire

    return(dire)

class wraith:
    def __init__(self, direction, lastwraith):
        if lastwraith == -1:
            self.direction = -1
            self.power = 1.6
        else:
            self.direction = direction
            self.power = math.log(lastwraith, 1.3)+14.786
            
    def tick(self, locale):
        temp = locale
        if not self.direction == -1:
            temp[0] += self.power*math.cos(self.direction*math.pi/180*-1)
            temp[1] += self.power*math.sin(self.direction*math.pi/180*-1)
            self.power -= 1
        return temp
        
    def tale(self):
        return self.power

motion = [wraith(0, -1)]


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            break
        if event.type == pygame.MOUSEBUTTONUP:
            if not launch:
                autumn = 0
                shrek = 0
                for i in motion:
                    temp = i.tale()
                    if temp > shrek:
                        shrek = temp
                motion.append(wraith(jump(locale), shrek))
            launch = 1
        else:
            launch = 0
            
    doom = []
    for i in range(len(motion)):
        locale = motion[i].tick(locale)
        if motion[i].tale() <= 0:
            doom.append(i)
    for i in doom:
        motion.pop(i)
        if len(doom) >= 1:
            for i in doom:
                i -= 1
    
    if locale[1] < 485:
        autumn += 1
        locale[1] += autumn
    if locale[1] >= 485:
        autumn = 0
        if locale[1] > autumn:
            locale[1] = 485
    
    pygame.display.set_caption(str(shrek)+"   "+str(motion))
    clock.tick(15)
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (255, 255, 255), (int(locale[0]), int(locale[1])), 6)
    pygame.display.update()