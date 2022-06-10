import pygame
import random
import Towers
import Enemy
from Projectile import Projectile
import math
from pygame import RLEACCEL
import Path

#basic settings
pygame.init()
size = (1200, 720)
BGCOLOR = (255, 255, 255)
screen = pygame.display.set_mode(size)
Font = pygame.font.Font("UpheavalPro.ttf", 30)
healthFont = pygame.font.Font("OmnicSans.ttf", 50)
healthRender = healthFont.render('z', True, pygame.Color('red'))
pygame.display.set_caption("SJ Pygame")
bg = pygame.image.load("background1.png").convert()
pygame.mouse.set_visible(False)  # hide the cursor


# Image for "manual" cursor
MANUAL_CURSOR = pygame.image.load('aim1.png').convert_alpha()
ENEMY_SPAWN = pygame.image.load('EB.png').convert()
BASE = pygame.image.load('MB.png').convert()

done = False
enemies = pygame.sprite.Group()
towers = pygame.sprite.Group()
walls = pygame.sprite.Group()
lastEnemy = 0
score = 0
clock = pygame.time.Clock()
Towerselection = 0

#class for wall

class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, collision_rects, Status):
        super().__init__()
        self.pos = list(pos)


        self.image = pygame.image.load("wall.png")
        # self.image.set_colorkey((PLAYERCOLOR), RLEACCEL)
        self.rect = self.image.get_rect(x=size[0] // 2,
                                        y=size[1] // 2)


    def render(self, surface):

        surface.blit(self.image, self.pos)


#update
def move_entities(towers, enemies, timeDelta):
    global screen
    global health


    score = 0


    for enemy in enemies:
        enemy.update(towers)


    for tower in towers:
        tower.shoot(enemies)

    for proj in Towers.Tower1.projectiles:
        proj.move(screen.get_size(), timeDelta)



    for proj in Towers.Tower2.projectiles:
        proj.move(screen.get_size(), timeDelta)



    for proj in Towers.Tower3.projectiles:
        proj.move(screen.get_size(), timeDelta)


    for proj in Towers.Tower4.projectiles:
        proj.move(screen.get_size(), timeDelta)



    return score

#blit
def render_entities(towers, enemies):
    for wall in walls:
        wall.render(screen)
    for tower in towers:
        tower.render(screen, enemies)

    for proj in Towers.Tower1.projectiles:
        proj.render(screen)

    for proj in Towers.Tower2.projectiles:
        proj.render(screen)
    for proj in Towers.Tower3.projectiles:
        proj.render(screen)
    for proj in Towers.Tower4.projectiles:
        proj.render(screen)

    for enemy in enemies:
        enemy.render(screen)

#once keys pressed
def process_keys(keys):
    global MANUAL_CURSOR
    global Towerselection
    if keys[pygame.K_q]:
        Towerselection = 0
        MANUAL_CURSOR = pygame.image.load('aim1.png').convert_alpha()
    if keys[pygame.K_1]:
        Towerselection = 1
        MANUAL_CURSOR = pygame.image.load('aim2.png').convert_alpha()
    if keys[pygame.K_2]:
        Towerselection = 2
        MANUAL_CURSOR = pygame.image.load('aim3.png').convert_alpha()
    if keys[pygame.K_3]:
        Towerselection = 3
        MANUAL_CURSOR = pygame.image.load('aim4.png').convert_alpha()
    if keys[pygame.K_4]:
        Towerselection = 4
        MANUAL_CURSOR = pygame.image.load('aim5.png').convert_alpha()
    if keys[pygame.K_w]:
        Towerselection = 5
        MANUAL_CURSOR = pygame.image.load('aim6.png').convert_alpha()
    #if keys[pygame.K_ESCAPE]:
        #options()


def process_mouse(mouse, TowerSelection):
    global matrix
    global Money
    global towers
    global path
    global Delaylast
    global wave
    global Status


    mouse_pos = pygame.mouse.get_pos()
    row = mouse_pos[1] // 60
    col = mouse_pos[0] // 60
    current_cell_value = matrix[row + 1][col+ 1]
    if wave == False:
        if not (row,col) == (0,0):
            if not (row,col) == (11, 19):
                if TowerSelection == 0:
                    if current_cell_value == 1:
                        x = col * 60
                        y = row * 60
                        pos = (x + 5, y + 5)
                        pos1 = (x,y)
                        rect = pygame.Rect((col * 60, row *60), (60,60))
                        screen.blit(pygame.image.load('selection.png').convert_alpha(),rect)

                        if mouse[0]:

                            matrix[row + 1][col+ 1] = 2
                            matrix1[row + 1][col + 1] = 0

                            try:
                                collision_rects = Path.find_path(matrix1)
                            except:
                                collision_rects = []
                                pass


                            if str(collision_rects) == 'None':
                                Status = "Can't Place there!"
                                matrix[row + 1][col + 1] = 1
                                matrix1[row + 1][col + 1] = 1

                            else:

                                loop = False
                                Status = "Normal"
                                walls.add(Wall(pos1, collision_rects, Status))

                                Enemy.PlayerMoney -= 10

                #deleting
                elif TowerSelection == 5:
                    if current_cell_value == 3:
                        x = col * 60
                        y = row * 60
                        rect = pygame.Rect((col * 60, row * 60), (60, 60))
                        screen.blit(pygame.image.load('selection.png').convert_alpha(), rect)
                        if pygame.mouse.get_pressed()[0]:
                            print("deleting wall")

                            towerDict = {}

                            for e in towers:
                                towerDict[e] = str(e.pos)


                            for key in towerDict.values():

                                if key == "["+ str(x+5) + ", " + str(y+5) +"]":
                                    toweronspot = list(towerDict.keys())[list(towerDict.values()).index(key)]
                                    toweronspot.kill()

                            Delaylast = pygame.time.get_ticks()

                            matrix[row + 1][col + 1] = 2

                    elif current_cell_value == 2 and (pygame.time.get_ticks() - Delaylast) > 200:
                        x = col * 60
                        y = row * 60
                        pos = (x, y)
                        rect = pygame.Rect((col * 60, row * 60), (60, 60))
                        screen.blit(pygame.image.load('selection.png').convert_alpha(), rect)
                        if pygame.mouse.get_pressed()[0]:


                            wallDict = {}

                            for e in walls:
                                wallDict[e] = str(e.pos)


                            for key in wallDict.values():

                                if key == "["+ str(x) + ", " + str(y) +"]":
                                    wallonspot = list(wallDict.keys())[list(wallDict.values()).index(key)]
                                    wallonspot.kill()
                            matrix[row + 1][col + 1] = 1
                            matrix1[row + 1][col + 1] = 1






                elif TowerSelection == 1 or 2 or 3 or 4:
                    if current_cell_value == 2:
                        x = col * 60
                        y = row * 60
                        pos = (x + 5, y + 5)
                        pos1 = (x,y)
                        rect = pygame.Rect((col * 60, row *60), (60,60))
                        screen.blit(pygame.image.load('selection.png').convert_alpha(),rect)
                        if mouse[0]:
                            if TowerSelection == 1 and Money >= 40:

                                towers.add(Towers.Tower1(pos))
                                matrix[row + 1][col + 1] = 3
                                Enemy.PlayerMoney -= 40
                            if TowerSelection == 2 and Money >= 100:
                                towers.add(Towers.Tower2(pos))
                                matrix[row + 1][col + 1] = 3
                                Enemy.PlayerMoney -= 100
                            if TowerSelection == 3 and Money >= 200:
                                towers.add(Towers.Tower3(pos))
                                matrix[row + 1][col + 1] = 3
                                Enemy.PlayerMoney -= 200
                            if TowerSelection == 4 and Money >= 500:
                                towers.add(Towers.Tower4(pos))
                                matrix[row + 1][col + 1] = 3
                                Enemy.PlayerMoney -= 500
                            else:
                                print("not enough money")



number = 0

def Enemyspawn(time):
    global collision_rects
    global number
    global spawn
    global lastspawn
    global Edit
    global Wave



    if (time - lastspawn >= 500):

        if (Wave - number) >= 0:
            print("spawning")

            pos = 30, 30
            enemies.add(Enemy.Enemy1(pos, collision_rects))
            number += 1
            lastspawn = pygame.time.get_ticks()



    elif Wave - number <= 0:
        number = 0
        spawn = False
        Wave += 1



#pygame.mixer.init()
#pygame.mixer.music.load("msi.wav")
#pygame.mixer.music.set_volume(1.0)
#pygame.mixer.music.play()

lastspawn = 0
collision_rects = []
Money = 0
Wave = 0
health = 0

#matrix for tower placement
matrix = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]

#matrix to find path
matrix1 = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]



Delaylast = 0

wave = False
Status = 'Normal'
spawn = False

def game_loop():
    global collision_rects
    global path
    global Wave
    global Towerselection
    global wave
    global Status
    global spawn
    global Money
    global TIME
    done = False
    score = 0
    lastwave = 0

    pygame.mixer.init()
    pygame.mixer.music.load("nonwave.wav")
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play()



    while not done:


        Money = Enemy.PlayerMoney
        health = Enemy.PlayerHealth
        if health <= 0:
            done = True
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        currentTime = pygame.time.get_ticks()
        TIME = (30000 - (currentTime - lastwave)) // 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        if wave == False:
            if currentTime - lastwave > 30000:
                wave = True
                spawn = True
                TIME = (30000 - (currentTime - lastwave)) // 1000

                pygame.mixer.music.stop()
                pygame.mixer.music.load("wave.wav")
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play()

            if keys[pygame.K_SPACE]:

                spawn = True
                wave = True
                pygame.mixer.music.stop()
                pygame.mixer.music.load("wave.wav")
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play()


        process_keys(keys)
        if wave == True:
            if spawn == False:
                if len(enemies) <= 0:
                    lastwave = pygame.time.get_ticks()
                    wave = False
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("nonwave.wav")
                    pygame.mixer.music.set_volume(1.0)
                    pygame.mixer.music.play()

            elif spawn == True:

                try:
                    collision_rects = Path.find_path(matrix1)
                    Enemyspawn(currentTime)



                except:
                    Status = "Cant find path!"
                    spawn = False
                    wave = False







        if move_entities(towers, enemies, clock.get_time() / 17) == True:
            return True
        screen.blit(bg, (0, 0))

        render_entities(towers, enemies)
        if wave == False:

            process_mouse(mouse, Towerselection)

        #Delete this later
        #Path.draw_path(matrix1, screen)
        screen.blit(ENEMY_SPAWN, (0, 0))
        screen.blit(BASE, (1140, 660))
        # weapon aim
        screen.blit(MANUAL_CURSOR, (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))

        # Health and score render
        for hp in range(health):
            screen.blit(healthRender, (800 + hp * 35, 0))

        MoneyRender = Font.render(("$ "+ str(Money)), True, pygame.Color('black'))
        MoneyRect = MoneyRender.get_rect()
        MoneyRect.right = size[0] - 20
        MoneyRect.top = 20
        screen.blit(MoneyRender, MoneyRect)

        WaveRender = Font.render(("Wave: " + str(Wave)), True, pygame.Color('black'))
        WaveRect = WaveRender.get_rect()
        WaveRect.right = size[0] - 20
        WaveRect.top = 60
        screen.blit(WaveRender, WaveRect)

        if Towerselection == 0:
            mode = "Walls"
        if Towerselection == 1:
            mode = "Tower 1"
        if Towerselection == 2:
            mode = "Tower 2"
        if Towerselection == 3:
            mode = "Tower 3"
        if Towerselection == 4:
            mode = "Tower 4"
        if Towerselection == 5:
            mode = "Delete"

        image1 = pygame.image.load("1ddark.png")
        image2 = pygame.image.load("2ddark.png")
        image3 = pygame.image.load("3ddark.png")
        image4 = pygame.image.load("4ddark.png")

        if Enemy.PlayerMoney >= 40:
            image1 = pygame.image.load("1dbright.png")

        if Enemy.PlayerMoney >= 100:
            image2 = pygame.image.load("2dbright.png")

        if Enemy.PlayerMoney >= 200:
            image3 = pygame.image.load("3dbright.png")

        if Enemy.PlayerMoney >= 500:
            image4 = pygame.image.load("4dbright.png")

        screen.blit(image1, (410, 10))
        screen.blit(image2, (510, 10))
        screen.blit(image3, (610, 10))
        screen.blit(image4, (710, 10))


        ModeRender = Font.render(("Mode: " + str(mode)), True, pygame.Color('black'))
        ModeRect = WaveRender.get_rect()
        ModeRect.right = size[0] - 120
        ModeRect.top = 100
        screen.blit(ModeRender, ModeRect)

        FPSRender = Font.render(("FPS: " + str(clock.get_fps() // 1)), True, pygame.Color('black'))
        FPSRect = WaveRender.get_rect()
        FPSRect.right = size[0] - 60
        FPSRect.top = 140
        screen.blit(FPSRender, FPSRect)

        if Status != 'Normal':
            StatusRender = Font.render((str(Status)), True, pygame.Color('red'))
            StatusRect = StatusRender.get_rect()
            StatusRect.centerx = size[0]/2
            StatusRect.centery = 200
            screen.blit(StatusRender, StatusRect)

        if wave == False:
            TimeRender = Font.render("Time Remaining: " +(str(TIME)) + " S", True, pygame.Color('black'))
            TimeRect = TimeRender.get_rect()
            TimeRect.centerx = size[0] / 2
            TimeRect.centery = 100
            screen.blit(TimeRender, TimeRect)


        if len(enemies) > 0:
            EnemyRender = Font.render("Enemy Remaining: " + (str(len(enemies))), True, pygame.Color('black'))
            EnemyRect = EnemyRender.get_rect()
            EnemyRect.centerx = size[0] / 2
            EnemyRect.centery = 100
            screen.blit(EnemyRender, EnemyRect)

        pygame.display.flip()
        clock.tick(60)



done = game_loop()
while not done:
    pygame.mixer.music.stop()
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    currentTime = pygame.time.get_ticks()
    screen.blit(pygame.image.load("died.png"), (0, 120))

    scoreRender = Font.render(str(score), True, pygame.Color('black'))
    scoreRect = scoreRender.get_rect()
    scoreRect.right = size[0] - 20
    scoreRect.top = 20
    screen.blit(scoreRender, scoreRect)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    if keys[pygame.K_r]:

        done = game_loop()

    clock.tick(30)
pygame.quit()
