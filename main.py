#import pygame
import pygame
import random
import math
#initalize pygame
pygame.init()

# create the screen
screen=pygame.display.set_mode((800,600))
# set window title
pygame.display.set_caption('Working Title')

# Load in and set Puzzle Logo
corner_image= pygame.image.load('jigsaw.png')
pygame.display.set_icon(corner_image)
#load background
background=pygame.image.load('white-cloud-blue-sky.jpg')
#load laser

#set player
playerImg=pygame.image.load('superhero (1).png')
# player starting coordinates and movement
playerX=370
playery=480
playerx_delta=0
playery_delta=0
run_game=True
# set enemy
enemyImg= pygame.image.load('enemy.png')
enemyx=[]
enemyy=[]
enemyx_delta=[]
enemyy_delta=[]
num_enemies=4
for i in range(num_enemies):

    enemyx.append(random.randint(0,800))
    enemyy.append(random.randint(50,150))
    enemyx_delta.append(.3)
    enemyy_delta.append(.2)
#set score
score_val=0
font= pygame.font.Font('freesansbold.ttf',32)
score_x=10
score_y=10

#game over
game_over= pygame.font.Font('freesansbold.ttf',64)
def game_over_text():
    game_over_message=font.render('GAME OVER',True,(255,255,255))
    screen.blit(game_over_message,(200,250))
def displayScore(x,y):
    score = font.render('Score: '+str(score_val),True,(255,255,255))
    screen.blit(score,(x,y))
#set laser
laserImg= pygame.image.load('laser2.png')
laserX=0
lasery=480
laserx_delta=0
lasery_delta=4
#if laser is set to 0 it is not being fired, if it is 1 it is being fired
laserstate='ready'
# player function
def player(x,y):
    screen.blit(playerImg,(x,y))
# new enemy
def enemy(x,y):
    screen.blit(enemyImg,(x,y))

def fireLaser(x:float,y:float)->None:
    global laserstate
    laserstate='fire'
    screen.blit(laserImg,(x+16,y+10))
def isCollision(enemyx,enemyy,laserx,lasery):
    distance=math.sqrt( math.pow(enemyx-laserx,2) + math.pow(enemyy-lasery,2))
    if distance < 27:
        return True

    else: False
while run_game:

    screen.fill((102, 255, 255))
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            run_game= False
        # if key is checked
        if event.type ==pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_delta =-.5
            if event.key == pygame.K_RIGHT:
                playerx_delta =.5
            if event.key == pygame.K_UP:
                playery_delta =-.5
            if event.key == pygame.K_DOWN:
                playery_delta =.5
            if event.key ==pygame.K_SPACE:
                if laserstate is 'ready':
                    laserX=playerX
                    lasery=playery
                    fireLaser(laserX, lasery)
        if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key==pygame.K_RIGHT:
                    playerx_delta =0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    playery_delta =0

#enemy x border movement
    for i in range(num_enemies):
        if enemyx[i] <= 0:
            enemyx[i] = 0
        elif enemyx[i] >= 736:
            enemyx[i] = 736
        if enemyy[i]>600:
            enemyy[i]-=600
            enemyx[i]=random.randrange(1,600)


    # enemy change direction
        if enemyx[i] <= 0:
            enemyx_delta[i]=.3
        elif enemyx[i] >= 736:
            enemyx_delta[i]= -.3
        if enemyy[i]<600:
            enemy(enemyx[i],enemyy[i])

        enemyy[i] += enemyy_delta[i]
        enemyx[i] += enemyx_delta[i]
        #collision
        collide = isCollision(enemyx[i], enemyy[i], laserX, lasery)
        if collide:
            lasery = 0
            laserstate = 'ready'
            score_val += 1

            enemyx[i] = random.randint(0, 800)
            enemyy[i] = random.randint(0, 100)
        player_collison=isCollision(enemyx[i],enemyy[i],playerX,playery)
        if player_collison:
            game_over_text()
            break


    #Laser reset if out of bounds
    # Laser movement after being fired,
    if lasery<0:
        lasery=480
        laserstate='ready'
    if laserstate is 'fire':
        fireLaser(laserX, lasery)
        lasery -= lasery_delta


    #player movement
    playerX += playerx_delta

    if playerX <=0:
        playerX=0
    if playerX>=740:
        playerX=740
    playery += playery_delta
    player(playerX,playery)
    displayScore(score_x,score_y)
    pygame.display.update()
