import pygame
import math
import random # for random values
from pygame import mixer

pygame.init() # to initialize the pygame it is must otherwise program not run

screen = pygame.display.set_mode((800,600)) #screen size

#Title and Icon 
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load(r'D:\Programming Code\Git Repo\Space Invader\Images\spaceship.png')
pygame.display.set_icon(icon)

#background music
mixer.music.load(r'D:\Programming Code\Git Repo\Space Invader\Music\background.mp3')
mixer.music.play(-1)

#player
playerImg = pygame.image.load(r'D:\Programming Code\Git Repo\Space Invader\Images\player.png')
playerX = 370
playerY = 480
playerX_change = 0

#Enemy 
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 6

for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load(r'D:\Programming Code\Git Repo\Space Invader\Images\enemy.png')) 
    enemyX.append(random.randint(0,735)) 
    enemyY.append(random.randint(50,150)) 
    enemyX_change.append(2) 
    enemyY_change.append(40) 

#background Image
backgroundImg = pygame.image.load(r'D:\Programming Code\Git Repo\Space Invader\Images\background.png')

#bullet
#ready - we can't see the bullet
#fire - bullet is moving
bulletImg = pygame.image.load(r'D:\Programming Code\Git Repo\Space Invader\Images\bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 25
bullet_state = 'ready'

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',24)
textX = 10
textY = 10

#game over
over_font = pygame.font.Font('freesansbold.ttf',72)
res_font = pygame.font.Font('freesansbold.ttf',30)
def game_over():
    over_text = over_font.render("GAME OVER ", True, (3, 186, 252))
    screen.blit(over_text,(200,200))
    
    


def show_score(x,y):
    score = font.render('Score: ' +str(score_value*10,True, (255,255,255))
    screen.blit(score, (x,y))


def fire_bullet(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg,(x+16 ,y+10))


def player(x,y):
    screen.blit(playerImg,(x,y)) # blit() method just draw this need two parameter. player and its coordinates
    
def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))
    
def isCollision(enemyX, enemyY, bulletX, buleetY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance <27:
        return True
    else:
        return False

#as screen is display for just few second so 
#game loop
running = True
game_over_var = False
while running:
    if game_over_var:

         #RGB
        screen.fill((0,0,0)) # but this not show on game window to do this
        
        #background draw
        screen.blit(backgroundImg,(0,0))
        game_over()
        for event in  pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    else:
            #RGB
        screen.fill((0,0,0)) # but this not show on game window to do this
        
        #background draw
        screen.blit(backgroundImg,(0,0))
        
        for event in  pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        #if keystroke is pressed or not
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -8
                if event.key == pygame.K_RIGHT:
                    playerX_change = 8
                if event.key == pygame.K_SPACE:
                    if bullet_state is 'ready':
                        bullet_sound = mixer.Sound(r'D:\Programming Code\Git Repo\Space Invader\Music\laser_gun.wav')
                        bullet_sound.play()
                        bulletX = playerX
                        fire_bullet(bulletX,bulletY)
                        
                            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0  
        #Creating boundaries  for player          
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736 
        
        #creating boundaries for enemy
        for i in range(no_of_enemies):
            
            #game over
            if enemyY[i] > 300:
               
                game_over_var = True
                break
            
            
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 2
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -2
                enemyY[i] += enemyY_change[i]
                
            #collision    
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision :
                explode_sound = mixer.Sound(r'D:\Programming Code\Git Repo\Space Invader\Music\explosion.wav')
                explode_sound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0,735)
                enemyY[i] = random.randint(50,150) 
                
            enemy(enemyX[i],enemyY[i], i)
            
        if bulletY <=0:
            bulletY = 480
            bullet_state = 'ready'    
            
        if bullet_state is 'fire':
            fire_bullet(bulletX,bulletY)
            bulletY -= bulletY_change  
        
                        
        
        playerX += playerX_change
        
        player(playerX,playerY) #it must draw after screen.fill because first screen is drawn then player is drawn
        show_score(textX,textY)



    
    
    pygame.display.update() # we use update method        
