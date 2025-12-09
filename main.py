# CS T Rex Runner
from abc import ABC, abstractmethod
import pygame
from pygame import mixer
import random
import socket
pygame.init()
clock = pygame.time.Clock()

size=(598,149)



class User:
    def __init__(self, index, username, score=0):
        self.index = index
        self.username = username
        self.score = score
    def export_data(self):
        return [self.index, self.username, self.score]

class CsvLoader:
    def __init__(self, filepath):
        self.filepath = filepath

    def load_data(self):
        users = []
        try:
            with open(self.filepath, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    index, username, score = line.strip().split(',')
                    users.append(User(int(index), username, int(score)))
        except FileNotFoundError:
            pass
        return users
    
    def save_data(self, users):
        with open(self.filepath, 'w') as file:
            for user in users:
                file.write(','.join(map(str, user.export_data())) + '\n')
    
    def exists(self, username):
        users = self.load_data()
        for user in users:
            if user.username == username:
                return True
        return False

    def add_user(self, username):
        if not self.exists(username):
            with open(self.filepath, 'a') as file:
                index = sum(1 for line in open(self.filepath)) + 1
                file.write(f"{index},{username},0\n")
    
    def update_score(self, username, new_score):
        if self.exists(username):
            users = self.load_data()
            for user in users:
                if user.username == username:
                    user.score = new_score
            self.save_data(users)
        else:
            self.add_user(username)

    def remove_user(self, username):
        users = self.load_data()
        users = [user for user in users if user.username != username]
        self.save_data(users)

    def get_user(self, username):
        users = self.load_data()
        
        for user in users:
            if user.username == username:
                return user
        return User(len(users)+1, username, 0)




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
        self.hitbox=rect
        self.hitbox_update()
        

    def __str__(self):
        return f"{self.name} at ({self.x},{self.y})"
     
            
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

    def gone(self):
        nums=[]
        num = 0
        if type(self.hitbox) == list: 
            for box in self.hitbox:
                nums.append(box[2])
            for n in nums:
                if n>num:
                    num=n
        else: num=self.hitbox[2]

        nums=[]
        left=0
        if type(self.hitbox) == list: 
            for box in self.hitbox:
                nums.append(box[0])
            for n in nums:
                if n<left:
                    left=n
        else: left=self.hitbox[0]

        if left<(0-num): 
            return True
        else: return False
    
    def move(self):
            speed=self.screenSpeed*self.speedModifier
            self.x-=speed
            self.hitbox_update()
           
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
    def __init__(self, name="powerup", x=1000, y=20, image='resources/light_neutral.png', firstImage='resources/light_neutral.png', secondaryImage='resources/light_neutral.png', screenSpeed=0, speedModifier=1, rect=None, state=False, sound=None,scale=1):
        super().__init__(name, x, y, image, firstImage, secondaryImage, screenSpeed, speedModifier, rect,scale)
        self.state=state
        self.sound=sound

    def show(self):
        if self.state == True:
            self.move()
            screen.blit(self.image,(self.x,self.y))
     

    @abstractmethod
    def effect(self,theme):
        pass


class Runner(OnScreen):
    def __init__(self, name='dino', x=0, y=85, image="resources/light_neutral.png", firstImage="resources/light_neutral.png", secondaryImage="resources/dark_neutral.png", frame1='resources/light_right.png',frame2='resources/light_left.png',crouch1='resources/light_crouch_right.png',crouch2='resources/light_crouch_left.png',screenSpeed=0, speedModifier=0, rect=[[12,11,20,42],[12,11,41,20]],crouchRect=[11,30,41,20],jumpHeight=155,state=True,invincible=False,scale=1,direction='up',jump_sound=None,death_sound=None):
        super().__init__(name, x, y, image, firstImage, secondaryImage, screenSpeed, speedModifier, rect,scale)
        self.jumpHeight=jumpHeight
        self.state=state
        self.invincible=invincible
        self.direction=direction
        self.frame1=pygame.image.load(frame1)
        self.frame2=pygame.image.load(frame2)
        self.crouch1=pygame.image.load(crouch1)
        self.crouch2=pygame.image.load(crouch2)
        self.jump_sound=jump_sound
        self.death_sound=death_sound
        self.crouchRect=crouchRect
    '''   
    def hitbox_update(self): #adjust hitbox position to account for movement
        # hitbox key: [x offset, y offset, width, height]
        if self.direction == 'crouch':
                rect=self.crouchRect
        else:
            rect=self.rect
        
        self.hitbox=[]
        for i in range(len(self.rect)):
            self.hitbox.append(pygame.rect.Rect(self.x+rect[i][0],self.y+rect[i][1],rect[i][2],rect[i][3]))
           '''
        

    def move(self):
            speed=self.screenSpeed*self.speedModifier
            self.x-=speed

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
        if self.death_sound!=None:
            pygame.mixer.sound.play(pygame.mixer.Sound(self.death_sound))
        else:
            print("death")
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

    def jumping_sound(self):
        if self.jump_sound!=None:
            pygame.mixer.sound.play(pygame.mixer.Sound(self.jump_sound))
        else:
            print("jump")

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
    def __init__(self, name='bird_high', x=0, y=0, image='resources/light_bird_high_down.png', firstImage='resources/light_bird_high_down.png', secondaryImage='resources/light_bird_high_down.png', screenSpeed=0, speedModifier=0, rect=[10,55,42,33], scale=1, frame1='resources/light_bird_high_down.png', frame2='resources/dark_bird_high_up.png'):
        super().__init__(name, x, y, image, firstImage, secondaryImage, screenSpeed, speedModifier, rect, scale, frame1, frame2)

class BirdMiddle(Bird):
    def __init__(self, name='bird_middle', x=0, y=0, image='resources/light_bird_middle_down.png', firstImage='resources/light_bird_middle_down.png', secondaryImage='resources/dark_bird_middle_down.png', screenSpeed=0, speedModifier=0, rect=[10,80,42,33], scale=1, frame1='resources/light_bird_middle_down.png', frame2='resources/light_bird_middle_up.png'):
        super().__init__(name, x, y, image, firstImage, secondaryImage, screenSpeed, speedModifier, rect, scale, frame1, frame2)\
        
class BirdLow(Bird):
    def __init__(self, name='bird_low', x=0, y=0, image='resources/dark_bird_low_down.png', firstImage='resources/dark_bird_low_down.png', secondaryImage='resources/dark_bird_low_down.png', screenSpeed=0, speedModifier=0, rect=[10,105,42,33], scale=1, frame1='resources/dark_bird_low_down.png', frame2='resources/dark_bird_low_up.png'):
        super().__init__(name, x, y, image, firstImage, secondaryImage, screenSpeed, speedModifier, rect, scale, frame1, frame2)


#'''
class Theme:
    def __init__(self,cactus_options = [CactusSmallSingle,CactusSmallDuo,CactusSmallTriad,CactusBigSingle,CactusQuartet],bird_options = [BirdHigh,BirdMiddle,BirdLow],power_up_options = [PowerUp],runner = Runner(),cloud_options = [Clouds],ground_options = [Ground],background = Background(),speed=0):
        self.runner=runner

        self.cloud_options=cloud_options
        self.clouds=[random.choice(self.cloud_options)(),random.choice(self.cloud_options)(x=400)]
        
        self.background=background

        self.ground_options=ground_options
        self.ground=[random.choice(self.ground_options)(),random.choice(self.ground_options)(x=598)]

        #powerup handling
        
        self.power_up_options=power_up_options
        self.power_up=[random.choice(self.power_up_options)(),random.choice(self.power_up_options)()]
        
        #enemy handling
        self.enemy_options=cactus_options+bird_options
        self.enemies=[random.choice(self.enemy_options)(x=800),random.choice(self.enemy_options)(x=1600)]

        self.objects= [self.background,self.ground,self.clouds,self.runner,self.power_up,self.enemies]

        self.speed=speed


    def change_speed(self,speed):
        #print(speed,speed//1)
        if speed//1 == speed: # integer check
            self.speed=speed
            for object in self.objects:
                if type(object)==list: 
                    for item in object:
                        item.screenSpeed = speed
                else: object.screenSpeed = speed
            

    def theme_change(self):
        for object in self.objects:
            if type(object)==list:
                for item in object:
                    item.colorChange()
            else:
                object.colorChange()

    def collision_check(self):
        if not self.runner.invincible:
            if type(self.enemies)==list:
                for enemy in self.enemies:
                    if self.runner.collisionCheck(enemy):
                        return 1
            else:
                if self.runner.collisionCheck(self.enemies):
                    return 1
        elif self.runner.collisionCheck(self.power_up):
            self.power_up.effect(self) # update later. figure out how powerups are gonna work
            self.power_up.state=False
            return 2
        else: return 0
                
        

    def show_all(self):
        params={'background':[600,self.background], # background
               'ground':[598,self.ground_options], # 
               'clouds':[600,self.cloud_options], # 
               'runner':[0,self.runner], # 
               'powerup': [600,self.power_up_options], # 
               'enemy':[800,self.enemy_options] # 
               }
        

        for objects in self.objects:
            name=list(params.keys())[self.objects.index(objects)]
            new_x=params[name][0]
            object_options=params[name][1]
            #

            if type(objects)==list:
                for object in objects:

                    if object.gone():
                        
                        objects.remove(object)
                        new_object=random.choice(object_options)(x=new_x,screenSpeed=self.speed)
                        objects.append(new_object)
                        
                        
                        #print(objects[0],objects[1])
                        objects[-1].show()
                    else: object.show()

            else:
                if objects.gone():
                    objects=random.choice(object_options)(x=new_x)
                objects.show()


    def hitboxes(self):
        colors=[(255,0,0), # red, bg
                (0,255,0), # green, ground
                (255,255,0), # yellow, clouds
                (255,0,255), # magenta, runner
                (0,255,255), # cyan, powerup
                (255,128,0) # orange, cactus
                ]
        #print(len(self.objects))
        for object in self.objects:
            color = colors[self.objects.index(object)]
            if type(object)==list:
                for item in object:
                    item.hitbox_draw(color)
            else:
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



csv=CsvLoader('scoreboard.csv')
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

player=csv.get_user(IPAddr)

highScore=player.score



def start(on_screen):
    speed=5
    dead = False
    on_screen.runner.y=85
    on_screen.runner.hitbox_update()
    for cactus in on_screen.enemies:
        if cactus.x<800 and cactus.x>-60:
            cactus.x=800


    return speed, dead

def temp(on_screen):
    return None, False
def dead_restart(on_screen):
    return 0, True


while running:
    clock.tick(60)
    time+=1
    resrart=temp

    if on_screen.runner.direction=='crouch':
        on_screen.runner.direction='crouch'

    for event in pygame.event.get():
        keys = pygame.key.get_pressed()

        if event.type == pygame.QUIT: # Close the window
            running = False

        if event.type == pygame.KEYDOWN: # Key is pressed
            if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w] : # if space or up is pressed
                
                if speed == 0: #reset after death
                    resrart=start
                    on_screen.runner.direction='up'
                    on_screen.runner.jumping_sound()
                elif on_screen.runner.y==85:
                    on_screen.runner.direction='up'
                    on_screen.runner.jumping_sound()

                walking=on_screen.runner.jump_frame

            elif keys[pygame.K_DOWN]or keys[pygame.K_s]:
                if speed == 0: #reset after death
                    resrart=start
                on_screen.runner.direction='crouch'
                walking=on_screen.runner.crouch
                print(on_screen.runner.direction)
                print(walking)

        else: walking=on_screen.runner.walk

        if pygame.mouse.get_pressed()[0] : # if mouse clicked
            if speed == 0: #reset after death
                    resrart=start
                    on_screen.runner.direction='up'
                    on_screen.runner.jumping_sound()
            elif on_screen.runner.y==85:
                    on_screen.runner.direction='up'
                    on_screen.runner.jumping_sound()
        
        
                    
    # collision detection

    if on_screen.collision_check()==1: # Death
        if dead == False:
            on_screen.runner.die()
        dead=True
        resrart=dead_restart if resrart != start else resrart
        
        walking=on_screen.runner.jump_frame

    # seperate frame rate dependent movement
        
   
        
    if speed != 0:
        on_screen.runner.jump()
        if (time//5-time/5)==0:
            walking()
            score+=1
            speed+=0.1
        
       
    else:
        on_screen.runner.image=on_screen.runner.firstImage
        if score > highScore:
            highScore=score
            csv.update_score(IPAddr,highScore)
        else:
            highScore=highScore
        score=0
        
    # show items
    vars=resrart(on_screen)
    speed=vars[0] if vars[0]!=None else speed
    dead = vars[1]

    on_screen.change_speed(speed)
    on_screen.show_all()

    if walking == on_screen.runner.crouch:
        on_screen.runner.direction='crouch'

    on_screen.hitboxes() #debugging hitboxes
    
    screen.blit(score_font.render(f"HI: {str(highScore).zfill(5)} {str(score).zfill(5)}", True, font_color), font_location)
    # update screen
    pygame.display.flip()
    
