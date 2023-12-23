import pygame,random
from assets import buff_imgs
from assets import timer

class Buffs():
    def __init__(self, SCREEN : pygame.Surface): 
        self.SCREEN = SCREEN
        self.stats = {
            "blue" : ["damage",10],
            "red"  : ["speed", 3],
            "green" : ["hp", 40]
        }
        self.images : dict[str, pygame.Surface] = buff_imgs
        self.buff = None
        self.spawnTimer = [start:=0, end:=1000]
        self.drawTimer = [start:=0, end:=3000]
        self.timer = timer
        self.key = ""

    def getBuff(self):
        self.key = random.choice([key for key in self.stats])
        x = random.choice([i*100 for i in range(3,7)])
        y = random.choice([i*100 for i in range(3,7)])
        self.buff = [self.images[self.key],pygame.Rect(x,y,75,75)]
    
    def drawBuff(self):
        self.SCREEN.blit(self.buff[0], (self.buff[1].x, self.buff[1].y))
    
    def getPair(self):
        return self.stats[self.key]

    def update(self):
        if self.timer(self.spawnTimer) and not self.buff: self.getBuff()
        if self.timer(self.drawTimer): self.buff = None
        if self.buff: self.drawBuff()