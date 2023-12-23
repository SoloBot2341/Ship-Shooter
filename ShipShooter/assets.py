import pygame, os
pygame.mixer.init()

def folderToDict(folder_path):
    dict = {}
    for filename in os.listdir(folder_path):
        if filename.endswith((".png", ".jpg", ".jpeg", ".gif", ".wav")):
            name = os.path.splitext(filename)[0]
            path = os.path.join(folder_path, filename)
            dict[name] = path
    return dict

def loadImgs(images : dict[str,str], reverse=False) -> dict[str,pygame.Surface]: 
    for img in images:
        images[img] = pygame.image.load(images[img])
        if reverse:
            images[img] = pygame.transform.flip(images[img])
    return images

def RenderText(SCREEN, text, pos, font_name='Arial', font_size=30, color=(255, 255, 255)):
    font = pygame.font.SysFont(font_name, font_size)
    text_surface = font.render(text, True, color)
    SCREEN.blit(text_surface, pos)

def loadSound(sounds : dict[str,str])-> dict[str, pygame.mixer.Sound]:
    for name in sounds:
        sounds[name] = pygame.mixer.Sound(sounds[name])
    return sounds

def createButtonWithText(SCREEN : pygame.Surface, rect_args : tuple[int],
    text : str, 
    color = (100,2,29)
    ):
    pos = (rect_args[0], rect_args[1])
    rect = pygame.Rect(*rect_args)
    pygame.draw.rect(SCREEN, color,rect)
    RenderText(SCREEN, text, pos)
    return rect

def timer(watch : [int,int], reset = 0):
    start,end = 0,1
    if watch[start] < watch[end]:
        watch[start] += 1
        return False
    watch[start] = reset
    return True

game_maps = loadImgs(folderToDict("maps"))
player_skins = {
    "hero" : lambda : loadImgs(folderToDict("ships/Hero")),
    "royce" : lambda : loadImgs(folderToDict("ships/Royce")),
    "ufo" : lambda : loadImgs(folderToDict("ships/Ufo"))
    }
player_bullet_imgs = loadImgs(folderToDict("ships/bullets"))
player_sounds = loadSound(folderToDict("sounds/ships"))
player_dead_sound = pygame.mixer.Sound("sounds/ships/deadPlayer/dead.wav")
buff_imgs = loadImgs(folderToDict("buffs"))
mob_imgs = loadImgs(folderToDict("mobs"))
mob_sounds = loadSound(folderToDict("sounds/mobs"))
mob_bullet_imgs = loadImgs(folderToDict("mobs/bullets"))