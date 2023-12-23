import pygame
from assets import game_maps, RenderText,player_skins,createButtonWithText
CBWT = createButtonWithText
class Menu():
    def __init__(self, SCREEN : pygame.Surface) -> None:
        self.SCREEN = SCREEN
        self.images : dict[str,pygame.Surface] = game_maps
        self.cur_map = "sky"
        self.index = 0
        self.prev_wave = 0
    
    def renderMap(self,WAVE):
        if WAVE%2==0 and self.prev_wave != WAVE: self.getMap()
        self.SCREEN.blit(self.images[self.cur_map], (0,0))
        self.prev_wave = WAVE

    "player is the player object"
    def chooseShip(self,player, clicked : int):
        RenderText(self.SCREEN, f"current ship {player.ship_name}",(250,450))
        CBWT(self.SCREEN, [35,35,300,30], "Press M to return to Menu.")
        CBWT(self.SCREEN, [35,100,350,30], "Press space to return to game.")
        mouse_rect = pygame.Rect(*pygame.mouse.get_pos(), 20, 20)
        x,y = [100,300]
        for skin in player_skins:
            images = player_skins[skin]()
            RenderText(self.SCREEN, skin, [x,y+75])
            temp_rect = images["ship"].get_rect()
            temp_rect.x,temp_rect.y = x,y
            self.SCREEN.blit(images["ship"], [x,y])
            if temp_rect.colliderect(mouse_rect) and clicked == 1:
                pygame.draw.rect(self.SCREEN, (200,200,200),temp_rect)
                player.ship_name = skin
                player.images = list(images.values())
            x += 200

    def getMap(self):
        keys = list(self.images.keys())
        if self.index < len(keys)-1:
            self.index += 1
        else:
            self.index = 0
        self.cur_map = keys[self.index]