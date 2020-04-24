import pygame, random, sys, math
from random import randint
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((710, 710))

locale = [255, 255]
bulletinboard = []
clock = pygame.time.Clock()
launch = 0
shrek = 0
autumn = 0
Helth = [15, 25]
spawner = 0
swarm = 1

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
    return(((pointA[0]-pointB[0])**2+(pointA[1]-pointB[1])**2)**(0.5))

def finale(swarm):
    if swarm <= 4:
        print(". Try again- I know you can do better than that!")
    elif swarm <= 9:
        print(". At least it's something.")
    elif swarm <= 15:
        print(". Not bad, not bad at all.")
    elif swarm <= 25:
        print(", that's actually quite good!")
    elif swarm <= 35:
        print("- I'm impressed!")
    else:
        print(", were you cheating? If not, you've earned my respect. Congratulations!")
    sys.exit()


class wraith:
    def __init__(self, direction, lastwraith):
        if lastwraith == -1:
            self.direction = -1
            self.power = 1.6
        else:
            self.direction = direction
            self.power = math.log(lastwraith, 1.7)+11.48
            
    def tick(self, locale):
        temp = locale
        if not self.direction == -1:
            temp[0] += self.power*math.cos(self.direction*math.pi/180*-1)
            temp[1] += self.power*math.sin(self.direction*math.pi/180*-1)
            self.power -= .35
        return temp
        
    def tale(self):
        return self.power
    
class rocket:
    def __init__(self, coordinates, initial):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.age = 0
        self.dir = initial
        self.flash = False
        
    def tick(self):
        if dist(locale, (self.x, self.y)) <= 12:
            self.flash = True
            return True
        iddir = jump((self.x, self.y), locale)
        tempdir = self.dir - 180
        tempbool = False
        if tempdir < 0:
            tempdir += 360
            tempbool = True
        if tempbool:
            if iddir < self.dir or iddir > tempdir:
                self.dir -= 3
            elif not self.dir == iddir:
                self.dir += 3
        else:
            if iddir > self.dir or iddir < tempdir:
                self.dir += 3
            elif not self.dir == iddir:
                self.dir -= 3
        if self.dir >= 360:
            self.dir -= 360
        if self.dir < 0:
            self.dir += 360
        pygame.draw.circle(screen, (255, 205, 210), (int(self.x), int(self.y)), 2)
        self.x += math.cos(self.dir*math.pi/180)*4
        self.y -= math.sin(self.dir*math.pi/180)*4
        pygame.draw.circle(screen, (255,225,230), (int(self.x), int(self.y)), 2)
        self.x += math.cos(self.dir*math.pi/180)*4
        self.y -= math.sin(self.dir*math.pi/180)*4
        pygame.draw.circle(screen, (255, 235, 240), (int(self.x), int(self.y)), 3)
        self.age += 1
        if self.age >= 160 or dist(locale, (self.x, self.y)) <= 12:
            return True
        else:
            return False
        
    def expire(self):
        if dist(locale, (self.x, self.y)) <= 16 or self.flash:
            Helth[0] -= 3
            if Helth[0] == 0 and Helth[1] >= 6 or Helth[0] < 0:
                print("You were blown up by a rocket, but it took " + str(swarm) + " warriors to do it", end = "")
                finale(swarm)
            bulletinboard.append(blast((self.x, self.y), 0))
        else:
            bulletinboard.append(blast((self.x, self.y), 0))
        return True
    
class blast:
    def __init__(self, site, fuse):
        self.x = site[0]
        self.y = site[1]
        self.fuse = fuse
        self.size = 16
        self.age = 0
        
    def tick(self):
        if dist((self.x, self.y), locale) <= int(self.size) and self.fuse == 1:
            Helth[0] -= 3
            if Helth[0] == 0 and Helth[1] >= 6 or Helth[0] < 0:
                print("You were blown up by a rocket, but it took " + str(swarm) + " warriors to do it", end = "")
                finale(swarm)
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
    
    
class heavy:
    def __init__(self):
        self.y = 674
        if randint(0, 1) == 1:
            self.x = -11-4*swarm
            self.speed = 8
        else:
            self.x = 721+4*swarm
            self.speed = -8
        self.frame = 0
        self.clock = 1
        
    def tick(self):
        self.clock += 1
        if self.clock >= 18:
            self.frame += 1
            self.clock = 0
            if self.frame > 5:
                self.frame = 0
                self.x += self.speed
                if self.x >= 486:
                    self.speed = -8
                elif self.x <= 24:
                    self.speed = 8
                bulletinboard.append(rocket((self.x, 485), 90))
                
        if self.frame == 0:
            pygame.draw.rect(screen, (110, 110, 145), (self.x, self.y, 4, 11))
            pygame.draw.rect(screen, (110, 110, 145), (self.x+2*self.speed, self.y, 4, 11))
            pygame.draw.rect(screen, (110, 110, 145), (self.x-self.speed, self.y, 4, 11))
        elif self.frame == 1:
            pygame.draw.rect(screen, (110, 110, 145), (self.x+2*self.speed, self.y, 4, 11))
            pygame.draw.rect(screen, (110, 110, 145), (self.x-self.speed, self.y, 4, 11))
            pygame.draw.rect(screen, (110, 110, 145), (self.x, self.y-7, 4, 11))
        elif self.frame == 2:
            pygame.draw.rect(screen, (110, 110, 145), (self.x+2*self.speed, self.y, 4, 11))
            pygame.draw.rect(screen, (110, 110, 145), (self.x-self.speed, self.y, 4, 11))
            pygame.draw.rect(screen, (110, 110, 145), (self.x+self.speed, self.y, 4, 11))
        elif self.frame == 3:
            pygame.draw.rect(screen, (110, 110, 145), (self.x+2*self.speed, self.y-8, 4, 11))
            pygame.draw.rect(screen, (110, 110, 145), (self.x-self.speed, self.y-8, 4, 11))
            pygame.draw.rect(screen, (110, 110, 145), (self.x+self.speed, self.y, 4, 11))
        elif self.frame >= 4:
            pygame.draw.rect(screen, (110, 110, 145), (self.x+3*self.speed, self.y, 4, 11))
            pygame.draw.rect(screen, (110, 110, 145), (self.x, self.y, 4, 11))
            pygame.draw.rect(screen, (110, 110, 145), (self.x+self.speed, self.y, 4, 11))
            if self.frame == 5:
                pygame.draw.polygon(screen, (110, 110, 145), ((self.x+self.speed+5, self.y), (self.x+self.speed-3, self.y), (self.x+self.speed+2, self.y+6)))
                
        return False
            

motion = [wraith(0, -1)]

bulletinboard.append(heavy())

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
            
    Helth[1] -= 1
    if Helth[1] <= 0:
        Helth[1] = 25
        if Helth[0] < 20:
            Helth[0] += 1
        
    spawner += 1
    if spawner >= 243+2*swarm:
        spawner = 0
        swarm += 1
        bulletinboard.append(heavy())
    pygame.display.set_caption(str(swarm)+"    "+str(Helth[0]))
        
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
            
    if locale[1] < 685:
        autumn += .5
        locale[1] += autumn
    if locale[1] >= 685:
        autumn = 0
        locale[1] = 685
    if locale[0] <= 25:
        locale[0] = 25
    elif locale[0] >= 685:
        locale[0] = 685
        
    
    clock.tick(35)
    pygame.draw.circle(screen, (200, 200, 200), (int(locale[0]), int(locale[1])), 7)
    pygame.draw.circle(screen, (255, 255, 255), (int(locale[0]), int(locale[1])), 1)
    pygame.display.update()