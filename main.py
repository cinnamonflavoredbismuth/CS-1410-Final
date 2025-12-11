# CS T Rex Runner
from abc import ABC, abstractmethod
import pygame
from pygame import mixer
import random
from classes import *
pygame.init()
clock = pygame.time.Clock()

size=(598,149)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("T-Rex runner") 
pygame_icon = pygame.image.load('resources/light_neutral.png')

# 32 x 32 px image
pygame.display.set_icon(pygame_icon)



on_screen = Theme()
on_screen.runner.direction=None
running = True
speed=0
time=0
score=0000

font_color = (0, 0, 0)
dead=True




highScore=0



def start(on_screen):
    speed=5
    dead = False
    on_screen.runner.y=85
    on_screen.runner.hitbox_update()
    on_screen.enemies.pop(0)
    on_screen.enemies.append(random.choice(on_screen.enemy_options)(x=800,screenSpeed=speed))


    return speed, dead

def temp(on_screen):
    return None, False
def dead_restart(on_screen):
    return 0, True


while running:
    clock.tick(60)
    time+=1
    resrart=temp


    for event in pygame.event.get():
        keys = pygame.key.get_pressed()

        if event.type == pygame.QUIT: # Close the window
            running = False

        if event.type == pygame.KEYDOWN: # Key is pressed
            if keys[pygame.K_SPACE] or keys[pygame.K_UP] : # if space or up is pressed
                
                if speed == 0: #reset after death
                    resrart=start
                    on_screen.runner.direction='up'
                    on_screen.runner.jumping_sound()
                elif on_screen.runner.y==85:
                    on_screen.runner.direction='up'
                    on_screen.runner.jumping_sound()

                walking=on_screen.runner.jump_frame

            elif keys[pygame.K_DOWN] or keys[pygame.K_s]: # if down arrow is pressed
                
                walking=on_screen.runner.crouch

        else: walking=on_screen.runner.walk
        if pygame.mouse.get_pressed()[0] : # if mouse clicked
            if speed == 0: #reset after death
                    resrart=start
                    on_screen.runner.direction='up'
                    on_screen.runner.jumping_sound()
            elif on_screen.runner.y==85:
                    on_screen.runner.direction='up'
                    on_screen.runner.jumping_sound()

            walking=on_screen.runner.jump_frame
                    
    # collision detection

    if on_screen.collision_check()==1: # Death
        if dead == False:
            on_screen.runner.die()
        dead=True

    if dead == True:
        resrart=dead_restart if resrart != start else resrart

    # seperate frame rate dependent movement
        
    if on_screen.runner.y==85 and walking != on_screen.runner.crouch:
        walking=on_screen.runner.walk
        
    if speed != 0:
        on_screen.runner.jump()
        if (time//5-time/5)==0:
            walking()
            if (time//10-time/10)==0:
                for x in on_screen.enemies:
                    try:
                        x.fly()
                    except:pass
            score+=1
            speed+=0.1
        
       
    else:
        on_screen.runner.image=on_screen.runner.firstImage
        if score > highScore:
            highScore=score
        else:
            highScore=highScore
        score=0
        
    # show items
    resrart(on_screen)
    vars=resrart(on_screen)
    speed=vars[0] if vars[0]!=None else speed
    dead = vars[1]

    if walking == on_screen.runner.crouch:
            on_screen.runner.direction='crouch'

    on_screen.change_speed(speed)
    on_screen.show_all()

    if score//100==score/100 and score != 0 and not pygame.mixer.get_busy():
        pygame.mixer.Sound.play(pygame.mixer.Sound('resources/point.mp3'))

    
    screen.blit(pygame.font.Font('freesansbold.ttf', 14).render(f"HI: {str(highScore).zfill(5)} {str(score).zfill(5)}", True, font_color), (480, 10))

    if dead:
        screen.blit(pygame.font.Font('freesansbold.ttf', 20).render("Press Space/Up/W or Click to Start, and S/down to Crouch", True, font_color), (15, 70))
    # update screen
    pygame.display.flip()
    
