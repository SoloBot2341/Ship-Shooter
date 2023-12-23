import pygame, random
#dict[str, pygame.Surface] and [str, pygame.mixer.Sound]
from assets import mob_imgs,mob_bullet_imgs, mob_sounds
from ProjectilesClass import Projectiles #[pygame.Surface, object]
from assets import timer

class CreateMob():
    def __init__(self, type : str, SCREEN : pygame.Surface, image : pygame.Surface,stats : list[int]):
        watch_map = {"red" : [0,2],"blue" : [0,4], "green" : [0,6]}
        self.weapon = Projectiles(SCREEN, self, mob_bullet_imgs, mob_sounds)
        self.init_Weapon(type)
        self.sounds = mob_sounds
        self.image = image
        self.SCREEN = SCREEN
        self.rect = self.init_rect()
        self.shift_watch = watch_map[type]
        self.movement = [True,False]
        self.stats = {
            "speed" : [stats[0]],
            "damage" : [stats[1]],
            "hp" : [stats[2]]
        }
    "using a function to create a rect to avoid copies"
    def init_rect(self):
        x,y = random.choice([i*100 for i in range(0,7)]), random.choice([i for i in range(0,200)]),
        w,h = self.image.get_width(), self.image.get_height()
        return pygame.Rect(x,y,w,h)

    def init_Weapon(self,type : str):
        self.weapon.getBullet(type)
        self.weapon.direction *= -1
        self.weapon.firing_watch = [25,25]

    def move(self):
        if timer(self.shift_watch):
            spd = self.stats["speed"][0]
            self.rect.x += self.movement[0] * spd or -self.movement[1] * spd 
        if self.rect.x >= self.SCREEN.get_width()-100: self.movement = [False,True]
        if self.rect.x <= 0: self.movement = [True,False]
    
    def update(self):
        self.SCREEN.blit(self.image, (self.rect.x, self.rect.y))
        self.move()
        self.weapon.update(None,False)

class Mobs():
    def __init__(self, SCREEN):
        self.types = {
            "blue" : ("blue",SCREEN, mob_imgs["blue"],[2,10,70]),
            "red" : ("red",SCREEN,mob_imgs["red"], [3,6,50]),
            "green" : ("green",SCREEN,mob_imgs["green"], [2,4,100]),
        }
        self.cur_mobs = []
        self.cur_wave = 0
    
    def getMobs(self, cur_wave : int):
        self.cur_mobs = [CreateMob(*self.types[random.choice([key for key in self.types])])for i in range(min(1*cur_wave,50))]
        
    def updateAll(self):
        remaining_mobs = []
        for mob in self.cur_mobs:
            if mob.stats["hp"][0] > 0:
                mob.update()
                remaining_mobs.append(mob)
        self.cur_mobs = remaining_mobs
            
    def update(self, cur_wave : int, reset : bool):
        if self.cur_wave < cur_wave or reset:
            self.cur_mobs = []
            self.cur_wave = cur_wave
            self.getMobs(cur_wave)
        self.updateAll()