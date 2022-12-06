import pygame
import sys
from pygame.display import set_mode
from pygame.locals import *

arrowUpxPos = 120
arrowDownxPos = 220
yAlignment = -20

goButtonPos = (300,400)

xUpPos = (arrowUpxPos, 100 + yAlignment)
xDownPos = (arrowDownxPos, 100 + yAlignment)
yUpPos = (arrowUpxPos, 200 + yAlignment)
yDownPos = (arrowDownxPos, 200 + yAlignment)
rateUpPos = (arrowUpxPos, 300 + yAlignment)
rateDownPos = (arrowDownxPos, 300 + yAlignment)
timeUpPos = (arrowUpxPos, 400 + yAlignment)
timeDownPos = (arrowDownxPos, 400 + yAlignment)

arrows = {timeDownPos, timeUpPos, rateDownPos, rateUpPos, yDownPos, yUpPos, xDownPos, xUpPos}


class SetUp:
    def __init__(self):
        #Member variables
        self.xSize = 500
        self.ySize = 500
        self.rate = 1
        self.time = 30
        
        #Start pygame
        pygame.init()
        self.screen = pygame.display.set_mode((400,500))
        pygame.display.set_caption("Aim Of The Game")

        #Load assets
        self.upArrow = pygame.image.load('Assets/up_arrow.png').convert()
        self.downArrow = pygame.image.load('Assets/down_arrow.png').convert()
        self.goButton = pygame.image.load('Assets/go_button.png').convert()
        if pygame.font:
            self.font = pygame.font.Font(None, 40)

        #Set up Pygame
        self.clock = pygame.time.Clock()

        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((239,228,176))

    def CheckTounching(self, pos1, pos2, size):
        if ((pos1[0] >= pos2[0] and pos1[0] <= pos2[0] + size[0]) and (pos1[1] >= pos2[1] and pos1[1] <= pos2[1] + size[1])):
            return True
        else:
            return False

    def HandleInput(self):
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                for arrow in arrows:
                    if self.CheckTounching(pos, arrow, self.upArrow.get_size()):
                        if arrow == xUpPos:
                            self.xSize += 10
                        elif arrow == xDownPos:
                            if self.xSize > 100:
                                self.xSize -= 10
                        elif arrow == yUpPos:
                            self.ySize += 10
                        elif arrow == yDownPos:
                            if self.ySize > 100:
                                self.ySize -= 10
                        elif arrow == rateUpPos:
                            self.rate += 1
                        elif arrow == rateDownPos:
                            if self.rate > 1:
                                self.rate -= 1
                        elif arrow == timeUpPos:
                            self.time += 1
                        elif arrow == timeDownPos:
                            if self.time > 1:
                                self.time -= 1
                if self.CheckTounching(pos, goButtonPos, self.goButton.get_size()):
                    return (self.xSize, self.ySize, self.rate, self.time)

    def Run(self):
        while(1):
            #Handle input
            ret = self.HandleInput()
            if ret != None:
                pygame.quit()
                return ret

            #clear screen
            self.screen.blit(self.background,(0,0))

            #Draw the text
            xString = 'X size:             ' + str(self.xSize)
            yString = 'Y size:             ' + str(self.ySize)
            zString = 'Target time (seconds): ' + str(self.rate)
            minesString = 'Time (seconds):   ' + str(self.time)
            xTxt = self.font.render(xString, True, (10,10,10))
            yTxt = self.font.render(yString, True, (10,10,10))
            zTxt = self.font.render(zString, True, (10,10,10))
            minesTxt = self.font.render(minesString, True, (10,10,10))
            self.screen.blit (xTxt, (50, 50))
            self.screen.blit (yTxt, (50, 150))
            self.screen.blit (zTxt, (50, 250))
            self.screen.blit (minesTxt, (50, 350))

            #Draw the arrows
            for arrow in arrows:
                if arrow[0] == arrowUpxPos:
                    self.screen.blit(self.upArrow, arrow)
                else:
                    self.screen.blit(self.downArrow, arrow)
            #Draw go button
            self.screen.blit(self.goButton, goButtonPos)

            pygame.display.flip()
            self.clock.tick(60)