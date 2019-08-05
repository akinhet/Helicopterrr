import pygame
import os
import random

pygame.init()

wid = 600
hei = 600
screen = pygame.display.set_mode((wid,hei))

# Procedura pisania na ekranie

def write(text, x, y, size):
        ft = pygame.font.SysFont('Arial', size)
        rend = ft.render(text, 1, (255, 0, 0))
        screen.blit(rend, (x,y))

# Procedura pisania na srodku ekranu

def write_mid(text, size):
        ft = pygame.font.SysFont('Arial', size)
        rend = ft.render(text, 1, (255, 0, 0))
        x = (wid - rend.get_rect().width)/2
        y = (hei - rend.get_rect().height)/2
        screen.blit(rend, (x,y))

displaying = 'menu'

prev_height_up = 200
hei_up_count = 0

class Obstacle():
        def __init__(self, x, width):
                self.x = x
                self.width = width
                self.y_up = 0
                self.distance = 200
                global hei_up_count
                if hei_up_count >= 40:
                        global prev_height_up
                        prev_height_up = random.randint((prev_height_up-30),(prev_height_up+30))
                        while prev_height_up <= 10 or prev_height_up >= (hei-(self.distance+10)):
                                prev_height_up = random.randint((prev_height_up-30),(prev_height_up+30))
                else:
                        hei_up_count = hei_up_count + 1
                
                self.height_up = prev_height_up
                self.y_down = self.height_up + self.distance
                self.height_down = hei - self.y_down
                self.color = (160,140,190)
                self.shape_up = pygame.Rect(self.x, self.y_up, self.width, self.height_up)
                self.shape_down = pygame.Rect(self.x, self.y_down, self.width, self.height_down)
                
        def draw(self):
                pygame.draw.rect(screen, self.color, self.shape_up, 0)
                pygame.draw.rect(screen, self.color, self.shape_down, 0)
                
        def move(self,v):
                self.x = self.x - v
                self.shape_up = pygame.Rect(self.x, self.y_up, self.width, self.height_up)
                self.shape_down = pygame.Rect(self.x, self.y_down, self.width, self.height_down)
                
        def collision(self,player):
                if self.shape_up.colliderect(player) or self.shape_down.colliderect(player):
                        return True
                else:
                        return False

class Helicopter():
        def __init__(self,x,y):
                self.x = x
                self.y = y
                self.width = 62
                self.height = 32
                self.shape = pygame.Rect(self.x, self.y, self.width, self.height)
                self.graphic = pygame.image.load(os.path.join('helicopter.png'))
                
        def draw(self):
                screen.blit(self.graphic, (self.x,self.y))
                
        def move(self, v):
                self.y = self.y + v
                self.shape = pygame.Rect(self.x, self.y, self.width, self.height)

# Inicjowanie przeszkod

def obs_draw():
        for i in range(21):
                obstacles.append(Obstacle(i*wid/20,wid/20))

obstacles = []

# Inicjowanie gracza

player = Helicopter(250,275)

dy = 0
dy_count = 0
up = 0
down = 0

points = 0

while True:
        pygame.display.update()
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                        
                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                                up = 1
                        if event.key == pygame.K_DOWN:
                                down = 1
                                
                        if event.key == pygame.K_SPACE:
                                if displaying != 'game':
                                        displaying = 'game'
                                        points = 0
                                        hei_up_count = 0
                                        prev_height_up = 200
                                        for o in obstacles:
                                                obstacles.remove(o)
                                        obs_draw()
                                        
                if event.type == pygame.KEYUP:
                        if event.key == pygame.K_UP:
                                up = 0
                                
                        if event.key == pygame.K_DOWN:
                                down = 0

                                
        screen.fill((0,0,0))
        if displaying == 'menu':
                write_mid('Press space to start', 35)
                logo = pygame.image.load(os.path.join('logo.png'))
                x_logo = (wid - logo.get_rect().width)/2
                screen.blit(logo, (x_logo, 190))
        
        elif displaying == "game":
                for o in obstacles:
                        o.move(1)
                        o.draw()
                        
                        # Wykrywanie kolizji

                        if o.collision(player.shape):
                                player = Helicopter(250,275)
                                dy = 0
                                displaying = 'end'

                dy = 0     
                if up == 1:
                        dy_count = dy_count + 1
                        if dy_count == 2:
                                dy = -1
                                dy_count = 0
                elif down == 1:
                        dy_count = dy_count + 1
                        if dy_count == 2:
                                dy = 1
                                dy_count = 0
                                
                # Przenoszenie przeszkod z jednego konca ekranu na drugi
                
                for o in obstacles:
                        if o.x <= -o.width:
                                obstacles.remove(o)
                                obstacles.append(Obstacle(wid,wid/20))
                                points = points + 1
                player.draw()
                player.move(dy)
                write(str(points),5,5,30)
                
        elif displaying == 'end':
                write_mid('You lose. Press space to try again.', 35)
                write(str(points),5,5,30)
                player = Helicopter(250,275)






        
