import pygame, sys, time, random

pygame.init()

#Colours
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
pink = (255,0,255)
yellow = (255,255,0)

#Display
screenX = 800
screenY = 600
size = (screenX,screenY)
screen = pygame.display.set_mode((size))
pygame.display.set_caption("Christmas Quest")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

pygame.display.update()
clock = pygame.time.Clock()

#Images
background = pygame.image.load("background.jpg")
christmas = pygame.image.load("christmas.jpg")
santa = pygame.image.load("santa.png")
present = pygame.image.load("gift.png")
cane = pygame.image.load("candycane.png")
burn = pygame.image.load("fireplace.png")
slow = pygame.image.load("cloud.png")

#Text Fonts
ComicSansMS1 = pygame.font.SysFont("ComicSansMS",50)
ComicSansMS2 = pygame.font.SysFont("ComicSansMS",40)
Calibri = pygame.font.SysFont("Calibri",30)

#Text Functions
#textObjects & centeredText Functions (From: The New Boston)

def textObjects(text,colour,font):
    textSurf = font.render(text,True,colour)
    return textSurf,textSurf.get_rect()

def centeredText(msg,font,colour):
    textSurface,textRect = textObjects(msg,colour,font)
    textRect.center = (screenX/2),(screenY/2)
    screen.blit(textSurface,textRect)
    
def locationText(msg,font,colour,x,y):    
    screenText = font.render(msg,True,colour)
    screen.blit(screenText,(x,y))

#Image of Instructions Text
#Line break doesn't work in pygame so instead image of text 
paragraph = pygame.image.load("instructions.png")

#Start Screen Function
def start():
    startGame = True
    while startGame == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    startGame = False
        screen.fill(black)
        cb = screen.blit(christmas,(0,0))
        locationText("Christmas Quest",ComicSansMS1,green,390,40)
        instructions = screen.blit(paragraph,(310,150))
        locationText("Press S to start the game.",ComicSansMS2,white,300,500)
        pygame.display.update()               

#Game Loop
def gameLoop():
    gameExit = False
    gameOver = False

    #Variables
    
    #Dimensions
    playerD = 75
    giftW = 29
    giftH = 34
    fireplaceD = 40
    candyW = 23
    candyH = 30
    cloudW = 100
    cloudH = 55

    #Locations
    playerX = screenX/2 - playerD/2
    playerY = screenY/2 - playerD/2
    giftX = 100
    giftY = 100
    fireplaceX = 650
    fireplaceY = 400
    candyX = random.randint(0,screenX-candyW)
    candyY = random.randint(0,screenY-100-candyH)
    cloud1X = random.randint(0,screenX-cloudW)
    cloud1Y = random.randint(0,screenY-100-cloudH)
    cloud2X = random.randint(0,screenX-cloudW)
    cloud2Y = random.randint(0,screenY-100-cloudH)

    #Other Variables
    speed = 4
    pointCount = 0
    timer = 3600
    
    while not gameExit:

        #Game over screen
        while gameOver == True:
            screen.fill(black)
            bg = screen.blit(background,(0,0))
            locationText("Points: %s" %(pointCount),Calibri,black,15,560)
            locationText("Timer: %s" %(timer/60),Calibri,black,670,560)
            centeredText("Press P to play again or Q to quit.",ComicSansMS2,white)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_p:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

        screen.fill(black)
        bg = screen.blit(background,(0,0))

        #Text(during game)
        locationText("Points: %s" %(pointCount),Calibri,black,15,560)
        locationText("Timer: %s" %(timer/60),Calibri,black,670,560)

        #Sprites
        candy = screen.blit(cane,(candyX,candyY))
        cloud1 = screen.blit(slow,(cloud1X,cloud1Y))
        cloud2 = screen.blit(slow,(cloud2X,cloud2Y))
        gift = screen.blit(present,(giftX,giftY))
        fireplace = screen.blit(burn,(fireplaceX,fireplaceY))
        player = screen.blit(santa,(playerX,playerY))
        pygame.display.update()

        #Player Movement
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            playerX -= speed
        if keys[pygame.K_RIGHT]:
            playerX += speed
        if keys[pygame.K_UP]:
            playerY -= speed
        if keys[pygame.K_DOWN]:
            playerY += speed

        #Player Boundary Limits
        if playerX < 0:
            playerX = 0
        if playerX > screenX-playerD:
            playerX = screenX-playerD
        if playerY < 0:
            playerY = 0
        if playerY > screenY-50-playerD:
            playerY = screenY-50-playerD

        #Player collide with candy    
        if player.colliderect(candy):
            candyX = 1000
            candyY = 1000
            if speed == 4:
                speed = 8
            elif speed == 2:
                speed = 4

        #Player collide with clouds
        if player.colliderect(cloud1) or player.colliderect(cloud2):
            if speed == 4:
                speed = 2
            elif speed == 8:
                speed = 4

        #Player collide with gift
        if player.colliderect(gift):
            pointCount += 1
            speed = 4
            candyX = random.randint(0,screenX-candyW)
            candyY = random.randint(0,screenY-100-candyH)
            giftX = random.randint(0,screenX-giftW)
            giftY = random.randint(0,screenY-100-giftH)
            fireplaceX = random.randint(0,screenX-fireplaceD)
            fireplaceY = random.randint(0,screenY-100-fireplaceD)
            cloud1X = random.randint(0,screenX-cloudW)
            cloud1Y = random.randint(0,screenY-100-cloudH)
            cloud2X = random.randint(0,screenX-cloudW)
            cloud2Y = random.randint(0,screenY-100-cloudH)

            #Clouds not overlap each other
            while 0 < cloud1X - cloud2X < 100 or 0 < cloud2X - cloud1X < 100:
                cloud1X = random.randint(0,screenX-cloudW)
            while 0 < cloud1Y - cloud2Y < 55 or 0 < cloud2Y - cloud1Y < 55:
                cloud1Y = random.randint(0,screenY-100-cloudH)

            #Gift not overlap with clouds
            while 0 < cloud1X - giftX < 29 or 0 < giftX - cloud1X < 100:
                giftX = random.randint(0,screenX-giftW)
            while 0 < cloud2X - giftX < 29 or 0 < giftX - cloud2X < 100:
                giftX = random.randint(0,screenX-giftW)
            while 0 < cloud1Y - giftY < 34 or 0 < giftY - cloud1Y < 55:
                giftY = random.randint(0,screenY-100-giftH)
            while 0 < cloud2Y - giftY < 34 or 0 < giftY - cloud2Y < 55:
                giftY = random.randint(0,screenY-100-giftH)

            #Player not overlap with clouds
            while 0 < playerX - cloud1X < 100 or 0 < cloud1X - playerX < 75:
                cloud1X = random.randint(0,screenX-cloudW)
            while 0 < playerX - cloud2X < 100 or 0 < cloud2X - playerX < 75:
                cloud2X = random.randint(0,screenX-cloudW)
            while 0 < playerY - cloud1Y < 55 or 0 < cloud1Y - playerY < 75:
                cloud1Y = random.randint(0,screenY-100-cloudH)
            while 0 < playerY - cloud2Y < 55 or 0 < cloud2Y - playerY < 75:
                cloud2Y = random.randint(0,screenY-100-cloudH)
            
            #Player not overlap with gift
            while 0 < playerX - giftX < 29 or 0 < giftX - playerX < 75:
                giftX = random.randint(0,screenX-giftW)
            while 0 < playerY - giftY < 34 or 0 < giftY - playerY < 75:
                giftY = random.randint(0,screenY-100-giftH)

            #Player not overlap with fireplace
            while 0 < playerX - fireplaceX < 40 or 0 < fireplaceX - playerX < 75:
                fireplaceX = random.randint(0,screenX-fireplaceD)
            while 0 < playerY - fireplaceY < 40 or 0 < fireplaceY - playerY < 75:
                fireplaceY = random.randint(0,screenY-50-fireplaceD)

            #Gift not overlap with fireplace
            while 0 < giftX - fireplaceX < 40 or 0 < fireplaceX - giftX < 29:
                giftX = random.randint(0,screenX-giftW)
            while 0 < giftY - fireplaceY < 40 or 0 < fireplaceY - giftY < 34:
                giftY = random.randint(0,screenY-100-giftH)

        #Player collide with fireplace
        if player.colliderect(fireplace):
            speed = 0
            centeredText("You burned to death, you lose!",ComicSansMS2,white)
            pygame.display.update()
            time.sleep(2)
            gameOver = True

        #Timer
        if timer > 0:
            timer -= 1
        if timer == 0 and pointCount < 25:
            centeredText("Time up! You lose!",ComicSansMS2,white)
            pygame.display.update()
            time.sleep(2)
            gameOver = True
        elif timer == 0 and pointCount >= 25:
            centeredText("Congratulations! You win!",ComicSansMS2,white)
            pygame.display.update()
            time.sleep(2)
            gameOver = True            

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    quit()

start()
gameLoop()

