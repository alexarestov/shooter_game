from pygame import *
from random import randint
from time import time as timer

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       super().__init__()
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
        if  keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if  keys[K_RIGHT] and self.rect.x <620:
            self.rect.x += self.speed
       
    def fire(self):
    
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_height - 80)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
    
#музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.2)
fire_sound = mixer.Sound('tankovyiy-vyistrel.ogg')
kill_sound = mixer.Sound('est-probitie.ogg')

#картинки
img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_enemy = 'ufo.png'
img_bullet = 'bullet.png'
img_asteroid = 'asteroid.png'

#надписи
font.init()
font1 = font.SysFont(None, 80)
win = font1.render('YOU WIN☠☠', True, (255, 255, 255))
lose = font1.render('YOU LOSE', True, (180,0,0))
font2 = font.SysFont(None, 36)

score = 0
lost = 0
max_lost = 5
life = 3


#окно
win_width = 700
win_height = 500
display.set_caption('pypsik')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

#спрайты
ship = Player(img_hero, 5, win_height -100, 80, 100, 10)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
    monsters.add(monster)

bullets = sprite.Group()

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy(img_asteroid, randint(30, win_width - 30), -40, 80, 50, randint(1,7))
    asteroids.add(asteroid)

run = True
finish = False

rel_time = False
num_fire = 0 

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 28927424924927537583479375734786347538945739453453487389753897823826583746345 and rel_time == False:
                    ship.fire()
                    fire_sound.play()
                    num_fire += 1
                if num_fire >= 28927424924927537583479375734786347538945739453453487389753897823826583746345 and rel_time == False:
                    last_time = timer()
                    rel_time = True
        
    if not finish:
        window.blit(background, (0,0))
        text = font2.render('Счет:  ' + str(score), 1, (255, 255, 255))
        window.blit(text, (10,20))
        text_lose = font2.render('Пропущено:  ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10,50))
        ship.update()
        monsters.update()
        bullets.update()
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)
        
        #перезарядка
        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 1:
                reload = font2.render('wait, reload...', 1, (150,0,0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life -= 1





        #столкловение пули и монстра
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            kill_sound.play()
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,7))
            monsters.add(monster)

        if life == 0 or lost >= 10:
            finish = True
            window.blit(lose, (200,200))


        #цвета жизни
        if life == 3:
            life_color = (0,150,0)
        if life == 2:
            life_color = (150,150,0)
        if life == 1:
            life_color = (150,0,0)
        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))
            


        #выигрыш
        if score >= 100:
            finish = True
            window.blit(win, (200,200)) 

        display.update()
    else:
        finish = False
        score = 0 
        lost = 0 
        life = 3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()
        
        time.delay(3000)
        for i in range(5):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,7))
            monsters.add(monster)
        for i in range(3):
            asteroid = Enemy(img_asteroid, randint(30, win_width - 30), -40, 80, 50, randint(1,7))
            asteroids.add(asteroid)
    time.delay(60)
