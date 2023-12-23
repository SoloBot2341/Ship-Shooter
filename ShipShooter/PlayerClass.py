import pygame
from assets import player_bullet_imgs, player_sounds,RenderText,player_dead_sound,timer
from ProjectilesClass import Projectiles

class Player():
    def __init__(self, SCREEN : pygame.Surface, images : dict[str, pygame.Surface]):
        self.max_lives = 3
        self.SCREEN = SCREEN
        self.ship_name = "hero"
        self.images = list(images.values())
        self.image = self.images[0]
        self.rect = pygame.Rect(350,500,75,75)
        self.frame = 0
        self.weapon = Projectiles(SCREEN, self, player_bullet_imgs, player_sounds)
        self.weapon.firing_watch = [10,10]
        self.weapon.reload_watch = [0,50]
        self.sound_watch = [0,90]
        self.dead_sound = player_dead_sound

        self.stats = {
            "speed" : [5,5],
            "hp" : [100,100],
            "damage" : [15,15]
        }
        self.movement = {
            pygame.K_d : [spd:=self.stats["speed"][0], 0],
            pygame.K_a : [-spd, 0],
            pygame.K_w : [0, -spd],
            pygame.K_s : [0, spd]
        }
    
    def move(self, keys):
        for move in self.movement:
            if keys[move]:
                self.rect.x += self.movement[move][0]
                self.rect.y += self.movement[move][1]

    def updateStats(self, pair : [str,int]):
        if not pair:
            for key in self.stats:
                if key != "hp": 
                    self.stats[key][0] = self.stats[key][1]
            return
        self.stats[pair[0]][0] += pair[1]
    
    def animate(self, speed : int):
        if self.frame < len(self.images):
            self.frame += speed
        else:
            self.frame = 0
        self.image = self.images[int(self.frame)-1]
    
    def isKilled(self):
        if self.stats["hp"][0] <= 0:
            self.max_lives -= 1
            self.rect.x,self.rect.y = [300,600]
            self.stats["hp"][0] = self.stats["hp"][1]
            self.weapon.key = "default"
    
    def renderHealth(self):
        lives = f"Lives: {self.max_lives}"
        health = f"Health: {self.stats['hp'][0]}"
        RenderText(self.SCREEN, lives, (25, 550), color=(255,0,0))
        RenderText(self.SCREEN, health, (25,650), color=(0,255,0))
    
    def lost(self):
        if self.max_lives > 0: return
        if not timer(self.sound_watch):
            self.SCREEN.fill((0,0,0))
            RenderText(self.SCREEN, "YOU LOST", (300, 350))
            self.dead_sound.play()
            return True
        self.max_lives = 3
            
    def update(self, keys):
        self.weapon.update(keys)
        self.move(keys)
        self.animate(.1)
        self.SCREEN.blit(self.image, (self.rect.x,self.rect.y))
        self.renderHealth()
        self.isKilled()