# CS T Rex Runner

from abc import ABC, abstractmethod
import pygame
from pygame import mixer

pygame.init()

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

class OnScreen:
    def __init__(self,name,x,y,image,firstImage,secondaryImage,screenSpeed,speedModifier):
        self.name=name
        self.x=x
        self.y=y
        self.image=image
        self.firstImage=firstImage
        self.secondaryImage=secondaryImage
        self.screenSpeed=screenSpeed
        self.speedModifier=speedModifier

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

