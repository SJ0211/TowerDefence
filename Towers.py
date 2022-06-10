import pygame
import math
from Projectile import Projectile
import time
import random
import Enemy

#direction stuff
def normalize_vector(vector):
    if vector == [0, 0]:
        return [0, 0]
    pythagoras = math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])
    return (vector[0] / pythagoras, vector[1] / pythagoras)


def rotate_vector(vector, theta):
    resultVector = (vector[0] * math.cos(theta)
                    - vector[1] * math.sin(theta),
                    vector[0] * math.sin(theta)
                    + vector[1] * math.cos(theta))
    return resultVector


class Tower1(pygame.sprite.Sprite):
    projectiles = pygame.sprite.Group()

    def __init__(self, pos):
        super().__init__()
        # get image
        self.image = pygame.image.load("base1.png")
        # self.image.fill(pygame.Color('black'))
        self.rect = self.image.get_rect(x=pos[0], y=pos[1])
        self.radius = self.rect.width / 2

        self.pos = list(pos)
        self.movementVector = [0, 0]
        self.lastShot = pygame.time.get_ticks()
        self.weaponCooldown = 1000
        self.Topimage = pygame.image.load("top1s.png")
        #recoil animation
        self.animationtime = 100

    # shoot
    def shoot(self, enemies):
        currentTime = pygame.time.get_ticks()
        Targetpos = self.target(enemies)

        # based on target pos, shoot at it
        if Targetpos != (0,0):
            if str(Targetpos) != 'None':
                if currentTime - self.lastShot > self.weaponCooldown:

                    direction = (Targetpos[0] - self.pos[0], Targetpos[1] - self.pos[1]) \
                        if Targetpos != self.pos else (1, 1)
                    self.lastShot = currentTime
                    self.projectiles.add(Projectile((6,6),((self.pos[0] + 25), (self.pos[1] + 25)),
                                                    normalize_vector(direction),
                                                    13, 4000, (100, 100, 100)))
                    self.Topimage = pygame.image.load("top1f.png")
                    sound = pygame.mixer.Sound("2.wav")
                    pygame.mixer.Sound.play(sound)
                    self.time = pygame.time.get_ticks()
        if currentTime - self.lastShot > self.animationtime:
            self.Topimage = pygame.image.load("top1s.png")


    #Identify most dangerous (close to our base) target and return its pos
    def target(self, enemies):
        inRange = pygame.sprite.Group()
        distancelist = []
        if len(enemies) <= 0:
            Targetpos = 0,0
            return Targetpos

        else:

            for e in enemies:
                ex, ey = e.pos
                sx, sy = self.pos
                x = int(abs(ex - sx))
                y = int(abs(ey - sy))
                D = math.sqrt(x**2 + y**2)
                #print(D)
                if D < 500:
                    inRange.add(e)
            enemyDict = {}

           # print(inRange)
            for e in inRange:

                enemyDict[e] = (e.distanceMoved)
                distancelist.append(e)

            if len(enemyDict) > 0:

                max_value = max(enemyDict.values())
                #print(max_value)
                enemyinlist = [k for k in enemyDict if enemyDict[k] == max_value]

                enemy = enemyinlist[0]

                #print(enemy)

                Targetpos = enemy.pos + enemy.direction * enemy.speed * (D/18)
                return Targetpos

    #blit
    def render(self, surface, enemies):

        Target = self.target(enemies)

        if str(Target) == 'None':

            tx = 0
            ty = 0

        else:


            tx, ty = Target

        surface.blit(self.image, self.pos)



        x, y = self.rect.center
        rel_x, rel_y = tx - x, ty - y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        TopimageCopy = pygame.transform.rotate(self.Topimage, angle)

        surface.blit(TopimageCopy, (x - int(TopimageCopy.get_width() / 2),
                                            y - int(TopimageCopy.get_height() / 2)))


# codes are almost same for other towers

class Tower2(pygame.sprite.Sprite):
    projectiles = pygame.sprite.Group()

    def __init__(self, pos):
        super().__init__()
        # get image
        self.image = pygame.image.load("base2.png")
        # self.image.fill(pygame.Color('black'))
        self.rect = self.image.get_rect(x=pos[0], y=pos[1])
        self.radius = self.rect.width / 2

        self.pos = list(pos)
        self.movementVector = [0, 0]
        self.lastShot = pygame.time.get_ticks()
        self.weaponCooldown = 100
        self.animationtime = 50
        self.Topimage = pygame.image.load("top2s.png")
        self.shots = 0
        self.spreadArc = 20


    def shoot(self, enemies):
        currentTime = pygame.time.get_ticks()
        Targetpos = self.target(enemies)

        if Targetpos != (0, 0):
            if str(Targetpos) != 'None':
                if currentTime - self.lastShot > self.weaponCooldown:
                    direction = (Targetpos[0] - self.pos[0], Targetpos[1] - self.pos[1]) \
                        if Targetpos != self.pos else (1, 1)
                    self.lastShot = currentTime
                    theta = math.radians(random.random() * self.spreadArc - self.spreadArc / 2)
                    projDir = rotate_vector(direction, theta)
                    self.projectiles.add(Projectile((6, 6), ((self.pos[0] + 25), (self.pos[1] + 25)),
                                                    normalize_vector(projDir),
                                                    8, 1200, (200, 200, 0)))
                    if self.shots == 0:
                        self.Topimage = pygame.image.load("top2f1.png")
                        self.shots = 1
                    elif self.shots == 2:
                        self.Topimage = pygame.image.load("top2f2.png")
                        self.shots = 0
                    elif self.shots == 1:
                        self.Topimage = pygame.image.load("top2f3.png")
                        self.shots = 2

                    sound = pygame.mixer.Sound("2.wav")
                    pygame.mixer.Sound.play(sound)
                    self.time = pygame.time.get_ticks()
        if currentTime - self.lastShot > self.animationtime:
            self.Topimage = pygame.image.load("top2s.png")





    def target(self, enemies):
        inRange = pygame.sprite.Group()
        distancelist = []
        if len(enemies) <= 0:
            Targetpos = 0, 0
            return Targetpos

        else:

            for e in enemies:
                ex, ey = e.pos
                sx, sy = self.pos
                x = int(abs(ex - sx))
                y = int(abs(ey - sy))
                D = math.sqrt(x ** 2 + y ** 2)
                # print(D)
                if D < 600:
                    inRange.add(e)
            enemyDict = {}

            # print(inRange)
            for e in inRange:
                enemyDict[e] = (e.distanceMoved)
                distancelist.append(e)

            if len(enemyDict) > 0:
                max_value = max(enemyDict.values())
                # print(max_value)
                enemyinlist = [k for k in enemyDict if enemyDict[k] == max_value]

                enemy = enemyinlist[0]

                # print(enemy)

                Targetpos = enemy.pos + enemy.direction * enemy.speed * (D / 18)
                return Targetpos

    def render(self, surface, enemies):

        Target = self.target(enemies)

        if str(Target) == 'None':

            tx = 0
            ty = 0

        else:

            tx, ty = Target

        surface.blit(self.image, self.pos)

        x, y = self.rect.center
        rel_x, rel_y = tx - x, ty - y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        TopimageCopy = pygame.transform.rotate(self.Topimage, angle)

        surface.blit(TopimageCopy, (x - int(TopimageCopy.get_width() / 2),
                                    y - int(TopimageCopy.get_height() / 2)))

class Tower3(pygame.sprite.Sprite):
    projectiles = pygame.sprite.Group()

    def __init__(self, pos):
        super().__init__()
        # get image
        self.image = pygame.image.load("base3.png")
        # self.image.fill(pygame.Color('black'))
        self.rect = self.image.get_rect(x=pos[0], y=pos[1])
        self.radius = self.rect.width / 2

        self.pos = list(pos)
        self.movementVector = [0, 0]
        self.lastShot = pygame.time.get_ticks()
        self.weaponCooldown = 2000
        self.Topimage = pygame.image.load("top3s.png")
        self.animationtime = 150

    def shoot(self, enemies):
        currentTime = pygame.time.get_ticks()
        Targetpos = self.target(enemies)

        if Targetpos != (0, 0):
            if str(Targetpos) != 'None':
                if currentTime - self.lastShot > self.weaponCooldown:
                    direction = (Targetpos[0] - self.pos[0], Targetpos[1] - self.pos[1]) \
                        if Targetpos != self.pos else (1, 1)
                    self.lastShot = currentTime
                    self.projectiles.add(Projectile((20, 20), ((self.pos[0] + 25), (self.pos[1] + 25)),
                                                    normalize_vector(direction),
                                                    10, 5000, (0, 0, 255)))
                    self.Topimage = pygame.image.load("top3f.png")
                    sound = pygame.mixer.Sound("3.wav")
                    pygame.mixer.Sound.play(sound)


        if currentTime - self.lastShot > self.animationtime:
            self.Topimage = pygame.image.load("top3s.png")

    def target(self, enemies):
        inRange = pygame.sprite.Group()
        distancelist = []
        if len(enemies) <= 0:
            Targetpos = 0, 0
            return Targetpos

        else:

            for e in enemies:
                ex, ey = e.pos
                sx, sy = self.pos
                x = int(abs(ex - sx))
                y = int(abs(ey - sy))
                D = math.sqrt(x ** 2 + y ** 2)
                # print(D)
                if D < 500:
                    inRange.add(e)
            enemyDict = {}

            # print(inRange)
            for e in inRange:
                enemyDict[e] = (e.distanceMoved)
                distancelist.append(e)

            if len(enemyDict) > 0:
                max_value = max(enemyDict.values())
                # print(max_value)
                enemyinlist = [k for k in enemyDict if enemyDict[k] == max_value]

                enemy = enemyinlist[0]

                # print(enemy)

                Targetpos = enemy.pos + enemy.direction * enemy.speed * (D / 18)
                return Targetpos

    def render(self, surface, enemies):

        Target = self.target(enemies)

        if str(Target) == 'None':

            tx = 0
            ty = 0

        else:

            tx, ty = Target

        surface.blit(self.image, self.pos)

        x, y = self.rect.center
        rel_x, rel_y = tx - x, ty - y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        TopimageCopy = pygame.transform.rotate(self.Topimage, angle)

        surface.blit(TopimageCopy, (x - int(TopimageCopy.get_width() / 2),
                                    y - int(TopimageCopy.get_height() / 2)))

class Tower4(pygame.sprite.Sprite):
    projectiles = pygame.sprite.Group()

    def __init__(self, pos):
        super().__init__()
        # get image
        self.image = pygame.image.load("base4.png")
        # self.image.fill(pygame.Color('black'))
        self.rect = self.image.get_rect(x=pos[0], y=pos[1])
        self.radius = self.rect.width / 2

        self.pos = list(pos)
        self.movementVector = [0, 0]
        self.lastShot = pygame.time.get_ticks()
        self.weaponCooldown = 4000
        self.Topimage = pygame.image.load("top4s.png")
        self.animationtime = 200

    def shoot(self, enemies):
        currentTime = pygame.time.get_ticks()
        Targetpos = self.target(enemies)

        if Targetpos != (0, 0):
            if str(Targetpos) != 'None':
                if currentTime - self.lastShot > self.weaponCooldown:
                    direction = (Targetpos[0] - self.pos[0], Targetpos[1] - self.pos[1]) \
                        if Targetpos != self.pos else (1, 1)
                    self.lastShot = currentTime
                    self.projectiles.add(Projectile((50, 50), ((self.pos[0] + 25), (self.pos[1] + 25)),
                                                    normalize_vector(direction),
                                                    15, 5000, (255, 10, 10)))
                    self.Topimage = pygame.image.load("top4f.png")
                    sound = pygame.mixer.Sound("3.wav")
                    pygame.mixer.Sound.play(sound)

        if currentTime - self.lastShot > self.animationtime:
            self.Topimage = pygame.image.load("top4s.png")

    def target(self, enemies):
        inRange = pygame.sprite.Group()
        distancelist = []
        if len(enemies) <= 0:
            Targetpos = 0, 0
            return Targetpos

        else:

            for e in enemies:
                ex, ey = e.pos
                sx, sy = self.pos
                x = int(abs(ex - sx))
                y = int(abs(ey - sy))
                D = math.sqrt(x ** 2 + y ** 2)
                # print(D)
                if D < 500:
                    inRange.add(e)
            enemyDict = {}

            # print(inRange)
            for e in inRange:
                enemyDict[e] = (e.distanceMoved)
                distancelist.append(e)

            if len(enemyDict) > 0:
                max_value = max(enemyDict.values())
                # print(max_value)
                enemyinlist = [k for k in enemyDict if enemyDict[k] == max_value]

                enemy = enemyinlist[0]

                # print(enemy)

                Targetpos = enemy.pos + enemy.direction * enemy.speed * (D / 18)
                return Targetpos

    def render(self, surface, enemies):

        Target = self.target(enemies)

        if str(Target) == 'None':

            tx = 0
            ty = 0

        else:

            tx, ty = Target

        surface.blit(self.image, self.pos)

        x, y = self.rect.center
        rel_x, rel_y = tx - x, ty - y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        TopimageCopy = pygame.transform.rotate(self.Topimage, angle)

        surface.blit(TopimageCopy, (x - int(TopimageCopy.get_width() / 2),
                                    y - int(TopimageCopy.get_height() / 2)))
