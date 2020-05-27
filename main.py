import pygame, random, sys, math
from random import randint
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((710, 710))
#initializes the screen and imports files
locale = [355, 355]
#spawns the player in the center of the screen
bulletinboard = []
#all the enemies and bullets
clock = pygame.time.Clock()
#initializes the clock so that frames aren't all triggering as fast as the computer can handle
launch = 0
#makes a launch variable which is later used for not making holding the mouse button down count as a bunch of jumps
shrek = 0
#makes a variable to keep track of the *most powerful* jump still affecting the player 
autumn = 0
#keeps track of how fast the player is *fall*ing
Helth = [15, 25]
#your health, and then the countdown until you heal (max HP 20)
spawner = 0
#timer until another enemy spawns
swarm = 2
#initializes variables and stuff
balance = ((1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1), (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2), (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2), (1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3), (1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3), (1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4), (2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5))


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
#finds the direction from point A to point B so I can do stuff with sin and cos later in homing missiles and such

def dist(pointA, pointB):
    return(((pointA[0]-pointB[0])**2+(pointA[1]-pointB[1])**2)**(0.5))
#pythagorean theorem function

def finale(swarm):
    if swarm <= 5:
        print(". I didn't even know it was possible to die that quickly.")
    elif swarm <= 7:
        print(". Try again- I know you can do better than that!")
    elif swarm <= 11:
        print(". At least it's something.")
    elif swarm <= 17:
        print(". Not bad, not bad at all.")
    elif swarm <= 25:
        print("; that's actually quite good!")
    elif swarm <= 45:
        print("- I'm impressed!")
    elif swarm <= 75:
        print(", were you cheating? If not, you've definitely earned my respect. Congratulations!")
    else:
        print(". Okay, with a score this high, you were definitely cheating.")
    sys.exit()
#gives you a reference point for your score and ends the game

def invade(score):
    decider = randint(0, 14)
    dudes = []
    if score <= 5:
        tier = 0
    elif score <= 7:
        tier = 1
    elif score <= 11:
        tier = 2
    elif score <= 17:
        tier = 3
    elif score <= 25:
        tier = 4
    elif score <= 45:
        tier = 5
    elif score <= 75:
        tier = 6
    if score <= 75:
        for i in range(balance[tier][decider]):
            dudes.append(randint(1, 2))
    else:
        for i in range(randint(3, int(score/12))):
            dudes.append(randint(1, 2))
    return (dudes)
        

            
#applies force to your character when you jump over a period of time so you don't just teleport
class wraith():
    def __init__(self, direction, lastwraith):
        if lastwraith == -1:
            self.direction = -1
            self.power = 1.6
            #puts in a wraith to the list that does absolutely nothing but stops the game from crashing when you iterate over the list when you try to iterate over the list
        else:
            self.direction = direction
            self.power = math.log(lastwraith, 1.7)+16.48-.25*Helth[0]
            #makes succesive jumps scale up in power and be more powerful at low health to build suspense by keeping you as close to 0 at all times
            
    def tick(self, locale):
        temp = locale
        if not self.direction == -1:
            temp[0] += self.power*math.cos(self.direction*math.pi/180*-1)
            temp[1] += self.power*math.sin(self.direction*math.pi/180*-1)
            self.power -= 0.35
            #actually moves you
        return temp
        #updates the player's location
        
    def tale(self):
        return self.power
    #returns how much the jump is moving you so the jump can make later jumps stronger and so jumps that are no longer doing anything can be cleared out
    

class ouch():
    def __init__(self, color):
        self.timer = randint(20, 30)
        self.self = [locale[0], locale[1]]
        self.autumn = 1
        self.jdire = randint(0, 360)*math.pi/180
        self.power = randint(7, 9)
        self.color = color
        self.color = color
        
    def tick(self):
        pygame.draw.circle(screen, self.color, (int(self.self[0]), int(self.self[1])), 2)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.self[0]), int(self.self[1])), 1)
        self.timer -= 1
        if self.timer <= 0:
            return True
        self.autumn += 0.5
        self.self[1] += self.autumn
        self.self[1] -= math.sin(self.jdire)*self.power
        self.self[0] += math.cos(self.jdire)*self.power
        
    def expire(self):
        return True
    
    
class rocket():
    def __init__(self, coordinates, initial):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.dir = initial
        #starts up the rocket where it should be
        self.age = 0
        #makes a timer so the rocket explodes eventually even if it hasn't hit you so every rocket isn't automatic damage
        self.flash = False
        
    def tick(self):
        if dist(locale, (self.x, self.y)) <= 12:
            #checks to see if you're next to the missile before moving in case you moved towards it last frame and it's about to move away from you
            self.flash = True
            #remembers that it hit you so that you can't escape the blast between the explosion and when the explosion will .tick()
            return True
            #blows up
        iddir = jump((self.x, self.y), locale)
        tempdir = self.dir - 180
        #cuts a circle into two halves, with one of the divisions pointing towards the player and the other pointing away. If the rocket is pointing towards one of them it will need to turn clockwise and if it is pointing towards the other one it will need to turn counterclockwise.
        tempbool = False
        if tempdir < 0:
            tempdir += 360
            tempbool = True
            #loops the other division of the circle around if it would be a negative value; tempbool remembers if this triggered or if it didn't need to trigger
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
        #checks to see which half-circle the rocket is pointing towards and then turns the rocket correspondingly
        if self.dir >= 360:
            self.dir -= 360
        if self.dir < 0:
            self.dir += 360
            #loops the direction so it can't try to move 361 or -1 degrees (which would still work for the actual motion, but would break the homing program and get it stuck soinning in circles)
        pygame.draw.circle(screen, (255, 205, 210), (int(self.x), int(self.y)), 2)
        self.x += math.cos(self.dir*math.pi/180)*4
        self.y -= math.sin(self.dir*math.pi/180)*4
        pygame.draw.circle(screen, (255,225,230), (int(self.x), int(self.y)), 2)
        self.x += math.cos(self.dir*math.pi/180)*4
        self.y -= math.sin(self.dir*math.pi/180)*4
        pygame.draw.circle(screen, (255, 235, 240), (int(self.x), int(self.y)), 3)
        #moves the rocket, in multiple steps to leave behind a neat-looking trail
        self.age += 1
        #increments the timer
        if self.age >= 160 or dist(locale, (self.x, self.y)) <= 12:
            if dist(locale, (self.x, self.y)) <= 12:
                self.flash = True
                #automatically hits you if it hit you so you can't escape
            return True
        #calls .expire to explode if it has already timed out or is next to the player
        else:
            return False
        #doesn't call .expire and doesn't explode
        
    def expire(self):
        if dist(locale, (self.x, self.y)) <= 12 or self.flash:
            #instantly deals damage to the player if necessary
            Helth[0] -= 3
            for i in range(randint(6, 12)):
                bulletinboard.append(ouch((255, 210, 180)))
            if Helth[0] == 0 and Helth[1] >= 6 or Helth[0] < 0:
                print("You were blown up by a rocket, but it took " + str(swarm) + " enemies to do it", end = "")
                finale(swarm)
                #deals damage
            bulletinboard.append(blast((self.x, self.y), 0))
            #create lingering explosion bracket that does nothing
        else:
            bulletinboard.append(blast((self.x, self.y), 0))
            #create lingering explosion bracket that can still hit you
        return True
    
class blast():
    def __init__(self, site, fuse):
        self.x = site[0]
        self.y = site[1]
        #puts the explosion where the missile was
        self.fuse = fuse
        #prevents the explosion from hitting you every frame and basicallyinstakilling you, also disables the explosion if the rocket already hit you
        self.size = 14
        #sets the starting size of the explosion so it can shrink over time (at a slightly higher radius than the missile will detect you at so you can feel cool by barely dodging missiles)
        self.age = 0
        #makes the explosion fade out
        
    def tick(self):
        if dist((self.x, self.y), locale) <= int(self.size) and self.fuse == 1:
            Helth[0] -= 3
            #hurts you
            for i in range(randint(6, 12)):
                bulletinboard.append(ouch((255, 210, 180)))
            #makes sparks appear
            if Helth[0] == 0 and Helth[1] >= 6 or Helth[0] < 0:
                print("You were blown up by a rocket, but it took " + str(swarm) + " enemies to do it", end = "")
                finale(swarm)
                #kills you (spares you if you're right about to gain a HP that would put you above 0 so you can have more near-death encounters)
            self.fuse = 0
            #defuses itself so it can't hit you multiple times
        pygame.draw.circle(screen, (255, 210, 180), (int(self.x), int(self.y)), math.ceil(self.size))
        #shows where the explosion is so the player doesn't get hit and killed by it without knowing what's happening (also makes the explosion up to half a pixel larger than the hitbox so the player can "miraculously" dodge a hit)
        if self.age in (8, 14, 19, 24):
            self.size -= 1
        #makes the shrinking of the explosion accelerate over time
        elif self.age >= 26:
            self.size -= 0.5
            #shrinks the explosion rapidly after the previous lines of code resolved and the explosion is shrinking at full speed
        self.age += 1
        #increases age so the acceleration works
        if self.size < 1:
            return True
        #erases explosion
        else:
            return False
        #doesn't erase explosion
        
    def expire(self):
        return True
    #does nothing, but self.expire() will get called before it is erased so a placeholder is necessary
    
    
class heavy():
    def __init__(self):
        self.y = 674
        if randint(0, 1) == 1:
            self.x = -1*randint(11+4*swarm, 21+5*swarm)
            self.speed = randint(7, 12)
            #either spawns a tank offscreen left...
        else:
            self.x = randint(721+4*swarm, 731+5*swarm)
            self.speed = -1*randint(7, 12)
            #or offscreen right (moving inwards at a slightly randomized speed, spawning farther from the screen's edge depending on number of already existing tanks to reduce overlap)
        self.frame = 0
        self.clock = 0
        #starts a timer
        self.step = 0
        
    def tick(self):
        self.clock += 1
        if self.clock >= 11:
            self.frame += 1
            self.clock = 0
            #switches to the next frame of the moving animation every 10 ticks
            if self.frame > 5 or self.frame == 4 and self.step == 1:
                self.frame = 0
                self.x += self.speed
                #loops around the animation
                if self.x >= 686 and self.speed >= 0:
                    self.speed *= -1
                elif self.x <= 24 and self.speed<=0:
                    self.speed *= -1
                #makes the tanks bounce off the edges so they don't walk offscreen
                if self.step == 0:
                    self.step = 1
                    bulletinboard.append(rocket((self.x, 674), 90))
                else:
                    self.step = 0
                #launches a missile on the end of the second step or toggles the step
                
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
            #draws the tank in a different position depending on the current frame of the moving animation
                
        return False
        #makes the tank not explode
        
        
class limiter():
    def __init__(self):
        self.x = randint(205, 505)
        self.y = randint(205, 505)
        #initializes force field at a random point
        self.power = randint(35, 65)
        #sets a randomized delay before forcefield activates
        self.frame = 5
        self.deel = 0
        
    def arrive(self):
        if self.frame == 0:
            pygame.draw.line(screen, (255, 255, 255), (self.x, self.y+self.power), (self.x, self.y+220), 8)
            pygame.draw.line(screen, (255, 255, 255), (self.x+self.power, self.y), (self.x+220, self.y), 8)
            pygame.draw.line(screen, (255, 255, 255), (self.x, self.y-self.power), (self.x, self.y-220), 8)
            pygame.draw.line(screen, (255, 255, 255), (self.x-self.power, self.y), (self.x-220, self.y), 8)
            #draws lines approaching power core
            self.power -= 7
            #makes lines get closer
        elif self.frame == 1:
            pygame.draw.line(screen, (255, 255, 255), (self.x, self.y+self.power), (self.x, self.y), 8)
            pygame.draw.line(screen, (255, 255, 255), (self.x+self.power, self.y), (self.x, self.y), 8)
            pygame.draw.line(screen, (255, 255, 255), (self.x, self.y-self.power), (self.x, self.y), 8)
            pygame.draw.line(screen, (255, 255, 255), (self.x-self.power, self.y), (self.x, self.y), 8)
            #draws lines being absorbed by power core
            self.power -= 7
            #makes lines get absorbed by core
        
    def tick(self):
        if self.frame == 0 or self.frame == 1:
            self.arrive()
            #calls above function and draws lines
            if self.power <= 0:
                self.frame += 1
                if self.frame == 1:
                    self.power = 220
                if self.frame == 2:
                    self.power = 0
                #proceeds to next steps of animation
        elif self.frame == 2:
            self.power += 7
            if self.power < 220:
                pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.power, 2)
                #draws powering up circle
            else:
                self.power = 105
                pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), 220, 2)
                self.frame += 1
                #draws circle at max power during final frame before next step of animation
        elif self.frame == 3:
            pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), 220, 4)
            #draws the new boundaries of the play field
            self.power -= 1
            if self.power <= 0:
                self.frame += 1
                self.power = 220
            #makes the core run out of power after a time
        elif self.frame == 4:
            pygame.draw.circle(screen, (225, 225, 225), (self.x, self.y), self.power, 2)
            self.power -= 11
            #draws the collapsing forcefield
            if self.power <= 1:
                self.power = randint(0, 15)
                self.frame += 1
                #ends the animation and sets the delay before the limiter reactivates
        else:
            self.power += 1
            #slowly reharges the limiter
            if self.power >= 175-5*swarm:
                self.frame = 0
                self.power = 220
                #resets the limiter
                self.x = randint(205, 505)
                self.y = randint(205, 505)
                #randomizes the limiter's position
                
        if self.frame == 2 or self.frame == 3:
            pygame.draw.rect(screen, (255, 255, 255), (self.x-7, self.y-7, 14, 14))
            pygame.draw.rect(screen, (255, 255, 255), (self.x-10, self.y-5, 20, 10))
            pygame.draw.rect(screen, (255, 255, 255), (self.x-5, self.y-10, 10, 20))
            #draws the power core
        if self.frame == 3:
            temp = dist((self.x, self.y), locale)
            if temp > 227:
                if self.deel >= 1:
                    self.deel -= 1
                    #decreases the clock until the limiter can deal damage again
                temp = 220/temp
                temper = (int(self.x+temp*(locale[0]-self.x)), int(self.y+temp*(locale[1]-self.y)))
                #finds the point on the circle's edge closest to the player
                pygame.draw.line(screen, (255, 255, 255), (self.x, self.y), trueloc, 3)
                pygame.draw.line(screen, (255, 220, 220), temper, trueloc, 3)
                pygame.draw.line(screen, (255, 65, 65), temper, trueloc, 1)
                #lasers that point
                if self.deel == 0:
                    self.deel = 10
                #limits the limiter's DPS to 2.5
                    Helth[0] -= 1
                    for i in range(randint(1, 2)):
                        bulletinboard.append(ouch((255, 220, 220)))
                    for i in range(randint(1, 2)):
                        bulletinboard.append(ouch((255, 65, 65)))
                    if Helth[0] == 0 and Helth[1] >= 6 or Helth[0] < 0:
                        print("You strayed out of bounds and were killed by a laser, but first avoided " + str(swarm) + " enemies' bullets", end = "")
                        finale(swarm)
                        #finally actually deals damage
            else:
                pygame.draw.line(screen, (255, 255, 255), (self.x, self.y), trueloc, 2)
                #draws a non-ouchy line to the player
                self.deel = 5
                #gives the player some leniency if they are only outside the circle for 1/7 of a second
        return False
        #makes the limiter not blow up immediately
        

class jumper():
    def __init__(self):
        #spawns the turret in upper-Earth's atmosphere falling down
        self.x = randint(80, 630)
        self.y = -15
        self.dire = 0
        if self.x <= 355:
            self.jdire = randint(180, 225)
        else:
            self.jdire = randint(315, 360)
        self.fall = 2
        self.power = randint(8, 12)
        self.vat = 0
        #offset's the turret's aim so the turrets don't all aim at roughly the same pixel
        if randint (0, 5) <= 1:
            self.offset = randint(-40, 40)
        else:
            self.offset = 0
        
    def cross(self):
        #figures out which side of the laser the character is on so it will know when the character crosses the beam (same method as rockets)
        temp = jump((self.x, self.y), locale)
        temper = self.dire*180/math.pi
        tempest = temper-180
        if tempest < 0:
            tempest += 360
            tempbool = True
        else:
            tempbool = False
        if tempbool:
            if temp <= tempest and temp >= temper:
                return "L"
            else:
                return "R"
        else:
            if temp >= tempest and temp <= temper:
                return "R"
            else:
                return "L"
        
    def tick(self):
        #makes self.vat increase so the turret will transfer between animations when on the ground
        if self.y == 660:
            self.vat += 1
        #makes the animation reset after laser-firing and jumps the turret
        if self.vat >= 125:
            self.vat = 0
            self.power = randint(12, 16)
            #chooses a direction to jump in, towards the middle if it's around the edges of the screen or randomly otherwise
            if self.x >= 600:
                self.jdire = randint(235, 270)*math.pi/180
            elif self.x <= 150:
                self.jdire = randint(270, 305)*math.pi/180
            else:
                self.jdire = randint(235, 305)*math.pi/180
        self.power -= 0.35
        #handles jumping
        if self.power < 0:
            self.power = 0
        self.x += math.cos(self.jdire)*self.power
        self.y += math.sin(self.jdire)*self.power
        self.fall += 0.5
        self.y += self.fall
        if self.y > 660:
            self.y = 660
            self.fall = 0
        #draws the turret's legs
        pygame.draw.line(screen, (255, 210, 210), (int(self.x), int(self.y)), (int(self.x)+12, int(self.y)+12), 5)
        pygame.draw.line(screen, (255, 210, 210), (int(self.x), int(self.y)), (int(self.x)-12, int(self.y)+12), 5)
        #draws the turret's arms and laser
        if self.vat <= 45:
            self.dire = (jump((self.x, self.y), locale)+self.offset)*math.pi/180
            pygame.draw.line(screen, (255, 210, 210), (int(self.x), int(self.y)), (int(self.x+math.cos(self.dire)*17), int(self.y-math.sin(self.dire)*17)), 5)
        elif self.vat <= 100:
            pygame.draw.line(screen, (255, 210, 210), (int(self.x), int(self.y)), (int(self.x+math.cos(self.dire)*17), int(self.y-math.sin(self.dire)*17)), 5)
            pygame.draw.line(screen, (140, 140, 140), (int(self.x+math.cos(self.dire)*17), int(self.y-math.sin(self.dire)*17)), (int(self.x+math.cos(self.dire)*1005), int(self.y-math.sin(self.dire)*1005)), 5)
            self.comp = self.cross()
        else:
            pygame.draw.line(screen, (255, 210, 210), (int(self.x), int(self.y)), (int(self.x+math.cos(self.dire)*17), int(self.y-math.sin(self.dire)*17)), 5)
            pygame.draw.line(screen, (210, 120, 160), (int(self.x+math.cos(self.dire)*17), int(self.y-math.sin(self.dire)*17)), (int(self.x+math.cos(self.dire)*1005), int(self.y-math.sin(self.dire)*1005)), 5)  
            #checks to see if the laser has been crossed
            new = self.cross()
            if not self.comp == new:
                self.comp = new
                #finally actually deals damage
                Helth[0] -= 4
                for i in range(randint(8, 16)):
                    bulletinboard.append(ouch((210, 120, 160)))
                if Helth[0] == 0 and Helth[1] >= 6 or Helth[0] < 0:
                    print("You were sliced up by a laser, but survived an onslaught of " + str(swarm) + " enemies first", end = "")
                    finale(swarm)
        #draws turret body
        pygame.draw.circle(screen, (255, 190, 190), (int(self.x), int(self.y)), 9)
        pygame.draw.polygon(screen, (255, 145, 145), ((int(self.x), int(self.y)-6), (int(self.x-4.24), int(self.y+4.24)), (int(self.x+4.24), int(self.y+4.24))))

        
motion = [wraith(0, -1)]
#starts the list of jumps off with a nonexistent jump so the list can be iterated over

bulletinboard.append(heavy())
#starts the game off with one enemy...

bulletinboard.append(limiter())
#and the limiter.





















while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            #closes the window when the X is pressed
        if event.type == pygame.MOUSEBUTTONUP:
            if not launch:
                autumn = 0
                shrek = 0
                #before jumping, resets shrek to gain new value and stops the player falling
                for i in motion:
                    temp = i.tale()
                    if temp > shrek:
                        shrek = temp
                        #updates shrek to truly be the most powerful jump
                motion.append(wraith(jump(locale, pygame.mouse.get_pos()), shrek))
                #actually jumps
            launch = 1
        else:
            launch = 0
            #prevents holding the mouse down from being a jump every frame
                        
    screen.fill((0, 0, 0))
    #makes a black background
    Helth[1] -= 1
    if Helth[1] <= 0:
        Helth[1] = 25
        if Helth[0] < 16+2*swarm:
            Helth[0] += 1
    #autoheals you by 1 HP every 25 frames to an always-increasing max HP
        
    spawner += 1
    if spawner >= 253-8*swarm:
        spawner = 0
        temp = invade(swarm)
        for i in temp:
            swarm += 1
            if i == 1:
                bulletinboard.append(heavy())
            else:
                bulletinboard.append(jumper())
        #spawns enemies preiodically, accelerating at a set rate
    pygame.display.set_caption(str(swarm))
    
    
    #tells the player the current score and health
    doom = []
    #empties the list of jumps that will be erased
    for i in range(len(motion)):
        locale = motion[i].tick(locale)
        #moves you according to what jumps are currently affecting you
        if motion[i].tale() <= 0:
            doom.append(i)
            #adds a jump that isn't affecting you anymore to the list of jumps that will be erased (if it was erased right here than the iterator will be offset, skipping the next jump and crashing the game when it gets to what would be the last jump)
    for i in doom:
        motion.pop(i)
        #now removes the useless jumps
        if len(doom) >= 1:
            for i in doom:
                i -= 1
                #decreases the number of each other jump that will be deleted now that there is one less item in the list
    
    if locale[1] < 685:
        autumn += 0.5
        locale[1] += autumn
    #makes gravity get you down (unlike an elevator- or *are* we gonna let the elevator bring us down? Who knows?)
    if locale[1] >= 685:
        autumn = 0
        locale[1] = 685
    if locale[0] <= -50:
        locale[0] = -50
    elif locale[0] >= 760:
        locale[0] = 760
    #stops the player from moving outside the boundaries of the box
        
    trueloc = [int(locale[0]), int(locale[1])]
    #creates a rounded location for the player because some of the drawing functions will soon be unable to operate with float parameters

    doom = []
    #empties doom
    if len(bulletinboard) >= 1:
        for i in range(len(bulletinboard)):
            if bulletinboard[i].tick():
                doom.append(i+1)
                #does the same thing as happened before but now with bullets and enemies instead of jumps
        while len(doom) >= 1:
            for i in range(len(doom)):
                doom[i] -= 1
                #more of the same
            bulletinboard[doom[0]].expire()
            #something different! Triggers any on-death effects like a missile exploding from enemies and bullets
            bulletinboard.pop(doom[0])
            doom.pop(0)
            #and back to more of the same. Deletes the bullets and enemies that need to be deleted.
            
    clock.tick(35)
    #makes the game wait 1/35 of a second between frames so you can actually see what's going on, assuming you're actually able to see the player and you aren't offscreen
    if locale[0] >= -5 and locale[0] <= 715:
        pygame.draw.circle(screen, (200, 200, 200), (trueloc[0], trueloc[1]), 7)
        #draws the player (much larger than the actual hitbox so you can just narrowly dodge a bullet or missile and feel good about yourself when in fact you weren't even close to getting hit)
        pygame.draw.circle(screen, (255, 255, 255), (trueloc[0], trueloc[1]), 1)
    #draws the player's actual hitbox
    else:
        if locale[0] < 0:
            pygame.draw.polygon(screen, (200, 200, 200), ((5, trueloc[1]), (13, trueloc[1]+5), (13, trueloc[1]-5)))
            #draws a triangle pointing to the player if offscreen left
        else:
            pygame.draw.polygon(screen, (200, 200, 200), ((705, trueloc[1]), (697, trueloc[1]+5), (697, trueloc[1]-5)))
            #draws a triangle pointing to the player if offscreen right
			
    criticality = Helth[0]/(16+2*swarm)
    if criticality <= 0.1:
        criticality = (254, 0, 0)
    elif criticality <= 0.3:
        criticality = (252, 100, 0)
    elif criticality <= 0.5:
        criticality = (250, 200, 0)
    elif criticality <= 0.99:
        criticality = (200, 250, 0)
    else:
        criticality = (100, 255, 0)
    #figures out how close you are to death so the healthbar will be colored corectly
    pygame.draw.line(screen, criticality, (12, 12), (12+6*Helth[0], 12), 6)
    #draws the healthbar
	
    pygame.display.update()
    #and finally makes everything that's happened so far visible.
    