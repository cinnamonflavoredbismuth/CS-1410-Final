# CS T Rex Runner

from abc import ABC, abstractmethod
import pygame
from pygame import mixer
import random

pygame.init()
clock = pygame.time.Clock()

size=(598,149)


# Score text



# Set up display 
screen = pygame.display.set_mode(size)
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
    def __init__(self,name='basic class',x=0,y=0,image='resources/light_neutral.png',firstImage='resources/light_neutral.png',secondaryImage='resources/light_neutral.png',screenSpeed=0,speedModifier=0,rect=None,scale=1):
        self.name=name
        self.x=x
        self.y=y
        self.img=pygame.image.load(image)
        width = self.img.get_width()
        height = self.img.get_height()
        
        self.image=pygame.transform.scale(self.img, (int(width * scale), int(height * scale)))

        self.firstImage=pygame.image.load(firstImage)
        self.secondaryImage=pygame.image.load(secondaryImage)
        self.screenSpeed=screenSpeed
        self.speedModifier=speedModifier
        self.rect=rect
        try:
            if type(self.rect[0])==list:
                self.hitbox=[]
                for i in range(len(self.rect)):
                    self.hitbox.append(pygame.rect.Rect(self.x+self.rect[i][0],self.y+self.rect[i][1],self.rect[i][2],self.rect[i][3]))
            else:
                self.hitbox=pygame.rect.Rect(self.x+self.rect[0],self.y+self.rect[1],self.rect[2],self.rect[3])
        except:
            self.hitbox=self.image.get_rect() #temporary
     
            
    def hitbox_update(self): #adjust hitbox position to account for movement
        # hitbox key: [x offset, y offset, width, height]
        try:
            if type(self.hitbox)==list:
                for i in range(len(self.hitbox)):
                    self.hitbox[i]=pygame.rect.Rect(self.x+self.rect[i][0],self.y+self.rect[i][1],self.rect[i][2],self.rect[i][3])
            else:
                self.hitbox=pygame.rect.Rect(self.x+self.rect[0],self.y+self.rect[1],self.rect[2],self.rect[3])
        except:
            self.hitbox=self.image.get_rect() #temporary
            self.hitbox.topleft=(self.x,self.y)

    def move(self):
        nums=[]
        num = 0
        if type(self.hitbox) == list: 
            for box in self.hitbox:
                nums.append(box[2])
            for n in nums:
                if n>num:
                    num=n

        else: num=self.hitbox[2]
        
        if self.x>=(0-num):
            speed=self.screenSpeed*self.speedModifier
            self.x-=speed
            self.hitbox_update()
        else: self.x=600
           
    def show(self):
        self.move()
        screen.blit(self.image,(self.x,self.y))
        
    def hitbox_draw(self,color=(255,0,0)): 
        if type(self.hitbox)==list:
            for box in self.hitbox:
                pygame.draw.rect(screen, color, box, 2) #debugging rect
        else:
            pygame.draw.rect(screen, color, self.hitbox, 2) #debugging rect

    def colorChange(self):
        if self.image==self.firstImage:
            self.image=self.secondaryImage
        elif self.image == self.secondaryImage:
            self.image=self.firstImage

    def collisionCheck(self,other):
        if type(self.hitbox)==list and type(other.hitbox)==list:
            for box1 in self.hitbox:
                for box2 in other.hitbox:
                    if pygame.Rect.colliderect(box1,box2):
                        return True
                        
        elif type(self.hitbox)==list:
            for box in self.hitbox:
                if pygame.Rect.colliderect(box,other.hitbox):
                    return True
                    
        elif type(other.hitbox)==list:
            for box in other.hitbox:
                if pygame.Rect.colliderect(self.hitbox,box):
                    return True
                    
        else:
            return pygame.Rect.colliderect(self.hitbox,other.hitbox)
    

# POWERUPS


class PowerUp(OnScreen):
    def __init__(self, name="powerup", x=100, y=20, image='resources/light_neutral.png', firstImage='resources/light_neutral.png', secondaryImage='resources/light_neutral.png', screenSpeed=0, speedModifier=1, rect=None, state=False, sound=None,scale=1):
        super().__init__(name, x, y, image, firstImage, secondaryImage, screenSpeed, speedModifier, rect,scale)
        self.state=state
        self.sound=sound

    @abstractmethod
    def effect(self,theme):
        pass

class Runner(OnScreen):
    def __init__(self, name='dino', x=0, y=85, image="resources/light_neutral.png", firstImage="resources/light_neutral.png", secondaryImage="resources/dark_neutral.png", frame1='resources/light_right.png',frame2='resources/light_left.png',crouch1='resources/light_crouch_right.png',crouch2='resources/light_crouch_left.png',screenSpeed=0, speedModifier=0, rect=[[12,11,20,42],[12,11,41,20]],jumpHeight=155,state=True,invincible=False,scale=1,direction='up',):
        super().__init__(name, x, y, image, firstImage, secondaryImage, screenSpeed, speedModifier, rect,scale)
        self.jumpHeight=jumpHeight
        self.state=state
        self.invincible=invincible
        self.direction=direction
        self.frame1=pygame.image.load(frame1)
        self.frame2=pygame.image.load(frame2)
        self.crouch1=pygame.image.load(crouch1)
        self.crouch2=pygame.image.load(crouch2)
    def jump_frame(self):
        self.image=self.firstImage
    def walk(self):
        if self.image==self.frame1 and self.y==85.0:
            self.image=self.frame2
        else:
            if self.y!=85.0:
                self.image=self.firstImage
            else: self.image=self.frame1
    def crouch(self):
        if self.image==self.crouch1 and self.y==85.0:
            self.image=self.crouch2
        else:
            if self.y!=85.0:
                self.image=self.firstImage
            else: self.image=self.crouch1
    def die(self):
        pass # death animation
        return True
    def jump_down(self):
        if self.y<85 and self.direction=='down':
            self.y+=4.5
            self.hitbox_update()
            self.direction='down'
        else: 
            self.direction=None
    def jump_up(self):
        if self.y>(149-self.jumpHeight) and self.direction=='up':
            self.y-=4.5
            self.hitbox_update()
            self.direction='up'
        else: 
            self.direction='down'
            self.jump_down()

    def jump(self):
        self.jump_up()
        

    def invincibility_frames(self):
        pass #invincibility frames animation

class Clouds(OnScreen):
    def __init__(self, name='cloud', x=600, y=0, image='resources/light_clouds.png', firstImage='resources/light_clouds.png', secondaryImage='resources/dark_moon.png', screenSpeed=0, speedModifier=0.2, rect=None,scale=1):
        super().__init__(name, x, y, image, firstImage, secondaryImage, screenSpeed, speedModifier, rect,scale)

class Ground(OnScreen):
    def __init__(self, name='ground', x=0, y=121, image='resources/light_ground.png', firstImage='resources/light_ground.png', secondaryImage='resources/dark_ground.png', screenSpeed=0, speedModifier=1, rect=None,scale=1):
        super().__init__(name, x, y, image, firstImage, secondaryImage, screenSpeed, speedModifier, rect,scale)

class Background(OnScreen):
    def __init__(self, name='background', x=0, y=0, image='resources/light_bg.png', firstImage='resources/light_bg.png', secondaryImage='resources/dark_bg.png', screenSpeed=0, speedModifier=0, rect=None,scale=1):
        super().__init__(name, x, y, image, firstImage, secondaryImage, screenSpeed, speedModifier, rect,scale)
        

# CACTI 


class Cactus(OnScreen):
    def __init__(self, name='cactus', x=800, y=0, image='resources/light_cactus_big_single.png', firstImage='resources/light_cactus_big_single.png', secondaryImage='resources/dark_cactus_big_single.png', screenSpeed=0, speedModifier=1,
                  rect=[26,90,25,50],scale=1):
        super().__init__(name, x, y, image, firstImage, secondaryImage, screenSpeed, speedModifier, rect,scale)

class CactusSmallSingle(Cactus):
    def __init__(self, name='cactus_small_single', x=800, y=0, image='resources/light_cactus_small_single.png', firstImage='resources/light_cactus_small_single.png', secondaryImage='resources/dark_cactus_big_single.png', screenSpeed=0, speedModifier=1,
                  rect=[31,105,18,40],scale=1):
        super().__init__(name, x, y, image, firstImage, secondaryImage, screenSpeed, speedModifier, rect,scale)

class CactusSmallDuo(Cactus):
    def __init__(self, name='cactus_small_duo', x=800, y=0, image='resources/light_cactus_small_duo.png', firstImage='resources/light_cactus_small_duo.png', secondaryImage='resources/dark_cactus_small_duo.png', screenSpeed=0, speedModifier=1,
                  rect=[21,105,35,37],scale=1):
        super().__init__(name, x, y, image, firstImage, secondaryImage, screenSpeed, speedModifier, rect,scale)

class CactusSmallTriad(Cactus):
    def __init__(self, name='cactus_small_triad', x=800, y=0, image='resources/light_cactus_small_triad.png', firstImage='resources/light_cactus_small_triad.png', secondaryImage='resources/dark_cactus_small_triad.png', screenSpeed=0, speedModifier=1,
                  rect=[11,105,50,35],scale=1):
        super().__init__(name, x, y, image, firstImage, secondaryImage, screenSpeed, speedModifier, rect,scale)

class CactusBigSingle(Cactus):
    def __init__(self, name='cactus_big_single', x=800, y=0, image='resources/light_cactus_big_single.png', firstImage='resources/light_cactus_big_single.png', secondaryImage='resources/dark_cactus_big_single.png', screenSpeed=0, speedModifier=1,
                  rect=[26,90,25,50],scale=1):
        super().__init__(name, x, y, image, firstImage, secondaryImage, screenSpeed, speedModifier, rect,scale)

class CactusQuartet(Cactus):
    def __init__(self, name='cactus_quartet', x=800, y=0, image='resources/light_cactus_quartet.png', firstImage='resources/light_cactus_quartet.png', secondaryImage='resources/dark_cactus_quartet.png', screenSpeed=0, speedModifier=1,
                  rect=[3,90,75,50],scale=1):
        super().__init__(name, x, y, image, firstImage, secondaryImage, screenSpeed, speedModifier, rect,scale)


# BIRDS



class Bird(OnScreen):
    def __init__(self, name='bird', x=0, y=0, image='resources/light_bird_middle_down.png', firstImage='resources/light_bird_middle_down.png', secondaryImage='resources/dark_bird_middle_down.png', screenSpeed=0, speedModifier=0, rect=None, scale=1,frame1='resources/light_bird_middle_down.png',frame2='resources/light_bird_middle_up.png'):
        super().__init__(name, x, y, image, firstImage, secondaryImage, screenSpeed, speedModifier, rect, scale)
        self.frame1=pygame.image.load(frame1)
        self.frame2=pygame.image.load(frame2)

    def fly(self):
        if self.image==self.frame1 and self.y==85.0:
            self.image=self.frame2
        else:
            self.image=self.frame1

class BirdHigh(Bird):
    def __init__(self, name='bird', x=0, y=0, image='resources/light_bird_high_down.png', firstImage='resources/light_bird_high_down.png', secondaryImage='resources/light_bird_high_down.png', screenSpeed=0, speedModifier=0, rect=[10,55,42,33], scale=1, frame1='resources/light_bird_high_down.png', frame2='resources/dark_bird_high_up.png'):
        super().__init__(name, x, y, image, firstImage, secondaryImage, screenSpeed, speedModifier, rect, scale, frame1, frame2)

class BirdMiddle(Bird):
    def __init__(self, name='bird', x=0, y=0, image='resources/light_bird_middle_down.png', firstImage='resources/light_bird_middle_down.png', secondaryImage='resources/dark_bird_middle_down.png', screenSpeed=0, speedModifier=0, rect=[10,80,42,33], scale=1, frame1='resources/light_bird_middle_down.png', frame2='resources/light_bird_middle_up.png'):
        super().__init__(name, x, y, image, firstImage, secondaryImage, screenSpeed, speedModifier, rect, scale, frame1, frame2)\
        
class BirdLow(Bird):
    def __init__(self, name='bird', x=0, y=0, image='resources/dark_bird_low_down.png', firstImage='resources/dark_bird_low_down.png', secondaryImage='resources/dark_bird_low_down.png', screenSpeed=0, speedModifier=0, rect=[10,105,42,33], scale=1, frame1='resources/dark_bird_low_down.png', frame2='resources/dark_bird_low_up.png'):
        super().__init__(name, x, y, image, firstImage, secondaryImage, screenSpeed, speedModifier, rect, scale, frame1, frame2)


#'''
class Theme:
    def __init__(self,cactus_options = [],power_up_options = [],runner = Runner(),clouds = Clouds(),ground = Ground(),ground2=Ground(x=598),background = Background(),power_up = PowerUp(),cactus=Cactus()):

        self.cactus_options=cactus_options
        self.power_up_options=power_up_options
        self.runner=runner
        self.clouds=clouds
        self.ground=ground
        self.ground2=ground2
        self.background=background
        self.power_up=power_up
        self.cactus=cactus
        self.objects= [self.background,self.ground,self.ground2,self.clouds,self.runner,self.power_up,self.cactus]

    def change_speed(self,speed):
        for object in self.objects:
            object.screenSpeed = speed

    def theme_change(self):
        for object in self.objects:
            object.colorChange()

    def collision_check(self):
        if not self.runner.invincible:
            if self.runner.collisionCheck(self.cactus):
                self.runner.die()
                return 1
        elif self.runner.collisionCheck(self.power_up):
            self.power_up.effect(self) # update later. figure out how powerups are gonna work
            self.power_up.state=False
            return 2
        else: return 0

    def show_all(self):
        for object in self.objects:
            if object == self.power_up:
                if object.state == True:
                    
                    object.show()
                else: pass
            else:
                object.show()
    def hitboxes(self):
        colors=[(255,0,0), # red, bg
                (0,255,0), # green, ground
                (0,255,0), # green, ground2
                (255,255,0), # yellow, clouds
                (255,0,255), # magenta, runner
                (0,255,255), # cyan, powerup
                (255,128,0) # orange, cactus
                ]
        #print(len(self.objects))
        for object in self.objects:
            color = colors[self.objects.index(object)]
            object.hitbox_draw(color)

#       ''' 
on_screen = Theme()
on_screen.runner.direction=None
running = True
speed=0
time=0
score=0000

score_font = pygame.font.Font('freesansbold.ttf', 14)
font_color = (0, 0, 0)
font_location = (480, 10)
dead=True
highScore=0

def start(on_screen):
    speed=5
    dead = False
    on_screen.runner.y=85
    on_screen.runner.hitbox_update()
    on_screen.cactus.x=800
    return speed, dead

def temp(on_screen):
    return None, False


while running:
    clock.tick(60)
    time+=1
    resrart=temp


    for event in pygame.event.get():
        keys = pygame.key.get_pressed()

        if event.type == pygame.QUIT: # Close the window
            running = False

        if event.type == pygame.KEYDOWN: # Key is pressed
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]: # if space or up is pressed
                
                if speed == 0: #reset after death
                    resrart=start
                on_screen.runner.direction='up'

                walking=on_screen.runner.jump_frame

            elif keys[pygame.K_DOWN]: # if down arrow is pressed
                walking=on_screen.runner.crouch

        else: walking=on_screen.runner.walk
        if pygame.mouse.get_pressed()[0]:
            if speed == 0: #reset after death
                resrart=start
            on_screen.runner.direction='up'
                    
    # collision detection

    if on_screen.collision_check()==1: # Death
        dead=True
        
    if dead:
        speed=0
        walking=on_screen.runner.die 
        on_screen.runner.image=on_screen.runner.firstImage
        if score > highScore:
            highScore=score
        else:
            highScore=highScore
        score=0
    else:
    # show items
    
        on_screen.runner.jump()
        if (time//5-time/5)==0:
            walking()
            score+=1
        

    vars=resrart(on_screen)
    speed=vars[0] if vars[0]!=None else speed
    dead = vars[1]

    on_screen.change_speed(speed)
    on_screen.show_all()
    on_screen.hitboxes() #debugging hitboxes

    # cactus Hitboxes
    '''    objects=[Background(),Ground(),CactusBigSingle(x=100),CactusQuartet(x=170),CactusSmallDuo(x=250),CactusSmallSingle(x=500),CactusSmallTriad(x=50),BirdHigh(x=320),BirdMiddle(x=380),BirdLow(x=450)]
    for object in objects:
                object.show()
                object.hitbox_draw((255,0,0))'''
    
    screen.blit(score_font.render(f"HI: {str(highScore).zfill(5)} {str(score).zfill(5)}", True, font_color), font_location)
    # update screen
    pygame.display.flip()
    
