from pygame import *
mixer.init()
kick = mixer.Sound("kick.ogg")
gold = mixer.Sound("money.ogg")

WIDTH, HEIGHT = 700, 525

window = display.set_mode((WIDTH, HEIGHT) )
display.set_caption("treasure")

clock = time.Clock()

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_img, width, height, x, y):
        super().__init__()
        self.image = transform.scale(image.load(sprite_img), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 4

    def draw(self):
        window.blit(self.image, self.rect)


class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        old_pos = self.rect.x, self.rect.y
        if keys_pressed[K_a] and self.rect.x > 7:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < WIDTH - 40:
            self.rect.x += self.speed
        if keys_pressed[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys_pressed[K_s] and self.rect.y < HEIGHT - 40:
            self.rect.y += self.speed

        collides = sprite.spritecollide(self , walls , False)
        for collide in collides:
            self.rect.x, self.rect.y = old_pos
        

class Enemy(GameSprite):
    def __init__(self,sprite_img, width, height, x, y ):
        super().__init__(sprite_img, width, height, x, y)
        self.direction = "left"
    def update(self):
        collides = sprite.spritecollide(self , walls , False)
        for collide in collides:
            self.speed *= -1
        self.rect.x += self.speed
class Enemy2(GameSprite):
    def __init__(self,sprite_img, width, height, x, y ):
        super().__init__(sprite_img, width, height, x, y)
        self.direction = "left"
    def update(self):
        collides = sprite.spritecollide(self , walls , False)
        for collide in collides:
            self.speed *= -1
        self.rect.y += self.speed


class Wall(GameSprite):

    def __init__(self, x, y,):
        super().__init__("Wall.png", 35, 35, x, y)
    def draw(self):
        window.blit(self.image, self.rect)





player = Player("hero.png", width = 20, height = 20, x = WIDTH-200, y = HEIGHT-100)
golda = GameSprite("treasure.png", width = 45, height = 45, x = 40, y = HEIGHT-80)
bg = transform.scale(image.load("background.jpg"), (WIDTH, HEIGHT))

walls = sprite.Group()
enemy = sprite.Group()
money = sprite.Group()
finish_wall = sprite.Group()

with open("map.txt", "r") as file:
    map = file.readlines()
    x, y = 0, 0
    for line in map:
        for symbol in line:
            if symbol =="W":
                walls.add(Wall(x,y))

            if symbol == "P":
                player.rect.x = x
                player.rect.y = y
            if symbol =="E":
                enemy.add(Enemy("cyborg.png", width = 30, height = 30, x = x, y = y))
            if symbol =="S":
                enemy.add(Enemy2("cyborg.png", width = 30, height = 30, x = x, y = y))
            if symbol =="C":
                money.add(GameSprite("money.png", width = 15, height = 15, x = x+7, y = y+7))
            if symbol =="F":
                fwall = GameSprite("Finish_wall.png", width = 15, height = 105, x = x, y = y)
                finish_wall.add(fwall)
                walls.add(fwall)
            x += 35
        y+=35
        x = 0

                

step = 3
FPS = 60
font.init()
font1 = font.SysFont("Impact", 50)
win = font1.render("YOUR WINERS", True,(0,255,0))
lose = font1.render("YOUR LOZER", True,(255,0,0))
run = True
finish = False

score = 0
max_score = len(money)
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

    
    

    if not finish:
        player.update()
        enemy.update()
        window.blit(bg, (0, 0))
        golda.draw()
        enemy.draw(window)
        walls.draw(window)
        player.draw()
        money.draw(window)
        finish_wall.draw(window)
        collides = sprite.spritecollide(player, enemy, False)
        for collide in collides:
            finish = True
            kick.play()
            window.blit(lose,(300, 200))
            kick.play()
            window.blit(lose,(300, 200))
        collides = sprite.spritecollide(player, money, True)
        for collide in collides:
            score +=1
            if score == max_score:
                fwall.kill()

        if sprite.collide_rect(player, golda):
            finish = True
            gold.play()
            window.blit(win,(300, 200))
            kick.play()
        

            
    display.update()
    clock.tick(FPS)