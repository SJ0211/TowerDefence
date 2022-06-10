import pygame
import math
import sys
import Towers
from Projectile import Projectile

PlayerHealth = 8
PlayerMoney = 200


#Enemy1
class Enemy1(pygame.sprite.Sprite):


    def __init__(self, pos, collision_rects):
        super().__init__()
        self.image = pygame.image.load("enemy.png")
        self.rect = self.image.get_rect(centerx=pos[0], centery=pos[1])
        self.copy = self.image
        self.pos = self.rect.center
        self.speed = 2
        self.direction = pygame.math.Vector2(0, 0)
        self.collision_rects = collision_rects



        self.health = 10
        self.movementVector = [0, 0]
        self.movementSpeed = self.speed
        self.distanceMoved = 0
        self.angle = 0
        self.slowtime = 0
        self.slowed = False


    #search for net rect
    def get_direction(self):
        if self.collision_rects:
            start = pygame.math.Vector2(self.pos)
            end = pygame.math.Vector2(self.collision_rects[0].center)
            self.direction = (end - start).normalize()
        else:
            self.direction = pygame.math.Vector2(0, 0)
    #delete stuff if hit
    def check_collisions(self):
        if self.collision_rects:
            for rect in self.collision_rects:
                if len(self.collision_rects) <= 1:
                    break
                elif rect.collidepoint(self.pos):
                    del self.collision_rects[0]
                    self.get_direction()



    #update
    def update(self, towers):
        global PlayerMoney
        global PlayerHealth


        self.pos += self.direction * self.speed
        self.check_collisions()
        self.rect.center = self.pos
        self.distanceMoved = pygame.time.get_ticks() * self.movementSpeed


        if pygame.sprite.spritecollide(self, Towers.Tower1.projectiles, True):
            print("hit!")
            self.health -= 1
        if pygame.sprite.spritecollide(self, Towers.Tower2.projectiles, True):
            self.health -= 0.7
        if pygame.sprite.spritecollide(self, Towers.Tower3.projectiles, True):
            self.health -= 3
            if self.slowed == False:
                self.speed -= 1.5
                self.slowed = True
            self.slowtime = pygame.time.get_ticks()
        if pygame.sprite.spritecollide(self, Towers.Tower4.projectiles, True):
            self.health -= 20

        if self.health <= 0:
            sound = pygame.mixer.Sound("money.wav")
            pygame.mixer.Sound.play(sound)
            PlayerMoney += 50
            self.kill()


        if self.rect.right > 1130 and self.rect.bottom > 650:
            sound = pygame.mixer.Sound("lost.wav")
            pygame.mixer.Sound.play(sound)
            PlayerHealth -= 1
            self.kill()




        if (self.slowed == True) and (pygame.time.get_ticks() - self.slowtime > 2500):
            self.speed += 3
            self.slowed = False

        x, y = self.rect.center
        cx, cy = self.collision_rects[0].center
        rel_x, rel_y = cx - x, cy - y
        self.angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

    #render
    def render(self, surface):

        self.copy = pygame.transform.rotate(self.image, self.angle)

        surface.blit(self.copy, ((self.pos[0] - 20), (self.pos[1] - 25)))


        pygame.draw.rect(surface, (255, 0, 0), (self.pos[0] -25, self.pos[1] + 30, (5 * (self.health)), 5))



