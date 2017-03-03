#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      THe Dark
#
# Created:     23/11/2015
# Copyright:   (c) THe Dark 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pygame as pg
import math
from math import atan2
from pygame.locals import *
import random

FPS = 50
WINDOW_SIZE = (1500,1000)
RED = pg.Color('red')
YELLOW = pg.Color('yellow')
BLUE = pg.Color ('blue')
BLACK = pg.Color ('black')
WHITE = pg.Color ('white')
GREY = pg.Color ('grey')
GREEN = pg.Color ('green')
ORANGE = pg.Color('orange')
PINK = pg.Color('pink')
PURPLE = pg.Color('purple')

#########################################
class Player(object):


    def __init__(self, x , y, size=50, color=WHITE, p=0, dmg=1, speed=4, angle=0, maxhp = 20, gun=1, tempForBullet=1, firerate=10, skill_cooldown=100):
        self.size = size
        self.x = x
        self.y = y
        self.color = color
        self.p = p
        self.dmg = dmg
        self.speed = speed
        self.angle = angle
        self.maxhp = maxhp
        self.hp = maxhp
        self.gun = gun
        self.tempForBullet = tempForBullet
        self.firerate = firerate
        self.invincible_timer=0
        self.shield =False
        self.skill_cooldown = skill_cooldown
        self.skill_timer = skill_cooldown
        self.ammo = 0

    def draw(self, display):
        pg.draw.rect(display, self.color, pg.Rect(
            self.x - self.size/2.0,
            self.y - self.size/2.0,
            self.size,
            self.size), 4)

    def moveangle(self, position):
        if position > 360:
            position-=360
        if position < 0:
            position+=360

        if (self.angle > position and self.angle - position < 180) or (self.angle < position and position - self.angle > 180):
            self.angle -=45
        elif self.angle - position !=0:
            self.angle +=45

        if self.angle > 360:
            self.angle-=360
        if self.angle < 0:
            self.angle+=360

    def get_hit_by(self, Enemy):
        return (self.x-self.size/2+5 < Enemy.x+Enemy.size/2 and self.x+self.size/2-5 > Enemy.x-Enemy.size/2) and (self.y-self.size/2+5 < Enemy.y+Enemy.size/2 and self.y+self.size/2-5 > Enemy.y-Enemy.size/2)

    def get_hit_by(self, Item):
        return (self.x-self.size/2+5 < Item.x+Item.size/2 and self.x+self.size/2-5 > Item.x-Item.size/2) and (self.y-self.size/2+5 < Item.y+Item.size/2 and self.y+self.size/2-5 > Item.y-Item.size/2)

    def get_hit_by(self, Enemy_Bullet):
        return (self.x-self.size/2+5 < Enemy_Bullet.x+Enemy_Bullet.size/2 and self.x+self.size/2-5 > Enemy_Bullet.x-Enemy_Bullet.size/2) and (self.y-self.size/2+5 < Enemy_Bullet.y+Enemy_Bullet.size/2 and self.y+self.size/2-5 > Enemy_Bullet.y-Enemy_Bullet.size/2)
#########################################
class Enemy(object):

    def __init__(self, x , y, size=50, color=RED, dmg=1, speed=2, angle=0, hp=1, score=100, enemy_type=0, skill_cooldown=1):
        self.size = size
        self.x = x
        self.y = y
        self.color = color
        self.dmg = dmg
        self.speed = speed
        self.angle = angle
        self.hp = hp
        self.score = score
        self.enemy_type = enemy_type
        self.skill_cooldown = skill_cooldown
        self.skill_timer = skill_cooldown
        self.get_hit = False

    def move_to(self, players):
        dx=WINDOW_SIZE[0]
        dy=WINDOW_SIZE[1]
        for player in players:
            if(math.sqrt(math.pow(player.x-self.x,2)+math.pow(player.y-self.y,2)) < math.sqrt(math.pow(dx,2)+math.pow(dy,2))):
                dx=player.x-self.x
                dy=player.y-self.y
        self.angle=atan2(dx,dy)*57.295
        self.x += math.sin(math.radians(self.angle)) * self.speed
        self.y += math.cos(math.radians(self.angle)) * self.speed

    def draw(self, display):
        pg.draw.rect(display, self.color, pg.Rect(
            self.x - self.size/2.0,
            self.y - self.size/2.0,
            self.size,
            self.size))

    def get_hit_by(self, Bullet):
        return (self.x-self.size/2 < Bullet.x+Bullet.size and self.x+self.size/2 > Bullet.x-Bullet.size) and (self.y-self.size/2 < Bullet.y+Bullet.size and self.y+self.size/2 > Bullet.y-Bullet.size)

#########################################
#Enemy Type
def walker(x,y):
    return Enemy(x, y, size=50, color=WHITE, dmg=2, speed=2, angle=0, hp=2, score=100, enemy_type=0)

def runner(x,y):
    return Enemy(x, y, size=40, color=ORANGE, dmg=2, speed=3.5, angle=0, hp=1, score=100, enemy_type=0)

def brute(x,y):
    return Enemy(x, y, size=100, color=BLUE, dmg=5, speed=1, angle=0, hp=20, score=200, enemy_type=0)

def mother(x,y):
    return Enemy(x, y, size=125, color=PINK, dmg=5, speed=0.5, angle=0, hp=30, score=300, enemy_type=1, skill_cooldown = 150)

def kid(x,y):
    return Enemy(x, y, size=40, color=PINK, dmg=1, speed=2, angle=0, hp=1, score=10, enemy_type=2)

def tresure(x,y):
    return Enemy(x, y, size=50, color=YELLOW, dmg=2, speed=2.5, angle=0, hp=2, score=300, enemy_type=3)

def soldier(x,y):
    return Enemy(x, y, size=50, color=RED, dmg=2, speed=2, angle=0, hp=2, score=200, enemy_type=4, skill_cooldown = 150)

def boomer(x,y):
    return Enemy(x, y, size=5, color=GREEN, dmg=2, speed=1, angle=0, hp=10, score=100, enemy_type=5, skill_cooldown = 10)

#########################################
class Item(object):
    def __init__(self, x , y, size=15, color=YELLOW, item_type=0, item_duration=1000):
        self.size = size
        self.x = x
        self.y = y
        self.color = color
        self.item_type = item_type
        self.item_duration = item_duration
        self.item_timer = 1

    def draw(self, display):
        pos=(int(self.x), int(self.y))
        pg.draw.circle(display, self.color, pos, self.size)
#########################################

def shotgun(x,y):
    return Item(x,y,color=RED,item_type=1)
def minigun(x,y):
    return Item(x,y,color=BLUE,item_type=2)
def regenaration(x,y):
    return Item(x,y,color=GREEN,item_type=3)
def shield(x,y):
    return Item(x,y,color=PURPLE,item_type=4)
def smg(x,y):
    return Item(x,y,color=YELLOW,item_type=5)

#########################################
class Bullet(object):

    def __init__(self, x , y, size=5, color=YELLOW, dmg=1, speed=10, angle=0):
        self.size = size
        self.x = x
        self.y = y
        self.color = color
        self.dmg = dmg
        self.speed = speed
        self.angle = angle

    def draw(self, display):
        pos=(int(self.x), int(self.y))
        pg.draw.circle(display, self.color, pos, self.size)

    def move(self):
        self.x += math.sin(math.radians(self.angle)) * self.speed
        self.y += math.cos(math.radians(self.angle)) * self.speed

#########################################
class Enemy_Bullet(object):

    def __init__(self, x , y, size=7, color=RED, dmg=1, speed=7, angle=0):
        self.size = size
        self.x = x
        self.y = y
        self.color = color
        self.dmg = dmg
        self.speed = speed
        self.angle = angle

    def draw(self, display):
        pos=(int(self.x), int(self.y))
        pg.draw.circle(display, self.color, pos, self.size)

    def move(self):
        self.x += math.sin(math.radians(self.angle)) * self.speed
        self.y += math.cos(math.radians(self.angle)) * self.speed



#########################################


def Retry():
    while True:
        for event in pg.event.get():
            if pg.key.get_pressed()[K_RIGHT] or (event.type == QUIT) or \
                    (event.type == KEYDOWN and event.key == K_ESCAPE):
                return False
            if pg.key.get_pressed()[K_LEFT]:
                return True

def playerOne():
    while True:
        for event in pg.event.get():
            if pg.key.get_pressed()[K_RIGHT]:
                return False
            if pg.key.get_pressed()[K_LEFT]:
                return True

#########################################

def render_score():
    '''Render score into an image for display'''
    global font,score,score_image
    score_image = font.render("Score = %d" % score, 0, GREY)

def render_hp(hp):
    '''Render hp into an image for display'''
    global font,hp_image
    hp_image = font.render("HP = %d" % hp, 0, WHITE)

def render_gameOver():
    '''Render game over into an image for display'''
    global font,gameOver_image1,gameOver_image2
    gameOver_image1 = font.render("GAME OVER! Try again?", 0, RED)
    gameOver_image2 = font.render("(YES press LEFT BOTTON , NO press RIGHT BOTTON)", 0, RED)

def render_start():
    global font,start_image1,start_image2
    start_image1 = font.render("How many Player?", 0, WHITE)
    start_image2 = font.render("(1 press LEFT BOTTON , 2 press RIGHT BOTTON)", 0, WHITE)

#########################################
def main():
    global game_over,font,score,score_image,hp_image,gameOver_image1,gameOver_image2,start_image1,start_image2

    pg.init()
    clock = pg.time.Clock()
    display = pg.display.set_mode(WINDOW_SIZE)
    pg.display.set_caption('GAME')
    game_over = False
    font = pg.font.SysFont("monospace", 20)
    score = 0
    score_image = None
    render_score()
    render_gameOver()
    render_start()
    start = False
    players = []
    p=0

    while not game_over:

        if players:
            for event in pg.event.get(): # process events
                if (event.type == QUIT) or \
                    (event.type == KEYDOWN and event.key == K_ESCAPE):
                    game_over = True


            display.fill(BLACK)  # clear screen
            display.blit(score_image, (10,10))  # draw score

            if(spawntimer%spawndelay==0):
                for player in players:
                    spawntimer=1
                    if spawndelay<1:
                        spawndelay-=1
                    random_spawnpoint = random.randint(0,3)
                    #create enemy at right
                    if(random_spawnpoint == 0):
                        rx=WINDOW_SIZE[0]+100
                        ry=random.randint(-100,WINDOW_SIZE[1]+100)
                    #create enemy at left
                    elif(random_spawnpoint == 1):
                        rx=-100
                        ry=random.randint(-100,WINDOW_SIZE[1]+100)
                    #create enemy at bottom
                    elif(random_spawnpoint == 2):
                        rx=random.randint(-100,WINDOW_SIZE[0]+100)
                        ry=WINDOW_SIZE[1]+100
                    #create enemy at top
                    else:
                        rx=random.randint(-100,WINDOW_SIZE[0]+100)
                        ry=-100

                    random_type = random.randint(0,12)
                    if(random_type <= 1):
                        enemy=brute(rx,ry)
                    elif(1 < random_type <= 3):
                        enemy=runner(rx,ry)
                    elif(3 < random_type <= 4):
                        enemy=mother(rx,ry)
                    elif(4 < random_type <= 6):
                        enemy=tresure(rx,ry)
                    elif(6 < random_type <= 8):
                        enemy=soldier(rx,ry)
                    elif(8 < random_type <= 9):
                        enemy=boomer(rx,ry)
                    else:
                        enemy=walker(rx,ry)
                    enemies.append(enemy)
            else:
                spawntimer+=1

            for player in players:
                if(player.tempForBullet%player.firerate==0):
                    bullet = Bullet(x=player.x, y=player.y, dmg=player.dmg, speed=player.speed+10, angle=player.angle)
                    bullets.append(bullet)
                    if player.gun >= 2:
                        bullet = Bullet(x=player.x, y=player.y, dmg=player.dmg, speed=player.speed+10, angle=player.angle+15)
                        bullets.append(bullet)
                    if player.gun >= 3:
                        bullet = Bullet(x=player.x, y=player.y, dmg=player.dmg, speed=player.speed+10, angle=player.angle-15)
                        bullets.append(bullet)
                    if player.gun >= 4:
                        bullet = Bullet(x=player.x, y=player.y, dmg=player.dmg, speed=player.speed+10, angle=player.angle+7.5)
                        bullets.append(bullet)
                    if player.gun >= 5:
                        bullet = Bullet(x=player.x, y=player.y, dmg=player.dmg, speed=player.speed+10, angle=player.angle-7.5)
                        bullets.append(bullet)
                    player.tempForBullet=1
                    if player.ammo > 0:
                        player.ammo -= 1
                else:
                    player.tempForBullet+=1
                if player.ammo<=0: #Base Pistol
                    player.dmg = 1
                    player.gun=1
                    player.firerate = 10

                if not player.invincible_timer > 0:
                    for enemy in enemies:
                        if player.get_hit_by(enemy):
                            player.invincible_timer = 50;
                            if not player.shield:
                                player.hp-=enemy.dmg
                            if enemy.enemy_type ==5 and enemy.score >= 350:
                                bulletangle=enemy.angle
                                while bulletangle < enemy.angle+360:
                                    bullet = Enemy_Bullet(x=enemy.x, y=enemy.y, angle=bulletangle)
                                    enemies_bullets.append(bullet)
                                    bulletangle += 15
                            else:
                                enemy.hp=0
                                player.shield=False
                            enemies.remove(enemy)

                    for bullet in enemies_bullets:
                        if player.get_hit_by(bullet):
                            player.invincible_timer = 50;
                            if not player.shield:
                                player.hp-=bullet.dmg
                                enemies_bullets.remove(bullet)
                            else:
                                enemies_bullets.remove(bullet)
                                player.shield=False
                else:
                    player.invincible_timer -= 1

                if player.shield:
                    pos=(int(player.x), int(player.y))
                    pg.draw.circle(display, PURPLE, pos, player.size, 2)

                for item in items:
                    if player.get_hit_by(item):
                        if item.item_type == 0:
                            score += 500
                        elif item.item_type == 1:
                            player.dmg = 5
                            player.gun = 5
                            player.firerate = 40
                            player.ammo = 30
                        elif item.item_type == 2:
                            player.dmg = 2
                            player.gun = 1
                            player.firerate = 3
                            player.ammo = 500
                        elif item.item_type == 3:
                            player.hp += 1
                            if player.hp > player.maxhp:
                                player.hp = player.maxhp
                        elif item.item_type == 4:
                            player.shield = True
                        elif item.item_type == 5:
                            player.dmg = 0.5
                            player.gun = 3
                            player.firerate = 6
                            player.ammo = 250
                        items.remove(item)

                if player.hp <= 0:
                    players.remove(player)

                render_hp(player.hp)
                display.blit(hp_image, (player.x-30,player.y+30))  # draw hp

                if player.p == 0:
                    if pg.key.get_pressed()[K_UP]:
                        if(player.y-player.speed>=0):
                            player.y-=player.speed
                    if pg.key.get_pressed()[K_DOWN]:
                        if(player.y+player.speed<=WINDOW_SIZE[1]):
                            player.y+=player.speed
                    if pg.key.get_pressed()[K_RIGHT]:
                        if(player.x+player.speed<=WINDOW_SIZE[0]):
                            player.x+=player.speed
                    if pg.key.get_pressed()[K_LEFT]:
                        if(player.x-player.speed>=0):
                            player.x-=player.speed

                    if pg.key.get_pressed()[K_UP] and pg.key.get_pressed()[K_RIGHT]:
                        player.moveangle(135)
                    elif pg.key.get_pressed()[K_UP] and pg.key.get_pressed()[K_LEFT]:
                        player.moveangle(225)
                    elif pg.key.get_pressed()[K_DOWN] and pg.key.get_pressed()[K_RIGHT]:
                        player.moveangle(45)
                    elif pg.key.get_pressed()[K_DOWN] and pg.key.get_pressed()[K_LEFT]:
                        player.moveangle(315)

                    elif pg.key.get_pressed()[K_UP]:
                        player.moveangle(180)
                    elif pg.key.get_pressed()[K_DOWN]:
                        player.moveangle(360)
                    elif pg.key.get_pressed()[K_RIGHT]:
                        player.moveangle(90)
                    elif pg.key.get_pressed()[K_LEFT]:
                        player.moveangle(270)

                    if player.skill_cooldown == player.skill_timer:
                        if pg.key.get_pressed()[K_m]:
                            if player.x+math.sin(math.radians(player.angle)) * 300 <= 0:
                                player.x = 10
                            elif player.x+math.sin(math.radians(player.angle)) * 300 >=WINDOW_SIZE[0]:
                                player.x = WINDOW_SIZE[0] - 10
                            else:
                                player.x += math.sin(math.radians(player.angle)) * 300
                            if player.y+math.cos(math.radians(player.angle)) * 300 <= 0:
                                player.y = 10
                            elif player.y+math.cos(math.radians(player.angle)) * 300 >=WINDOW_SIZE[1]:
                                player.y = WINDOW_SIZE[1] - 10
                            else:
                                player.y += math.cos(math.radians(player.angle)) * 300

                            #Extra backfire
                            player.angle += 180
                            bullet = Bullet(x=player.x, y=player.y, dmg=player.dmg, speed=player.speed+10, angle=player.angle)
                            bullets.append(bullet)
                            if player.gun >= 2:
                                bullet = Bullet(x=player.x, y=player.y, dmg=player.dmg, speed=player.speed+10, angle=player.angle+15)
                                bullets.append(bullet)
                            if player.gun >= 3:
                                bullet = Bullet(x=player.x, y=player.y, dmg=player.dmg, speed=player.speed+10, angle=player.angle-15)
                                bullets.append(bullet)
                            if player.gun >= 4:
                                bullet = Bullet(x=player.x, y=player.y, dmg=player.dmg, speed=player.speed+10, angle=player.angle+7.5)
                                bullets.append(bullet)
                            if player.gun >= 5:
                                bullet = Bullet(x=player.x, y=player.y, dmg=player.dmg, speed=player.speed+10, angle=player.angle-7.5)
                                bullets.append(bullet)
                            if player.ammo > 0:
                                player.ammo -= 1
                            player.tempForBullet=1

                            player.skill_timer = 1
                    else:
                        player.skill_timer += 1

                if player.p == 1:
                    if pg.key.get_pressed()[K_w]:
                        if(player.y-player.speed>=0):
                            player.y-=player.speed
                    if pg.key.get_pressed()[K_s]:
                        if(player.y+player.speed<=WINDOW_SIZE[1]):
                            player.y+=player.speed
                    if pg.key.get_pressed()[K_d]:
                        if(player.x+player.speed<=WINDOW_SIZE[0]):
                            player.x+=player.speed
                    if pg.key.get_pressed()[K_a]:
                        if(player.x-player.speed>=0):
                            player.x-=player.speed


                    if pg.key.get_pressed()[K_w] and pg.key.get_pressed()[K_d]:
                        player.moveangle(135)
                    elif pg.key.get_pressed()[K_w] and pg.key.get_pressed()[K_a]:
                        player.moveangle(225)
                    elif pg.key.get_pressed()[K_s] and pg.key.get_pressed()[K_d]:
                        player.moveangle(45)
                    elif pg.key.get_pressed()[K_s] and pg.key.get_pressed()[K_a]:
                        player.moveangle(315)

                    elif pg.key.get_pressed()[K_w]:
                        player.moveangle(180)
                    elif pg.key.get_pressed()[K_s]:
                        player.moveangle(360)
                    elif pg.key.get_pressed()[K_d]:
                        player.moveangle(90)
                    elif pg.key.get_pressed()[K_a]:
                        player.moveangle(270)

                    if player.skill_cooldown == player.skill_timer:
                        if pg.key.get_pressed()[K_SPACE]:
                            if player.x+math.sin(math.radians(player.angle)) * 300 <= 0:
                                player.x = 10
                            elif player.x+math.sin(math.radians(player.angle)) * 300 >=WINDOW_SIZE[0]:
                                player.x = WINDOW_SIZE[0] - 10
                            else:
                                player.x += math.sin(math.radians(player.angle)) * 300
                            if player.y+math.cos(math.radians(player.angle)) * 300 <= 0:
                                player.y = 10
                            elif player.y+math.cos(math.radians(player.angle)) * 300 >=WINDOW_SIZE[1]:
                                player.y = WINDOW_SIZE[1] - 10
                            else:
                                player.y += math.cos(math.radians(player.angle)) * 300

                            #Extra backfire
                            player.angle += 180
                            bullet = Bullet(x=player.x, y=player.y, dmg=player.dmg, speed=player.speed+10, angle=player.angle)
                            bullets.append(bullet)
                            if player.gun >= 2:
                                bullet = Bullet(x=player.x, y=player.y, dmg=player.dmg, speed=player.speed+10, angle=player.angle+15)
                                bullets.append(bullet)
                            if player.gun >= 3:
                                bullet = Bullet(x=player.x, y=player.y, dmg=player.dmg, speed=player.speed+10, angle=player.angle-15)
                                bullets.append(bullet)
                            if player.gun >= 4:
                                bullet = Bullet(x=player.x, y=player.y, dmg=player.dmg, speed=player.speed+10, angle=player.angle+7.5)
                                bullets.append(bullet)
                            if player.gun >= 5:
                                bullet = Bullet(x=player.x, y=player.y, dmg=player.dmg, speed=player.speed+10, angle=player.angle-7.5)
                                bullets.append(bullet)
                            if player.ammo > 0:
                                player.ammo -= 1
                            player.tempForBullet=1

                            player.skill_timer = 1
                    else:
                        player.skill_timer += 1

                if player.invincible_timer%2 == 0 : #make player blink when invincible
                    player.draw(display)  # draw player

            for bullet in bullets:
                if bullet.y < -10 or bullet.y > WINDOW_SIZE[1]+10 or bullet.x < -10 or bullet.x > WINDOW_SIZE[0]+10:
                    bullets.remove(bullet)
                bullet.move()
                bullet.draw(display)

            for bullet in enemies_bullets:
                if bullet.y < -10 or bullet.y > WINDOW_SIZE[1]+10 or bullet.x < -10 or bullet.x > WINDOW_SIZE[0]+10:
                    enemies_bullets.remove(bullet)
                bullet.move()
                bullet.draw(display)


            for enemy in enemies:
                enemy.get_hit = False
                for bullet in bullets:
                    if enemy.get_hit_by(bullet):
                        enemy.hp-=bullet.dmg
                        bullets.remove(bullet)
                        enemy.get_hit=True
                if enemy.hp <= 0:
                    score+=enemy.score
                    render_score()
                    if enemy.enemy_type == 1:
                        enemies.append(kid(enemy.x, enemy.y+30))
                        enemies.append(kid(enemy.x-30, enemy.y-30))
                        enemies.append(kid(enemy.x+30, enemy.y-30))
                        kids += 3
                    if enemy.enemy_type == 2:
                        kids -= 1
                    enemies.remove(enemy)
                    if enemy.enemy_type == 3 or ((not enemy.enemy_type == 2 ) and random.randint(0,9) == 1):
                        random_type = random.randint(0,4)
                        if(random_type == 0):
                            items.append(shotgun(enemy.x,enemy.y))
                        elif(random_type == 1):
                            items.append(minigun(enemy.x,enemy.y))
                        elif(random_type == 2):
                            items.append(regenaration(enemy.x,enemy.y))
                        elif(random_type == 3):
                            items.append(shield(enemy.x,enemy.y))
                        elif(random_type == 4):
                            items.append(smg(enemy.x,enemy.y))

                if kids <=10:
                    if enemy.enemy_type == 1:
                        if enemy.skill_timer%enemy.skill_cooldown == 0 :
                            enemies.append(kid(enemy.x, enemy.y))
                            kids += 1
                            enemy.skill_timer=1
                        else:
                            enemy.skill_timer+=1

                if enemy.enemy_type ==4:
                    if enemy.skill_timer%enemy.skill_cooldown == 0 :
                        bullet = Enemy_Bullet(x=enemy.x, y=enemy.y, angle=enemy.angle)
                        enemies_bullets.append(bullet)
                        enemy.skill_timer=1
                    else:
                        enemy.skill_timer+=1

                if enemy.enemy_type ==5:
                    if enemy.skill_timer%enemy.skill_cooldown == 0 :

                        enemy.size += 5
                        enemy.score += 10
                        if enemy.speed <= 4:
                            enemy.speed += 0.1
                        enemy.skill_timer=1

                        if enemy.score >= 500:
                            bulletangle=enemy.angle
                            while bulletangle < enemy.angle+360:
                                bullet = Enemy_Bullet(x=enemy.x, y=enemy.y, angle=bulletangle)
                                enemies_bullets.append(bullet)
                                bulletangle += 15
                            enemies.remove(enemy)
                    else:
                        enemy.skill_timer+=1
                        if enemy.score >=350:
                            enemy.dmg = 5;
                            if enemy.skill_timer%2==0:
                                enemy.get_hit=True

                if not enemy.get_hit: #make enemy blink when damaged
                    enemy.draw(display)
                enemy.move_to(players)

            for item in items:
                if item.item_timer%item.item_duration == 0:
                    items.remove(item)
                else:
                    item.item_timer += 1
                if item.item_timer%2 == 0 or not item.item_timer >=750:
                    item.draw(display)

            pg.display.update()  # redraw the screen
            clock.tick(FPS)  # wait to limit FPS requirement

        else:
            if not start:
                display.blit(start_image1, (WINDOW_SIZE[0]/2-100,WINDOW_SIZE[1]/2))
                display.blit(start_image2, (WINDOW_SIZE[0]/2-200,WINDOW_SIZE[1]/2+50))
                pg.display.update()  # redraw the screen
                clock.tick(FPS)  # wait to limit FPS requirement
                if playerOne():
                    p=1
                else:
                    p=2

                start = True
                enemies = []
                bullets = []
                enemies_bullets = []
                items = []
                kids = 0 #count kid for capped
                score = 0
                render_score()
                spawntimer=0
                spawndelay=100
                if p >= 1:
                    players.append(Player(color=BLUE,p=0,y=WINDOW_SIZE[1]/2 ,x=WINDOW_SIZE[0]/2))
                if p >= 2:
                    players.append(Player(color=RED,p=1,y=WINDOW_SIZE[1]/2 ,x=WINDOW_SIZE[0]/2))
            else:
                p=0
                display.blit(gameOver_image1, (WINDOW_SIZE[0]/2-100,WINDOW_SIZE[1]/2))  # draw gameOver ask player try to play?
                display.blit(gameOver_image2, (WINDOW_SIZE[0]/2-200,WINDOW_SIZE[1]/2+50))  # draw gameOver ask player try to play?
                pg.display.update()  # redraw the screen
                clock.tick(FPS)  # wait to limit FPS requirement
                if not Retry():
                    game_over = True
                else:
                    display.fill(BLACK)  # clear screen
                    start = False


#########################################
if __name__=='__main__':
    main()
    print "Game Over!"
    pg.quit()