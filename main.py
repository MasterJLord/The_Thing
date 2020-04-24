import pygame, random, sys, math
from random import randint
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((510, 510))

locale = [255, 255]
bulletinboard = []
clock = pygame.time.Clock()
launch = 0
shrek = 0
autumn = 0
Helth = [15]

def jump(locale, target):
    tempx =target[0]-locale[0]
    tempy = target[1]-locale[1]
    if tempy == 0:
        if tempx >= 0:
            dire = 0
        else:
            dire = 180
    elif tempx == 0:
        if tempy >= 0:
            dire = 90
        else:
            dire = 270
    else:
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

def dist(pointA, pointB):
    return(((pointA[0]-pointB[0])**2+(pointA[0]-pointB[0])**2)**(0.5))

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
    
class rocket:
    def __init__(self, coordinates, initial):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.age = 0
        self.dir = initial
        
    def tick(self):
        iddir = jump((self.x, self.y), locale)
        tempdir = self.dir - 180
        tempbool = False
        if tempdir < 0:
            tempdir += 360
            tempbool = True
        if tempbool:
            if iddir < self.dir or iddir > tempdir:
                self.dir -= 7
            elif not self.dir == iddir:
                self.dir += 7
        else:
            if iddir > self.dir or iddir < tempdir:
                self.dir += 7
            elif not self.dir == iddir:
                self.dir -= 7
        if self.dir >= 360:
            self.dir -= 360
        if self.dir < 0:
            self.dir += 360
        pygame.draw.circle(screen, (255, 205, 210), (int(self.x), int(self.y)), 2)
        self.x += math.cos(self.dir*math.pi/180)*9
        self.y -= math.sin(self.dir*math.pi/180)*9
        pygame.draw.circle(screen, (255,225,230), (int(self.x), int(self.y)), 2)
        self.x += math.cos(self.dir*math.pi/180)*9
        self.y -= math.sin(self.dir*math.pi/180)*9
        pygame.draw.circle(screen, (255, 235, 240), (int(self.x), int(self.y)), 3)
        self.age += 1
        if self.age >= 121 or dist(locale, (self.x, self.y)) <= 5:
            return True
        else:
            return False
        
    def expire(self):
        bulletinboard.append(blast((self.x, self.y)))
        return True
    
class blast:
    def __init__(self, site):
        self.x = site[0]
        self.y = site[1]
        self.fuse = 1
        self.size = 14
        self.age = 0
        
    def tick(self):
        if dist((self.x, self.y), locale) <= int(self.size) and self.fuse == 1:
            Helth[0] -= 3
            self.fuse = 0
            pygame.display.set_caption("temp")
        pygame.draw.circle(screen, (255, 210, 180), (int(self.x), int(self.y)), math.ceil(self.size))
        if self.age in (8, 14, 19, 23) or self.age >= 25:
            self.size -= .5
        self.age += 1
        if self.age >= 47:
            return True
        else:
            return False
        
    def expire(self):
        return True

motion = [wraith(0, -1)]

bulletinboard.append(rocket((176, 112), 270))

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
                motion.append(wraith(jump(locale, pygame.mouse.get_pos()), shrek))
            launch = 1
        else:
            launch = 0
            
            
    screen.fill((0, 0, 0))
            
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
                
    doom = []
    if len(bulletinboard) >= 1:
        for i in range(len(bulletinboard)):
            if bulletinboard[i].tick():
                doom.append(i+1)
        while len(doom) >= 1:
            for i in range(len(doom)):
                doom[i] -= 1
            bulletinboard[doom[0]].expire()
            bulletinboard.pop(doom[0])
            doom.pop(0)
            
    if locale[1] < 485:
        autumn += 1
        locale[1] += autumn
    if locale[1] >= 485:
        autumn = 0
        if locale[1] > autumn:
            locale[1] = 485
    
    clock.tick(20)
    pygame.draw.circle(screen, (200, 200, 200), (int(locale[0]), int(locale[1])), 7)
    pygame.draw.circle(screen, (255, 255, 255), (int(locale[0]), int(locale[1])), 1)
    pygame.display.update()