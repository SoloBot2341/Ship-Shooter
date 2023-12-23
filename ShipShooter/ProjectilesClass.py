import pygame
from assets import timer
from assets import RenderText

class Bullet():
    def __init__(self, ammo : list[int], image : pygame.Surface, sound :pygame.mixer.Sound, rect_args:list[int],offset=40):
        self.ammo = ammo
        self.image = image
        self.rect_args = rect_args
        self.offset = -offset
        self.sound = sound
        self.ammo_text = lambda : f"Bullets : {self.ammo[0]} / {self.ammo[1]}"

class Projectiles():
    def __init__(self,SCREEN : pygame.Surface, obj, image_dict : dict[str,pygame.Surface], sound_dict : dict[pygame.mixer.Sound]):
        self.SCREEN = SCREEN
        #object needs a rect attr.
        self.obj = obj
        self.table = {
            "blue" : lambda : Bullet([5,5], image_dict["blue"],sound_dict["blue"], [0,0,50,50]),
            "red" :  lambda : Bullet([15,15], image_dict["red"],sound_dict["red"], [0,0,20,20],20),
            "green" : lambda : Bullet([3,3], image_dict["green"],sound_dict["green"], [0,0,50,75],60),
            "default" : lambda : Bullet([7,7], image_dict.get("default",0),sound_dict.get("default",0),[0,0,35,35])
        }
        self.key = "default"
        self.direction = 1
        self.can_fire = True
        self.bullet = self.table[self.key]()
        self.bullet_rects = []
        self.firing_watch = [start:=0, end:=20]
        self.reload_watch = [start:=0, end:=100]
        self.is_reloading = False

    def getBullet(self, key : str):
        if key == None: self.key = "default"
        else: self.key = key
        self.bullet = self.table[self.key]()
        self.bullet_rects = []
        self.is_reloading = False
        self.bullet.ammo[0] = self.bullet.ammo[1]

    def reload(self):
        if timer(self.reload_watch) and self.bullet.ammo[0] < self.bullet.ammo[1]: 
            self.bullet.ammo[0] += 1
            self.is_reloading = False

    def bulletTrigger(self, keys, is_player):
        if self.is_reloading: return
        def init():
            self.bullet.ammo[0] -= 1
            self.bullet.rect_args[0] = self.obj.rect.x
            self.bullet.rect_args[1] = self.obj.rect.y+self.bullet.offset*self.direction
            self.bullet.sound.play()
            self.bullet_rects.append(pygame.Rect(*self.bullet.rect_args))
        if is_player and keys[pygame.K_1] and self.can_fire:init()
        if not is_player:init()
        if self.bullet.ammo[0] <= 0: self.is_reloading = True

    def renderBullets(self):
        remaining_bullets = []
        for bullet in self.bullet_rects:
            if self.SCREEN.get_height() >= bullet.y >= 0:
                bullet.y -= self.direction * self.obj.stats["speed"][0]
                remaining_bullets.append(bullet)
                self.SCREEN.blit(self.bullet.image, (bullet.x,bullet.y))
        self.bullet_rects = remaining_bullets

    def update(self, keys, is_player=True):
        if is_player: RenderText(self.SCREEN, self.bullet.ammo_text(), (25,600))
        self.bulletTrigger(keys,is_player)
        self.can_fire = timer(self.firing_watch)
        self.renderBullets()
        self.reload()