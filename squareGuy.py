import pygame
import random

pygame.init()

#info = pygame.display.Info()
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Cool Square Guy")

# TimeKeeping

clock = pygame.time.Clock()
elapsedTime = 0.0
dt = clock.tick(60) / 1000

# CLASSES
# Menu
# Button attributes
class button:
    def __init__(self, x, y, color, w, h):
        self.x, self.y = x, y
        self.width, self.height = w, h
        self.color = color
    
# Powerup attributes
class powerUp:
    def __init__(self, sz, colA, colB, colC):
        self.puSz = sz
        self.Col = (colA, colB, colC)

# Character attributes
class character:
    def __init__(self, sz, colA, colB, colC):
        self.squareSz = sz
        self.cx = colA
        self.cy = colB
        self.cz = colC

        self.Col = (self.cx, self.cy, self.cz)
        self.Flight = False
        self.Vx = 8
        self.Vy = 0
        self.VyFlight = self.Vx

        self.floorCt = 0
        self.flightCt = 0

def drawCharacter(myCharacter):
    pygame.draw.rect(
        screen,
        myCharacter.Col,
        (xPos - myCharacter.squareSz // 2,  # center it horizontally
        yPos - myCharacter.squareSz // 2,  # center it vertically
        myCharacter.squareSz,
        myCharacter.squareSz)
    )

def printPos():
    print("x: ", xPos, " y: ", yPos)

def spawnPowerup():
    pu = powerUp(10,
                 random.randint(50,255),
                 random.randint(50,255),
                 random.randint(50,255))
    pu.x = random.randint(10, width-10)
    pu.y = random.randint(10, height-10)
    return pu

def drawPowerUps(powerUps):
    for pu in powerUps:
        pygame.draw.rect(
            screen,
            pu.Col,
            (
                pu.x - pu.puSz//2,
                pu.y - pu.puSz//2,
                pu.puSz,
                pu.puSz
            )
        )

# menu

menuRunning = True
menuBGCol = (0,133,198)
menuButtonCol = (6,190,220)
menuButtonOutlineCol = (0,214,255)

buttonWidth, buttonHeight = 200, 50

while menuRunning:
    screen.fill(menuBGCol)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menuRunning = False
            menuSaidNo = True # If we quit on menu screen, makes sure that happens
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print("enterpress")
                menuSaidNo = False
                menuRunning = False
                continue


# game set up

# set up square guy

myCharacter = character(50, 20, 20, 20)

# Constants and timer set up for powerups

SPAWN_INTERVAL = 1_000 # ms
lastSpawn = pygame.time.get_ticks()
powerUps = []

g = 0.2
spawnXPos = width // 2
spawnYPos = 720 - myCharacter.squareSz // 2

# spawnpoint

xPos = spawnXPos
yPos = spawnYPos

ground = height - myCharacter.squareSz // 2
ceiling = myCharacter.squareSz // 2

gameRunning = True

pygame.display.update()

while gameRunning and not menuSaidNo:
    dt = clock.tick(120)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False
        
        elif event.type == pygame.KEYDOWN:

            # ESCAPE PRESSED, QUIT GAME

            if event.key == pygame.K_ESCAPE:
                print("GAME CLOSED")
                gameRunning = False

            # JUMP MECHANIC
                
            elif event.key == pygame.K_w and yPos == ground and not myCharacter.Flight:
                myCharacter.Vy = -10
            
            # RESET

            elif event.key == pygame.K_r:   
                xPos = spawnXPos
                yPos = spawnYPos
                myCharacter.flightCt = 0
                myCharacter.Flight = False
                myCharacter.Col = (myCharacter.cx, myCharacter.cy, myCharacter.cz)
                powerUps.clear()

            elif event.key == pygame.K_f:
                myCharacter.flightCt += 1

                if myCharacter.flightCt % 2 == 0:
                    myCharacter.Flight = False
                    myCharacter.Col = (myCharacter.cx, myCharacter.cy, myCharacter.cz)

                else:
                    myCharacter.Flight = True
                    myCharacter.Col = (0, 250, 0)

    keys = pygame.key.get_pressed()

    # Horizontal Controls

    if keys[pygame.K_a] and xPos > 0:
        xPos -= myCharacter.Vx
        printPos()

    if keys[pygame.K_d] and xPos < width:
        xPos += myCharacter.Vx
        printPos()

    # Vertical Controls
    # If flight is OFF

    if not myCharacter.Flight:
        myCharacter.Vy += g
        yPos += myCharacter.Vy

        if yPos > ground:
            yPos = ground
            myCharacter.Vy = 0

        if yPos < ceiling:
            yPos = ceiling
            myCharacter.Vy = 0

    # If flight is ON

    else:
        myCharacter.Vy = 0  # Reset to 0 so vertical speed doesn't get maintained in flight

        if keys[pygame.K_w]:
            yPos -= myCharacter.VyFlight
            printPos()
        if keys[pygame.K_s]:
            yPos += myCharacter.VyFlight
            printPos()
    
    # Update frame by drawing character and powerups
    screen.fill((0,0,0))
    now = pygame.time.get_ticks()
    # only spawn if interval passed *and* fewer than 10 exist
    if now - lastSpawn >= SPAWN_INTERVAL and len(powerUps) < 10:
        powerUps.append(spawnPowerup())
        lastSpawn = now

    drawCharacter(myCharacter)
    drawPowerUps(powerUps)      

    pygame.display.flip() # Update the frame / display

    
pygame.quit()

# TODO:
"""
Add start page
Add escape menu page
Implement powerups
Implement character dash ability
Turn the action of drawing character, powerups, platforms in the future into FUNCTIONS
"""
"""
While you're new at this
git add .
git commit -m "msg"
git push
"""