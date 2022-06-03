import pygame
from pygame.locals import *
import random

pygame.init()

#fps
clock = pygame.time.Clock()
fps = 45

#window
width = 800
height = 400
window = pygame.display.set_mode((width,height))
pygame.display.set_caption('Knight')

#background
bg_img = pygame.image.load('img/Background.png').convert_alpha()
bg_img = pygame.transform.scale(bg_img,(width,height))
def bg():
    window.blit(bg_img, (0,0))

#both hero and bandit
class Warrior():
    def __init__(self, x, y, name, max_hp, strength):
        #mutual info
        self.x = x 
        self.y = y
        self.name = name 
        self.max_hp = max_hp 
        self.strength = strength
        self.dir = 0
        #hero image
        self.idle_img = [[], []]
        self.run_img = [[], []]
        self.jump_img = [[], []]
        self.fall_img = [[], []]
        self.attack_img = [[], []]
        self.death_img = [[], []]
        self.hurt_img = [[], []]
        #enemy image
        self.enemy_idle_img = [[], []]
        self.enemy_death_img = [[], []]
        self.enemy_run_img = [[], []]
        self.enemy_attack_img = [[], []]
        #hero image load
        if self.name == 'hero':
            for i in range(8): #Hero Idle
                img = pygame.image.load(f'img/{self.name}/Idle/HeroKnight_Idle_{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
                self.idle_img[0].append(img)
                img =  pygame.transform.flip(img, True, False)
                self.idle_img[1].append(img)            
            for i in range(10): #Hero Run
                img = pygame.image.load(f'img/{self.name}/Run/HeroKnight_Run_{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
                self.run_img[0].append(img)
                img = pygame.transform.flip(img, True, False)
                self.run_img[1].append(img)
            for i in range(8): #Hero Attack
                img = pygame.image.load(f'img/{self.name}/Attack/HeroKnight_Attack3_{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
                self.attack_img[0].append(img)
                img = pygame.transform.flip(img, True, False)
                self.attack_img[1].append(img)
            for i in range(10): #Hero Death
                img = pygame.image.load(f'img/{self.name}/Death/HeroKnight_Death_{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
                self.death_img[0].append(img)
                img = pygame.transform.flip(img, True, False)
                self.death_img[1].append(img)
            for i in range(3):
                img = pygame.image.load(f'img/{self.name}/Hurt/HeroKnight_Hurt_{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
                self.hurt_img[0].append(img)
                img = pygame.transform.flip(img, True, False)
                self.hurt_img[1].append(img)

            # for i in range(3): # Jump
            #     img = pygame.image.load(f'img/{self.name}/Jump/HeroKnight_Jump_{i}.png')
            #     img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
            #     self.jump_img[0].append(img)
            #     img = pygame.transform.flip(img, True, False)
            #     self.jump_img[1].append(img)
            self.rect = self.idle_img[0][0].get_rect() 
        #bandit image load
        else:
            for i in range(4): #Enemy Idle
                img = pygame.image.load(f'img/{self.name}/Combat Idle/LightBandit_Combat Idle_{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
                self.enemy_idle_img[0].append(img)
                img = pygame.transform.flip(img, True, False)
                self.enemy_idle_img[1].append(img)
            for i in range(8):
                img = pygame.image.load(f'img/{self.name}/Run/LightBandit_Run_{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
                self.enemy_run_img[0].append(img)
                img = pygame.transform.flip(img, True, False)
                self.enemy_run_img[1].append(img)
            for i in range(8):
                img = pygame.image.load(f'img/{self.name}/Attack/LightBandit_Attack_{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
                self.enemy_attack_img[0].append(img)
                img = pygame.transform.flip(img, True, False)
                self.enemy_attack_img[1].append(img)

            img = pygame.image.load(f'img/{self.name}/Death/LightBandit_Death_0.png')
            img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
            self.enemy_death_img[0].append(img)
            img = pygame.transform.flip(img, True, False)
            self.enemy_death_img[1].append(img)

            self.rect = self.enemy_idle_img[0][0].get_rect()

        self.rect.center = (x,y)
        #hero anime
        self.state = 0 # 0 for idle, 1 for run, 2 for jump...
        self.jumped = False
        self.jump_anime = 0 # 0~30
        self.idle_anime = 0 # 0~16
        self.run_anime = 0 # 0~20
        self.attack_anime = 0 # 0~16
        self.death_anime = 0 # 0~10
        self.hurt_anime = 0 # 0~6
        #enemy anime
        self.enemy_idle_anime = 0 # 0~8
        self.enemy_death_anime = 0 # 0~45
        self.enemy_run_anime = 0 #0~16
        self.enemy_attack_anime = 0 #0~16
        #velocity
        self.xvel = 0
        self.yvel = -15
        self.gameover = False
        
    def draw(self):
        #hero anime
        if self.name == 'hero':
            if self.state == 0: # idle
                window.blit(self.idle_img[self.dir][self.idle_anime//2], self.rect)
            elif self.state == 1: # run
                window.blit(self.run_img[self.dir][self.run_anime//2], self.rect)
            elif self.state == 2: # jump
                window.blit(self.jump_img[self.dir][self.jump_anime//10], self.rect)
            elif self.state == 3: # attack
                window.blit(self.attack_img[self.dir][self.attack_anime//2], self.rect)
            elif self.state == 4: # death
                window.blit(self.death_img[self.dir][self.death_anime//5], self.rect)
            elif self.state == 5: # hurt
                window.blit(self.hurt_img[self.dir][self.hurt_anime//11], self.rect)
        #enemy anime
        else:
            if self.state == 0: #enemy idle
                window.blit(self.enemy_idle_img[self.dir][self.enemy_idle_anime//2], self.rect)
            elif self.state == 1: #enemy run
                 window.blit(self.enemy_run_img[self.dir][self.enemy_run_anime//2], self.rect)
            elif self.state == 2 and self.enemy_death_anime < 45: #enemy death
                window.blit(self.enemy_death_img[self.dir][0], self.rect)
            elif self.state == 3:
                window.blit(self.enemy_attack_img[self.dir][self.enemy_attack_anime//2], self.rect)
        
    def update(self): #hero
        if self.max_hp > 0:
            self.rect.x += self.xvel
            # if self.jump_anime != 0 :
            #     self.rect.y += self.yvel #####
            if self.state == 0: # Idle
                self.idle_anime += 1
                self.idle_anime %= 16
            elif self.state == 1: # Run
                self.run_anime += 1
                self.run_anime %= 20
            # elif self.state == 2: # Jump 
            #     self.yvel += 1
            #     self.jump_anime += 1
            #     if self.yvel >= 15 and self.jump_anime >= 30:
            #         self.jump_anime = 0
            #         self.idle_anime = 0
            #         self.state = 0
            #         self.yvel = -15
            # 
                # if self.rect.bottom > height:
                #     self.rect.bottom = height
                    
            elif self.state == 3: # Attack
                self.attack_anime += 1
                if self.attack_anime == 16:
                    self.attack_anime = 0
                    self.idle_anime = 0
                    self.state = 0
            
            elif self.state == 5:
                self.hurt_anime +=1
                self.hurt_anime %=33
            
        elif self.state == 4 and self.gameover == False: #death
            self.death_anime +=1
            if self.death_anime == 49:
                self.gameover = True


    def enemy_update(self, _x):
        if self.state != 2 and self.max_hp > 0:
            self.rect.x += self.xvel
            if self.rect.x >_x + 100:
                self.xvel = -3
                self.state = 1
            elif self.rect.x < _x - 20:
                self.xvel = 3
                self.state = 1
            elif self.rect.x == _x + 100 or _x - 20:
                self.xvel = 0
                self.state = 0
                
            if self.state == 0: #idle
                self.enemy_idle_anime += 1
                self.enemy_idle_anime %= 8
            elif self.state == 1: #run
                self.enemy_run_anime += 1
                self.enemy_run_anime %= 16
            elif self.state == 3:
                self.enemy_attack_anime += 1
                self.enemy_attack_anime %= 16

            if self.rect.x > _x + 50: self.dir = 0
            else: self.dir =1
                
        elif self.state == 2:
          if self.enemy_death_anime < 45:
              self.enemy_death_anime += 1
            
    def draw_health(self):
        red = (255,0,0)
        green = (0,255,0)
        pygame.draw.rect(window,green,pygame.Rect(30, 30, self.max_hp*2, 15))
        pygame.draw.rect(window,red,pygame.Rect(30+ self.max_hp*2, 30, 100-self.max_hp*2 , 15))

def hero_atk_enemy(hero, enemy):
    if hero.state == 3 and enemy.state != 2:
        if hero.dir == enemy.dir:
            if  hero.rect.x > enemy.rect.x:
                if hero.rect.x -enemy.rect.x < 50:
                    enemy.max_hp -= hero.strength
            else:
                if enemy.rect.x - hero.rect.x < 125:
                    enemy.max_hp -= hero.strength
    if enemy.max_hp <= 0:
        enemy.state = 2

def enemy_atk_hero(hero, enemy):
    if k % 45 == 0:
        if hero.state != 4 and enemy.state != 2:
            if hero.dir != enemy.dir:
                if  hero.rect.x > enemy.rect.x:
                    if hero.rect.x -enemy.rect.x < 30:
                        hero.max_hp -= enemy.strength
                        hero.state = 5
                        enemy.state = 3
                else:
                    if enemy.rect.x - hero.rect.x < 150:
                        hero.max_hp -= enemy.strength
                        hero.state = 5
                        enemy.state = 3           
        if hero.max_hp <= 0:
            hero.state = 4
            
hero = Warrior(400, 305, 'hero', 50, 10) #strength * 5 = real strength
enemy_list = []
k = 0

running = True
while running:
    #fps
    clock.tick(fps)
    #background
    bg()
    #hero 
    hero.draw()
    if k % 90 == 0: # 45 means 45/45 second per spawn
        enemy = Warrior(random.choice([0,800]), 311, 'enemy', 50, 10)
        enemy_list.append(enemy)
    for enemys in enemy_list:
        enemys.draw()
        enemys.enemy_update(hero.rect.x)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            hero.state = 1
            hero.run_anime = 0
            if event.key == pygame.K_LEFT:
                hero.xvel = -5
                hero.dir = 1
            elif event.key == pygame.K_RIGHT:
                hero.xvel = 5
                hero.dir = 0
            elif event.key == pygame.K_UP:
                hero.state = 2
            elif event.key == pygame.K_SPACE:
                hero.state = 3
        elif event.type == pygame.KEYUP:
            hero.idle_anime = 0
            if hero.state == 1: 
                hero.state = 0
            hero.xvel = 0
    hero.update() 
    for enemys in enemy_list:          
        hero_atk_enemy(hero, enemys)
        enemy_atk_hero(hero, enemys)
    hero.draw_health()
    if hero.gameover == True:
        print('gameover')
        break
    k+=1
    pygame.display.update()         

pygame.quit()