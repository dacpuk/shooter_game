#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

lost = 0
score = 0
num_fire = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80,win_width - 80)
            lost = lost + 1
    def update2(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80,win_width - 80)

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80,win_width - 80)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()

font.init()
font1 = font.SysFont('Arial',36)

win_width = 700
win_height = 500 

asteroids = sprite.Group()
for i in range(3):
    asteroid = Asteroid('asteroid.png', randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster) 

ship = Player('rocket.png', 5, win_height - 100, 80, 100, 10)

window = display.set_mode((win_width,win_height))

background = transform.scale(image.load('galaxy.jpg'),(win_width,win_height))
clock = time.Clock()
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')

win = font1.render('ПОБЕДА',True,(255,255,255))
lose = font1.render('ПРОИГРЫШ',True,(255,255,255))

reload = False
FPS  = 40
finish = False
run = True
while run:
    for e  in event.get():
        if e.type == QUIT: 
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and reload == False:
                    ship.fire()
                    fire.play()
                    num_fire += 1
                if num_fire >= 5 and reload == False:
                    reload = True
                    last_time = timer()
    if finish != True:
        window.blit(background,(0,0)) 
        ship.update()
        ship.reset()
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)
        bullets.update()
        bullets.draw(window)
        if reload == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload_text = font1.render('Wait,reload',True,(150,0,0))
                window.blit(reload_text,(260,460))
            else:
                num_fire = 0
                reload = False
        sprite_list = sprite.groupcollide(monsters,bullets,True,True)
        for i in sprite_list:
            score += 1
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        if score >= 10:
            window.blit(win,(200,200))
            finish = True
        if lost >= 3 or sprite.spritecollide(ship,monsters, False) or sprite.spritecollide(ship,asteroids,False):
            window.blit(lose,(200,200))
            finish = True
        schet1 = font1.render('Счет:' + str(score),True,(255,255,255))
        schet2 = font1.render('Пропущено:' + str(lost) ,True,(255,255,255))
        window.blit(schet1,(10,20))
        window.blit(schet2,(10,50))
        display.update()
    time.delay(50)
