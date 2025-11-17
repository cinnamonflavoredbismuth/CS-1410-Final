# CS T Rex Runner

from abc import ABC, abstractmethod
import pygame
from pygame import mixer

pygame.init()
clock = pygame.time.Clocke()

background = pygame.image.load('tbd')
background = pygame.transform.scale(background, (800, 600))

# Score text
score_font = pygame.font.Font('tbd', 32)
font_color = (255, 255, 255)
font_location = (10, 10)

mixer.music.load('tbd')

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("T-Rex runner")
pygame_icon = pygame.image.load('tbd')

# 32 x 32 px image
pygame.display.set_icon(pygame_icon)


class Button:
    def __init__(self, x, y, img, scale=1):
        self.x = x
        self.y = y
        self.img = img
        width = img.get_width()
        height = img.get_height()
        self.img = pygame.transform.scale(img, (int(width * scale), int(height * scale)))
        self.scale = scale
        self.rect = self.img.get_rect(topleft=(self.x, self.y))
    def draw(self):
        pos = pygame.mouse.get_pos()
        print(pos)
        if self.rect.collidepoint(pos):
            print("Button hover")
            if pygame.mouse.get_pressed()[0] == 1:
                print("Button clicked")
                return True
        screen.blit(self.img, (self.x, self.y))

class OnScreen:
    def __init__(self,name,x,y,image,firstImage,secondaryImage,screenSpeed,speedModifier,rect):
        self.name=name
        self.x=x
        self.y=y
        self.image=image
        self.firstImage=firstImage
        self.secondaryImage=secondaryImage
        self.screenSpeed=screenSpeed
        self.speedModifier=speedModifier
        self.rect=rect

    def show(self):
        screen.blit(self.image,(self.x,self.y))
    
    def move(self):
        speed=self.screenSpeed*self.speedModifier
        self.x-=speed

    def colorChange(self):
        if self.image==self.firstImage:
            self.image=self.secondaryImage
        elif self.image == self.secondaryImage:
            self.image=self.firstImage

    def collisionCheck(self,other):
        return pygame.Rect.colliderect(self.rect,other.rect)
    

class PowerUp(OnScreen):
    def __init__(self, name, x, y, image, firstImage, secondaryImage, screenSpeed, speedModifier, rect):
        super().__init__(name, x, y, image, firstImage, secondaryImage, screenSpeed, speedModifier, rect)

class Runner(OnScreen):
    def __init__(self, name, x, y, image, firstImage, secondaryImage, screenSpeed, speedModifier, rect):
        super().__init__(name, x, y, image, firstImage, secondaryImage, screenSpeed, speedModifier, rect)

class Clouds(OnScreen):
    def __init__(self, name, x, y, image, firstImage, secondaryImage, screenSpeed, speedModifier, rect):
        super().__init__(name, x, y, image, firstImage, secondaryImage, screenSpeed, speedModifier, rect)

class Ground(OnScreen):
    def __init__(self, name, x, y, image, firstImage, secondaryImage, screenSpeed, speedModifier, rect):
        super().__init__(name, x, y, image, firstImage, secondaryImage, screenSpeed, speedModifier, rect)

class Background(OnScreen):
    def __init__(self, name, x, y, image, firstImage, secondaryImage, screenSpeed, speedModifier, rect):
        super().__init__(name, x, y, image, firstImage, secondaryImage, screenSpeed, speedModifier, rect)

class Cactus(OnScreen):
    def __init__(self, name, x, y, image, firstImage, secondaryImage, screenSpeed, speedModifier, rect):
        super().__init__(name, x, y, image, firstImage, secondaryImage, screenSpeed, speedModifier, rect)

class Theme:
    def __init__(self,cactus_options = [],power_up_options = [],runner = Runner(),clouds = Clouds(),ground = Ground(),background = Background(),power_up = PowerUp(),cactus=Cactus()):

        self.cactus_options=cactus_options
        self.power_up_options=power_up_options
        self.runner=runner
        self.clouds=clouds
        self.ground=ground
        self.background=background
        self.power_up=power_up
        self.cactus=cactus
        self.objects= [self.cactus_options,self.power_up_options,self.runner,self.clouds,self.ground,self.background,self.power_up,self.cactus]

    def change_speed(self,speed):
        for object in self.objects:
            object.screenSpeed = speed

    def theme_change(self):
        for object in self.objects:
            object.colorChange()

    def collision_check(self):

        if self.runner.collisionCheck(self.cactus):
            pass # make player death function
        elif self.runner.collisionCheck(self.power_up):
            self.runner.effect(self.power_up.effect) # update later. figure out how powerups are gonna work
            self.power_up.state=False
        else: return 0

    def show_all(self):
        for object in self.objects:
            if object == self.power_up:
                if object.state == True:
                    object.show()
                else: pass
            else:
                object.show()

        

running = True
speed=0
while running:
    clock.tick(30) # 30fps

   

    on_screen = Theme()

    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT: # Close the window
            running = False

        if event.type == pygame.KEYDOWN: # Key is pressed
            if keys[pygame.SPACE] or keys[pygame.K_UP]: # if space or up is pressed

                if speed == 0:
                    speed=30

            elif keys[pygame.K_DOWN]: # if down arrow is pressed
                pass #make the creature crouch

    # detect collision here

    # 

    
                

        

    