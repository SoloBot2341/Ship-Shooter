import pygame
from assets import RenderText, createButtonWithText, player_skins
from MenuClass import Menu
from PlayerClass import Player
from BuffsClass import Buffs
from CollisionsClass import Collision
from MobsClass import Mobs
pygame.init(); pygame.font.init()

class Main():
    def __init__(self):
        self.SCREEN = pygame.display.set_mode((700,700))
        self.GAMING = 1
        self.WAVE = 1
        self.FPS = 60
        self.CLOCK = pygame.time.Clock()
        self.should_reset = False
        self.game_menu = Menu(self.SCREEN)
        self.player = Player(self.SCREEN,player_skins["hero"]())
        self.buffs = Buffs(self.SCREEN)
        self.mobs = Mobs(self.SCREEN)
        self.keys = None
        self.clicked = False
        self.current_event = "menu"
        self.states = {
            "menu" : lambda : self.menu_state(),
            "inGame" : lambda : self.inGame(),
            "pause" : lambda : self.paused(),
            "ship selection" : lambda : self.game_menu.chooseShip(self.player,self.clicked),
            "QUIT" : lambda : self.QUIT()
        }
        self.events = {
            pygame.K_p : "pause",
            pygame.K_SPACE : "inGame",
            pygame.K_m : "menu",
            pygame.K_z : "ship selection",
            pygame.K_ESCAPE : "QUIT"
        }

    def menu_state(self):
        RenderText(self.SCREEN, "PRESS SPACE TO PLAY!!!", pos=(100,350),font_size=50)
        createButtonWithText(self.SCREEN,[25,600,300,50], "Press z to choose a ship")
    def paused(self): 
        RenderText(self.SCREEN, "PRESS SPACE TO CONTINUE PLAYING", pos=(50,350),font_size=50)
    
    def QUIT(self): self.GAMING = 0

    def mousePressed(self,event):
        self.clicked = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: self.clicked = 1
            elif event.button == 3: self.clicked = -1

    def inGame(self):
        self.game_menu.renderMap(self.WAVE)
        self.player.update(self.keys)
        self.buffs.update()
        self.mobs.update(self.WAVE, self.should_reset)
        Collision.buff_collision(self.player,self.buffs)
        Collision.player_vs_mobs(self.player,self.mobs)
        self.reset(); self.getWave()
    
    def get_event(self):
        for event in self.events:
            if self.keys[event]: self.current_event = self.events[event]
    
    def getWave(self):
        if len(self.mobs.cur_mobs) <= 0 or not self.WAVE:
            self.WAVE += 1
        wave_text = f"WAVE {self.WAVE}"
        RenderText(self.SCREEN, wave_text, (25,10),font_size = 60, color = (0,0,0))
    
    def reset(self):
        if self.player.lost():
            self.WAVE = 1
        self.should_reset = self.player.max_lives <= 0
    
    def run(self):
        while self.GAMING:
            self.SCREEN.fill((0,0,0))
            for event in pygame.event.get():
                self.mousePressed(event)
                if event.type == pygame.QUIT:
                    self.QUIT()

            self.keys = pygame.key.get_pressed()
            self.get_event()
            self.states[self.current_event]()
            pygame.display.flip()
            self.CLOCK.tick(self.FPS)
        pygame.quit()

MAIN = Main()
MAIN.run()