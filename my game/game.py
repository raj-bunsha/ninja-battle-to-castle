import pygame
from pygame.locals import*
import os
import random
import math

class player(object):
    run = [pygame.image.load(os.path.join('images/png', "Run ("+str(x) + ').png')) for x in range(1,11)]
    jump = [pygame.image.load(os.path.join('images/png', "Jump ("+str(x) + ').png')) for x in range(1,11)]
    for x in range(0,10):
        run[x]=pygame.transform.scale(run[x],(100,100))
    for x in range(0,10):
        jump[x]=pygame.transform.scale(jump[x],(100,100))
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.sliding = False
        self.slideCount = 0
        self.jumpCount = 0
        self.runCount = 0
        self.slideUp = False
        self.time=0
        self.dead=False
        
    def draw(self, win):
        ori=self.y
        if self.jumping:
            if self.y < 250:
                self.time += 0.2   
                po = player.ninjumpPath(self.x,self.y, 10, math.pi/2,self.time)
                self.y = po
                win.blit(self.jump[int(self.time//2)], (self.x,self.y))
            else:
                self.jumping = False
                self.time = 0
                self.y = 240
        elif self.dead:
            dead=[pygame.transform.scale(pygame.image.load(os.path.join('images/png', "Dead (10).png")),(100,100))]
            win.blit(dead[0],(self.x,self.y))
            self.dead=True
        else:
            if self.runCount > 9:
                self.runCount = 0
            win.blit(self.run[self.runCount], (self.x,self.y))
            self.runCount += 1
        self.hitbox=(self.x+7,self.y+5,self.width+9,self.height+25)
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)

    @staticmethod
    def ninjumpPath(startx, starty, power, ang, time):
        angle = ang
        vely = math.sin(angle) * power
        distY = (vely * time) + ((-4.9 * (time ** 2)) / 2)
        newy = round(starty - distY)
        return (newy)
class crate(object):
    img=[pygame.image.load(os.path.join('images',"Crate.png"))]
    def __init__(self,x,y,width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.crate=(x,y, width, height)
    def draw(self, win):
        self.hitbox=(self.x,self.y,self.width,self.height)
        win.blit(self.img[0],(self.x,self.y))
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    def collide(self,rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
        return False

def redrawWin():
    win.blit(bg,(bgX,0))
    win.blit(bg,(bgX2,0))
    ninja.draw(win)
    for x in objectss:
        x.draw(win)
    #crates.draw(win)
    if ninja.dead==True:
        largeFont = pygame.font.SysFont('comicsans', 80)
        ended = largeFont.render('you are dead-> try again:-',1,(255,255,255))
        win.blit(ended, (W/2 - ended.get_width()/2,150))
    pygame.display.update()

def updateFile():
    f = open('scores.txt','r')
    file = f.readlines()
    last = int(file[0])

    if last < int(score):
        f.close()
        file = open('scores.txt', 'w')
        file.write(str(score))
        file.close()
        return score  
    return last

def over_window():
    global pause, score, speed, objectss
    pause = 0
    speed = 30
    objectss = []

    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                main()

        win.blit(bg, (0,0))
        largeFont = pygame.font.SysFont('comicsans', 80)
        lastScore = largeFont.render('Best Score: ' + str(updateFile()),1,(255,255,255))
        currentScore = largeFont.render('Score: '+ str(score),1,(255,255,255))
        win.blit(lastScore, (W/2 - lastScore.get_width()/2,150))
        win.blit(currentScore, (W/2 - currentScore.get_width()/2, 240))
        pygame.display.update()
    score = 0

def main():
    global W,H,win,bg,bgX,bgX2,clock,objectss,ninja,speed,score,bgs
    pygame.init()
    W,H = 800, 433
    win = pygame.display.set_mode((W,H))
    pygame.display.set_caption('ninja warrior attack to castle')
    bg = pygame.image.load(os.path.join('images','background.jpg')).convert()
    bgX = 0
    bgX2 = bg.get_width()
    clock = pygame.time.Clock()

    objectss=[]
    crates=crate(300,250,77,77)
    ninja=player(100,240,64,64)
    pygame.time.set_timer(USEREVENT+1, 500) # Sets the timer for 0.5 seconds
    pygame.time.set_timer(USEREVENT+2, random.randrange(2000,5000))
    Head=pygame.image.load(os.path.join('images/dragonbones/library','Head.png'))
    pygame.display.set_icon(Head)
    speed=20
    score=0
    pause=0
    fallSpeed=0
    run=True
    bgs=speed//2
    while run:
        score+=speed//10
        for obj in objectss:
            obj.x-=bgs
            if obj.collide(ninja.hitbox) or ninja.dead:
                ninja.dead=True
                speed=0
                bgs=0
                pause+=2
                if pause>=50:
                    over_window()

            if obj.x<obj.width*-1:
                objectss.pop(objectss.index(obj))

        if bgX < bg.get_width() * -1: 
            bgX = bg.get_width()
        
        if bgX2 < bg.get_width() * -1:
            bgX2 = bg.get_width()

        bgX-=bgs
        bgX2-=bgs
        for event in pygame.event.get():  
            if event.type == pygame.QUIT: 
                run = False
                pygame.quit()
                quit()
            if event.type==USEREVENT+1:
                speed+=0
            if event.type==USEREVENT+2:
                objectss.append(crate(810,250,77,77))
            keys=pygame.key.get_pressed()
            if keys[K_SPACE] or keys[K_UP]:
                if not(ninja.jumping) and not(ninja.dead):
                    ninja.jumping=True
        clock.tick(20)
        redrawWin()
main()
