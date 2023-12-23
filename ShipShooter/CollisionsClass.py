import pygame
from assets import timer

class Collision():
    damage_watch = [0,10]

    "to be used with the player and buff class, determines if a player needs a buff"
    @staticmethod
    def buff_collision(player,buff_obj):
        if buff_obj.buff and player.rect.colliderect(buff_obj.buff[1]):
            player.updateStats(buff_obj.getPair())
            player.weapon.getBullet(buff_obj.key)
            buff_obj.buff = None
            return
        if buff_obj.drawTimer[0] == buff_obj.drawTimer[1]:
            player.updateStats(None)
            player.weapon.getBullet(None)
    
    "will check if the player or a mob attack is colliding w mob/player rectangle"
    def player_vs_mobs(player, mobs, damage_watch = damage_watch):
        remaining_bullets = []
        for player_bullet_rect in player.weapon.bullet_rects:
            for mob in mobs.cur_mobs:
                if mob.rect.colliderect(player_bullet_rect) and timer(damage_watch):
                    mob.stats["hp"][0] -= player.stats["damage"][0]
                    player_bullet_rect = None
                    break
                if mob.stats["hp"][0] <= 0: mob.sounds["killed"].play()
            if player_bullet_rect: remaining_bullets.append(player_bullet_rect)
        player.weapon.bullet_rects = remaining_bullets
        for mob in mobs.cur_mobs:
            remaining_bullets = []
            for mob_bullet_rect in mob.weapon.bullet_rects:
                if mob_bullet_rect.colliderect(player.rect) and timer(damage_watch):
                    player.stats["hp"][0] -= mob.stats["damage"][0]
                    mob_bullet_rect = None
                else:
                    remaining_bullets.append(mob_bullet_rect)
            mob.weapon.buller_rects = remaining_bullets