import pygame
from pygame.locals import *
import random
import math
import sys

#Defines
XHOLES = 5
YHOLES = 5
XSPACING = 20
YSPACING = 20
TOPBAR = 100
TARGETRATE = 5
MAXTARGETS = 5
TARGETCHANCE = 5
TARGETTIME = 60
NOSETHRESHOLD = 10  #The number of frames where just the nose will show at the start and end
TIMELIMIT = 100
MISSPENALTY = 5

#Colour definitions for the target
BULLSEYE = (0, 0, 0, 255)
BULLSEYEPOINTS = 20
INNERRING = (136, 0, 27, 255)
INNERRINGPOINTS = 10
INNERMIDDLE = (236, 28, 36, 255)
INNERMIDDLEPOINTS = 5
OUTERMIDDLE = (255, 127, 39, 255)
OUTERMIDDLEPOINTS = 3
INNEREDGE = (255, 242, 0, 255)
INNEREDGEPOINTS = 2
OUTEREDGE = (255, 255, 255, 255)
OUTEREDGEPOINTS = 1
SCORING = (BULLSEYE, BULLSEYEPOINTS), (INNERRING, INNERRINGPOINTS), (INNERMIDDLE, INNERMIDDLEPOINTS), (OUTERMIDDLE, OUTERMIDDLEPOINTS), (INNEREDGE, INNEREDGEPOINTS), (OUTEREDGE, OUTEREDGEPOINTS)

#Helper functions
def CheckTounching(pos1, pos2, size):
    if ((pos1[0] >= pos2[0] and pos1[0] <= pos2[0] + size[0]) and (pos1[1] >= pos2[1] and pos1[1] <= pos2[1] + size[1])):
        return True
    else:
        return False

class Target:
    def __init__(self, xpos, ypos):
        self.pos = (xpos, ypos)
        self.timeToLive = TARGETTIME
        self.adjustedPos = (xpos + XSPACING, ypos + YSPACING + TOPBAR)

    def Tick(self):
        self.timeToLive -= 1

class AimOfTheGame:
    def __init__(self, setUp):
        self.xSize = setUp[0]
        self.ySize = setUp[1]
        global TARGETTIME
        TARGETTIME = setUp[2] * 60
        self.time = setUp[3]
        pygame.init()
        pygame.display.set_caption("Aim Of The Game")

        self.clock = pygame.time.Clock()

        #Load assets.
        self.retry = pygame.image.load('Assets/retry.png')
        self.target = pygame.image.load('Assets/target.png')

        self.screen = pygame.display.set_mode((self.xSize + 2 * XSPACING, self.ySize + 2 * YSPACING + TOPBAR))

        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((200,200,200))

        if pygame.font:
            self.font = pygame.font.Font(None, 40)

        self.score = 0
        self.spawnTick = 0
        self.timeOver = False

        self.targets = []

        #Start the main gameplay loop
        #self.Run()

    def Run(self):
        self.finished = False

        while not self.finished:
            #Handle input
            self.HandleInput()

            #Tick moles, and remove any that have expired
            for t in self.targets:
                t.Tick()
                if t.timeToLive <= 0:
                    self.targets.remove(t)

            if not self.timeOver:
                self.SpawnTargets()

            #Draw screen
            self.Draw()

            self.clock.tick(60)
        
        pygame.quit()
        return True

    def HandleInput(self):
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                self.CheckHit(pos)
                if self.timeOver == True:
                    if CheckTounching(pos, (self.screen.get_size()[0] - self.retry.get_size()[0] - XSPACING, 3 * YSPACING), self.retry.get_size()):
                        self.finished = True
    
    def Draw(self):
        #clear screen
        self.screen.blit(self.background, (0,0))

        #Draw moles
        for t in self.targets:
            img = self.target
            self.screen.blit(img, (t.pos[0] + XSPACING, t.pos[1] + YSPACING + TOPBAR))

        #Draw score
        scoreStr = "Score: " + str(self.score)
        scoreTxt = self.font.render(scoreStr, True, (10,10,10))
        self.screen.blit(scoreTxt, (XSPACING,YSPACING))

        #Draw timer
        timeElapsed = pygame.time.get_ticks()/1000
        timeRemaining = math.floor(self.time - timeElapsed)
        if timeRemaining <= 0:
            self.timeOver = True
            timeRemaining = 0
        timeStr = "Time remaining: " + str(timeRemaining)
        timeTxt = self.font.render(timeStr, True, (10,10,10))
        self.screen.blit(timeTxt, (XSPACING, 3 * YSPACING))

        if self.timeOver == True:
            endStr = "Time over!"
            endText = self.font.render(endStr, True, (10,10,10))
            self.screen.blit(endText, (self.screen.get_size()[0] - endText.get_size()[0] - XSPACING, YSPACING))
            #Draw restart icon
            self.screen.blit(self.retry, (self.screen.get_size()[0] - self.retry.get_size()[0] - XSPACING, 3 * YSPACING))

        #Refresh the screen
        pygame.display.flip()

    def SpawnTargets(self):
        #Wait until the spawn rate
        self.spawnTick += 1
        if self.spawnTick < TARGETRATE:
            return
        else:
            self.spawnTick = 0
        
        #If we've already got all our targets, don't spawn any more
        if len(self.targets) >= MAXTARGETS:
            return

        #Only spawn a target if we hit the chance
        if random.randint(0, TARGETCHANCE) != 0:
            return
        
        #We're good to spawn a mole, find a new spot
        valid = False
        x = 0
        y = 0
        while (valid == False):
            valid = True
            x = (random.random() * (self.xSize - 2 * XSPACING)) + XSPACING
            y = (random.random() * (self.ySize - 2 * YSPACING)) + YSPACING
        
        #We've found our spot, spawn the mole
        self.targets.append(Target(x,y))

    def CheckHit(self, pos):
        if (pos[0] < XSPACING or pos[0] > XSPACING + self.xSize or pos[1] < YSPACING + TOPBAR or pos[1] > YSPACING + TOPBAR + self.ySize):
            #The click was out of the play area
            return
        colour = self.screen.get_at(pos)
        hit = False
        for zone in SCORING:
            if zone[0] == colour:
                self.score += zone[1]
                hit = True
        if hit == False:
            self.score -= MISSPENALTY
        else:
            for t in self.targets:
                if CheckTounching(pos, t.adjustedPos, self.target.get_size()):
                    self.targets.remove(t)
