# CS T Rex Runner

from abc import ABC, abstractmethod
import pygame
from pygame import mixer

pygame.init()
clock = pygame.time.Clocke()

size=(149,598)

background = pygame.image.load('resources/light_bg.png')
background = pygame.transform.scale(background, size)

# Score text
score_font = pygame.font.Font(None, 32)
font_color = (255, 255, 255)
font_location = (10, 10)


# Set up display 
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("T-Rex runner") 
pygame_icon = pygame.image.load('resources/light_neutral.png')

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
    def __init__(self, name, x, y, image, firstImage, secondaryImage, screenSpeed, speedModifier, rect, state, sound):
        super().__init__(name, x, y, image, firstImage, secondaryImage, screenSpeed, speedModifier, rect)
        self.state=state
        self.sound=sound

    @abstractmethod
    def effect(self,theme):
        pass

class Runner(OnScreen):
    def __init__(self, name='dino', x=598-16+64/2, y=598+24+64/2, image="resources/light_neutral.png", firstImage="resources/light_neutral.png", secondaryImage="resources/dark_neutral.png", screenSpeed=0, speedModifier=0, rect=None,jumpHeight=None,state=True,invincible=False):
        super().__init__(name, x, y, image, firstImage, secondaryImage, screenSpeed, speedModifier, rect)
        self.jumpHeight=jumpHeight
        self.state=state
        self.invincible=invincible
    def walk(self):
        pass #animation for walking
    def crouch(self):
        pass #animation for crouching
    def die(self):
        pass #animation for dying
    def jump(self):
        for x in self.jumpHeight:
            self.y+=0.3
        for x in self.jumpHeight:
            self.y-=0.3
    def invincibility_frames(self):
        pass #invincibility frames animation

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
        if not self.runner.invincible:
            if self.runner.collisionCheck(self.cactus):
                pass # make player death function
        elif self.runner.collisionCheck(self.power_up):
            self.power_up.effect(self) # update later. figure out how powerups are gonna work
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

    
                

        

    