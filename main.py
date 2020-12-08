import os
import pygame as pg
import random

pg.font.init()
STAT_FONT = pg.font.SysFont("comicsans", 50)

SPRITE_IMG = pg.transform.scale2x(pg.image.load(os.path.join("assets", "bg-sprite.png")))
TREX_IMG = [pg.image.load(os.path.join("assets", "trex1.png")), pg.image.load(os.path.join("assets", "trex2.png")), pg.image.load(os.path.join("assets", "trex3.png"))]
CACTUS_IMG_SMALL = [pg.image.load(os.path.join("assets", "cactus1.png")), pg.image.load(os.path.join("assets", "cactus2.png")), pg.image.load(os.path.join("assets", "cactus3.png"))]
CACTUS_IMG_BIG = [pg.image.load(os.path.join("assets", "cactus4.png")), pg.image.load(os.path.join("assets", "cactus5.png"))]


class TRex:
    IMG = TREX_IMG
    ANIMATION_TIME = 10
    ACC = 1.001
    GRAVITY = 2

    def __init__(self):
        self.y = 280
        self.x = 50
        self.tick_count = 0
        self.vel = 0
        self.heigth = self.y

        self.img_count = 0
        self.img = self.IMG[0]
        self.animation_time = self.ANIMATION_TIME

    def jump(self):
        if self.y == 280:
            self.vel = -5.5
            self.tick_count = 0
        

    def move(self):
        self.tick_count += 1

        d = self.vel + 0.25*self.tick_count

        self.y = self.y + d

        if self.y >= 280:
           self.y = 280
    
    def draw(self, win):
        self.img_count += 1

        if self.y == 280:
            if self.img_count < self.animation_time:
                self.img = self.IMG[1]
            elif self.img_count < self.animation_time*2:
                self.img = self.IMG[2]
            elif self.img_count < self.animation_time*3:
                self.img = self.IMG[1]
                self.img_count = 0
        else:
            self.img = self.IMG[0]
            self.img_count = 0
          
        win.blit(self.img, (self.x, self.y))


class Base:
    VEL = 4
    ACC = 1.001
    WIDTH = SPRITE_IMG.get_width()
    
    def __init__(self):
        self.sprite = SPRITE_IMG
        self.x1 = 0
        self.x2 = self.WIDTH
        self.v = self.VEL
        print(self.x2)
        

    def move(self):
        #self.v *= self.ACC
        self.x1 -= self.v
        self.x2 -= self.v

        if self.x1 + self.WIDTH <= 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH <= 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.get_img(0, 102, self.WIDTH, 40), (self.x1, 300))
        win.blit(self.get_img(0, 102, self.WIDTH, 40), (self.x2, 300))

    def get_img(self, x, y, width, heigth):
        image = pg.Surface([width, heigth])

        image.blit(self.sprite, (0,0), (x, y, width, heigth))
        image.set_colorkey((0,0,0))
        return image

class Enemy:
    pass

class Cactus:
    IMG_SMALL = CACTUS_IMG_SMALL
    IMG_BIG = CACTUS_IMG_BIG
    VEL = 4
    ACC = 1.001

    def __init__(self):
        self.x1 = 0
        self.x2 = 0
        self.img_small = self.IMG_SMALL[0]
        self.img_big = self.IMG_BIG[0]
        self.passed = False
        self.v = self.VEL
        self.set_x()
        self.set_cactus()

    def set_x(self):
        self.x1 = random.randrange(501, 700)
        self.x2 = random.randrange(750, 1900)

    def set_cactus(self):
        pos = int(random.randrange(0, 2))
        self.img_small = self.IMG_SMALL[pos]
        self.img_big = self.IMG_BIG[pos]

    def move(self):
        #self.v *= self.ACC
        self.x1 -= self.v
        self.x2 -= self.v

    def collide(self):
        pass

    def draw(self, win):
        win.blit(self.img_small, (self.x1, 285))
        win.blit(self.img_big, (self.x2, 280))

def draw_window(win, base, trex, cactuses, score):
    base.draw(win)
    trex.draw(win)
    for cactus in cactuses:
        cactus.draw(win)

    score_txt = int(score)
    text = STAT_FONT.render("Score: "+str(score_txt),1,(0,0,0))
    win.blit(text, (500 - 10 - text.get_width(), 10))

    pg.display.update()

def main():
    win = pg.display.set_mode((500, 450))
    score = 0
    clock = pg.time.Clock()

    trex = TRex()
    base = Base()
    cactuses = [Cactus()]

    fps = 60
    
    run = True
    while run:
        if fps < 170:
            fps += 0.01
        clock.tick(fps)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                trex.jump()
        
        score += 0.05
        
        add_cactus = False
        for cactus in cactuses:
            if not cactus.passed and (cactus.x1 < trex.x or cactus.x2 < trex.x):
                add_cactus = True
                cactus.passed = True
            cactus.move()

        if add_cactus:
            cactuses.append(Cactus())

        trex.move()
        win.fill((255,255,255))
        base.move()
        draw_window(win, base, trex, cactuses, score)

main()