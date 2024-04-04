from pygame import *
from random import randint
font.init()

WIDTH,HEIGHT = 700, 525  
FPS = 60

lost = 0
points = 0

mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.0)
mixer.music.play()


window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Шутер")

class GameSprite(sprite.Sprite):
    def init(self,sprite_image, x, y, width, height):
        super().init()
        self.image = transform.scale(image.load(sprite_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = mask.from_surface(self.image)

    def draw(self):
        window.blit(self.image, self.rect)


class Player(GameSprite):
    def update(self):
        old_pos = self.rect.x, self.rect.y
        pressed = key.get_pressed()
        if pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= 3
        if pressed[K_RIGHT] and self.rect.x < WIDTH - 70:            
            self.rect.x += 3

    def fire(self):
        """Постріл кулею"""
        new_bullet = Bullet(self.rect.centerx, self.rect.y)
        bullets.add(new_bullet)


class Asteroid(GameSprite):
    def init(self, x, y, speed):
        super().init("asteroid.png", x, y, 60, 60)
        self.speed = speed

    def update(self):
        """рух астероїда"""
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.x = randint(0, WIDTH -80)
            self.rect.y = randint(-500, -150)
            self.speed = randint(3,4)

asteroids = sprite.Group()
for i in range(2):
    new = Asteroid(x=randint(0, WIDTH - 80),
                     y = randint(-500, -150),speed = randint(3,6))
    asteroids.add(new)



class Enemy(GameSprite):
    def init(self, x, y, speed):
        super().init("spaceship.png", x, y, 80, 60)
        self.speed = speed


    def update(self):
        """рух ворога"""
        global lost, lost_text
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            lost += 1
            lost_text = font1.render("Пропущено:" + str(lost), True,(255,255,255))
            self.rect.x = randint(0, WIDTH -80)
            self.rect.y = randint(-500, -150)
            self.speed = randint(3,6)


class Bullet(GameSprite):
    def init(self, x, y):
        super().init("bullet.png", x, y, 30,35)
        self.speed = 4

    def update(self):
        """рух кулі"""
        self.rect.y -= self.speed
        if self.rect.y < -30:
            self.kill()


player = Player("spaceship.png", x=WIDTH/2-50, y=HEIGHT-200, width =100, height =100)
bg = transform.scale(image.load("infinite_starts.jpg"), (WIDTH, HEIGHT))
bg2 = transform.scale(image.load("infinite_starts.jpg"), (WIDTH, HEIGHT))
bg_y1, bg_y2 = 0,-HEIGHT

bullets = sprite.Group()
monsters = sprite.Group()
for i in range(5):
    new_enemy = Enemy(x=randint(0, WIDTH - 80),
                     y = randint(-500, -150),speed = randint(3,6))
    monsters.add(new_enemy)

font1 = font.SysFont("Arial", 25)
lost_text = font1.render("Пропущено" + str(lost), True,(255,255,255))
points_text = font1.render("Рахунок" + str(points), True,(255,255,255))

font2 = font.SysFont("Arial", 50)
result_text = font2.render("БОТ!",True,(230, 145, 12))
restart_text = font2.render("РЕСТАРТ!",True,(230, 145, 12))
restart_btn = restart_text.get_rect()

run = True
finish = False
clock = time.Clock()

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()