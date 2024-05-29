#Imports
import pygame
import random
import math


#Initializations
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Limbo!")
clock = pygame.time.Clock()
times = 0
answer_key = pygame.image.load("misc/Yellow.png") 
fake_key = pygame.image.load("misc/Gray.png")
font = pygame.font.Font("misc/Retro Gaming.ttf", 64)
font2 = pygame.font.Font("misc/Retro Gaming.ttf", 32)
limbo_text = font.render("Limbo ", True, (255, 255, 0))
win_text = font.render("You Win!", True, (255, 255, 0))
lose_text = font.render("You Lose!", True, (255, 255, 0))
enter_text = font2.render("Enter No of Keys:", True, (255, 255, 0))
limit_text = font2.render("(Select number of keys from 2 to 24)", True, (255, 255, 0))
controls = font2.render("Press Space to start/restart game", True, (255, 255, 0))
controls2 = font2.render(" Escape to return to menu", True, (255, 255, 0))
num = ""


#Booleans
started = False
reset = False
held = False
game = False
win = False
lose = False
in_menu = True

#Classes
class Keys:
    def __init__(self, posx, posy, type, endx,endy):
        self.posx = posx
        self.calculating = False
        self.posy = posy
        self.type = type
        self.endx = endx
        self.endy = endy
        self.angle = math.atan2(endy - posy, endx - posx)
        self.velocity = random.randint(10,20)
        self.distance = math.sqrt((endx - posx)**2 + (endy - posy)**2)
    
    def recalculate(self,end):
        self.endx, self.endy = end
        self.angle = math.atan2(self.endy - self.posy, self.endx - self.posx)
        self.distance = math.sqrt((self.endx - self.posx)**2 + (self.endy - self.posy)**2)

    def draw(self, screen, started,game):
        if self.type == 0 or started or game:
            screen.blit(fake_key, (self.posx, self.posy))
        else:
            screen.blit(answer_key, (self.posx, self.posy))
    
    def update(self):
        if self.distance > 0:
            self.posx += self.velocity*math.cos(self.angle)
            self.posy += self.velocity*math.sin(self.angle)
            self.distance-=self.velocity
        else:
            self.posx, self.posy = self.endx, self.endy
            self.calculating = False

        

#Loop
while True:
    screen.fill((21,34,56))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()       
        elif event.type == pygame.KEYDOWN and in_menu:
            try:
                chr(event.key)
            except ValueError:
                event.key = 0
            if chr(event.key).isdigit():
                num += chr(event.key)
                if int(num) > 24:
                    num = num[:-1]
            elif event.key == pygame.K_BACKSPACE:
                num = num[:-1]
            elif event.key == pygame.K_RETURN and num != "":
                if int(num) > 1:
                    in_menu = False
                    key_pattern = []
                    for i in range(int(num)):
                        key_pattern.append(0)
                    key_pattern[random.randint(0, int(num)-1)] = 1
    
                    #Display all keys
                    start = []
                    for i in range(len(key_pattern)):
                        start.append([130 + (i%6)*100, 100+i//6*150])
                    end = start.copy()
                    random.shuffle(end)
        
                    #Create Keys
                    keys_list = []
                    for count, i in enumerate(key_pattern):
                        if i == 1:
                            keys_list.append(Keys(start[count][0], start[count][1], 1, end[count][0], end[count][1]))
                        else:
                            keys_list.append(Keys(start[count][0], start[count][1], 0, end[count][0], end[count][1]))

    screen.blit(limbo_text, (300, 0))
    if in_menu:
        screen.blit(enter_text, (250, 100))
        pygame.draw.rect(screen, (255, 255, 0), (610, 105, 100, 35), 2)
        screen.blit(font2.render(num, True, (255, 255, 0)), (635, 102))
        screen.blit(limit_text, (50, 150))
        screen.blit(controls, (50, 200))
        screen.blit(controls2, (150, 250))
    else:
       keys = pygame.key.get_pressed()
       if keys[pygame.K_SPACE]:
           held = True
       if held and not keys[pygame.K_SPACE]:
           started= True
           times = random.randint(5,9)
           held = False
       for i in keys_list:
           i.draw(screen, started,game)
           if started:
               i.calculating = True
               i.update()
       if started:
           c=0
           for i in keys_list:
               if i.calculating:
                   break
               c+=1
           if c==len(key_pattern):
               reset = True
               pygame.time.delay(5)
           if reset and times > 0:
               times -= 1
               random.shuffle(end)
               for count, i in enumerate(keys_list):
                   i.recalculate(end[count])
                   i.calculating = True
           reset = False
       if started and times == 0:
           started = False
           game = True
   
       if game:
           mouse = pygame.mouse.get_pos()
           if pygame.mouse.get_pressed()[0]:
               for i in keys_list:
                   if mouse[0] > i.posx and mouse[0] < i.posx + fake_key.get_width() and mouse[1] > i.posy and mouse[1] < i.posy + fake_key.get_height():
                       if i.type == 1:
                           win = True
                       else:
                           lose = True
                       game=False
   
                       
           
       if win:
           screen.blit(win_text, (250, 500))
           if keys[pygame.K_SPACE]:
               win = False
       if lose:
           screen.blit(lose_text, (220, 500))
           if keys[pygame.K_SPACE]:
               lose = False
       if lose or win: 
           if keys[pygame.K_ESCAPE]:
               in_menu=True
               win = False
               lose = False
    pygame.display.update()        
    clock.tick(60)
