#To do list:
# Make display size dynamic/Graphical overhaul (This is a V2 level change. Create new file.)

import pygame, sys, random, time, math
from pygame.locals import *

# Set up pygame.
pygame.init()
mainClock = pygame.time.Clock()

# Set up window.
windowSurface = pygame.display.set_mode((605, 855), 0, 32)
pygame.display.set_caption('Tetris')

# Setup up the colors.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LONG = (43,213,255)
SQUARE = (240, 228, 0)
SBLOCK = (57, 140, 38)
ZBLOCK = (235, 0, 0)
TBLOCK = (122, 0, 222)
LBLOCK = (255, 136, 0)
JBLOCK = (0, 10, 201)

display = []
settled = []
positions = []
testPositions = []
testRotation = 0
testX = 0
testY = 0
gameSpeed = 120
tic = gameSpeed
nextBlock = False
currentBlock = random.randint(1, 7)
nextBlock1 = random.randint(1, 7)
nextBlock2 = random.randint(1, 7)
nextBlock3 = random.randint(1, 7)
holdBlock = 0
holdDelay = False
xCurrent = 3
yCurrent = 2
rotation = 0
inputLeft = False
inputRight = False
inputUp = False
inputDown = False
inputE = False
inputQ = False
inputSpace = False
inputLeftHold = 0
inputRightHold = 0
gameover = False
delayLR = 0
delaySlam = 0
delayRotate = 0
delayDown = 0
clear = 0
clearCount = 0
totalLineClears = 0
slide = gameSpeed/2
move = True
highY = 24
score = 0
level = 0
temp = 0
rotated = 0
paused = False
downCount = 0

# Set up the fonts.
giantFont = pygame.font.Font('ARCADECLASSIC.ttf', 120)
bigFont = pygame.font.Font('ARCADECLASSIC.ttf', 60)
smallFont = pygame.font.Font('ARCADECLASSIC.ttf', 52)
smolFont = pygame.font.Font('ARCADECLASSIC.ttf', 42)

# Set up the text
# HOLD
holdText = bigFont.render('Hold', True, WHITE)
holdRect = holdText.get_rect()
holdRect.centerx = 512
holdRect.centery = 105
# UP NEXT
nextText = smallFont.render('Up Next', True, WHITE)
nextRect = nextText.get_rect()
nextRect.centerx = 512
nextRect.centery = 305
# Score Label
labelText = smallFont.render('Score', True, WHITE)
labelRect = labelText.get_rect()
labelRect.centerx = 510
labelRect.centery = 27
# Score
scoreText = smolFont.render(str(score), True, WHITE)
scoreRect = scoreText.get_rect()
scoreRect.centerx = 510
scoreRect.centery = 55
# Level Label
labelText1 = smallFont.render("Level", True, WHITE)
labelRect1 = labelText1.get_rect()
labelRect1.left = 5
labelRect1.top = 805
# Level Number
levelText = smallFont.render(str(level), True, WHITE)
levelRect = levelText.get_rect()
levelRect.left = 160
levelRect.top = 805
# Label Total Lines
labelText2 = smallFont.render("Clears", True, WHITE)
labelRect2 = labelText2.get_rect()
labelRect2.left = 275
labelRect2.top = 805
# Lines
linesText = smallFont.render(str(totalLineClears), True, WHITE)
linesRect = linesText.get_rect()
linesRect.left = 250
linesRect.top = 805
# Paused
pauseText = giantFont.render("Paused", True, WHITE)
pauseRect = pauseText.get_rect()
pauseRect.centerx = 302
pauseRect.centery = 402
# Paused instructions
infoText1 = smallFont.render("Press ESC to resume", True, WHITE)
infoRect1 = infoText1.get_rect()
infoRect1.centerx = 302
infoRect1.centery = 465
infoText2 = smallFont.render("Press E to exit", True, WHITE)
infoRect2 = infoText2.get_rect()
infoRect2.centerx = 302
infoRect2.centery = 502
# Gameover
endText = giantFont.render('GAMEOVER', True, WHITE)
endRect = endText.get_rect()
endRect.centerx = 302
endRect.centery = 402

# Draw the white background
windowSurface.fill(BLACK)

# Set up the music
fallSound = pygame.mixer.Sound('SFX_PieceFall.ogg')
slamSound = pygame.mixer.Sound('SFX_PieceHardDrop.wav')
holdSound = pygame.mixer.Sound('SFX_PieceHold.ogg')
moveSound = pygame.mixer.Sound('SFX_PieceMoveLR.ogg')
rotateFailSound = pygame.mixer.Sound('SFX_PieceRotateFail.ogg')
rotateSound = pygame.mixer.Sound('SFX_PieceRotateLR.ogg')
softDropSound = pygame.mixer.Sound('SFX_PieceSoftDrop.ogg')
touchDownSound = pygame.mixer.Sound('SFX_PieceTouchDown.ogg')
singleClearSound = pygame.mixer.Sound('SFX_SpecialLineClearSingle.ogg')
doubleClearSound = pygame.mixer.Sound('SFX_SpecialLineClearDouble.ogg')
tripleClearSound = pygame.mixer.Sound('SFX_SpecialLineClearTriple.ogg')
tetrisSound = pygame.mixer.Sound('SFX_SpecialTetris.ogg')
pygame.mixer.music.load('Tetris_Theme.mid')
musicPlaying = False
            
for i in range(4):
    positions.append([])
    testPositions.append([])
    for j in range(2):
        positions[i].append(0)
        testPositions[i].append(0)

for y in range(24):
        display.append([])
        settled.append([])
        for x in range(10):
            display[y].append(0)
            settled[y].append(0)

# Defines each position for every block
def getPosition(block, rotation, x, y):
    # Long Piece
    if block == 1:
        if rotation == 0:
            return([[x, y], [x, y - 1], [x, y + 1], [x, y + 2]])
        elif rotation == 90:
            return([[x, y], [x - 1, y], [x + 1, y], [x + 2, y]])
        elif rotation == 180:
            return([[x, y], [x, y - 1], [x, y + 1], [x, y + 2]])
        elif rotation == 270:
            return([[x, y], [x + 1, y], [x - 1, y], [x - 2, y]])
    # Square Piece
    elif block == 2:
        return([[x, y], [x + 1, y], [x, y + 1], [x + 1, y + 1]])
    # S Block
    elif block == 3:
        if rotation == 0 or rotation == 180:
            return([[x, y], [x + 1, y], [x, y + 1], [x - 1, y + 1]])
        elif rotation == 90 or rotation == 270:
            return([[x, y], [x, y - 1], [x + 1, y], [x + 1, y + 1]])
    # Z Block
    elif block == 4:
        if rotation == 0 or rotation == 180:
            return([[x, y], [x - 1, y], [x, y + 1], [x + 1, y + 1]])
        elif rotation == 90 or rotation == 270:
            return([[x, y], [x - 1, y], [x, y - 1], [x - 1, y + 1]])
    # T Block
    elif block == 5:
        if rotation == 0:
            return([[x, y], [x - 1, y], [x + 1, y], [x, y - 1]])
        elif rotation == 90:
            return([[x, y], [x, y - 1], [x + 1, y], [x, y + 1]])
        elif rotation == 180:
            return([[x, y], [x - 1, y], [x, y + 1], [x + 1, y]])
        elif rotation == 270:
            return([[x, y], [x - 1, y], [x, y - 1], [x, y + 1]])
    # L Block
    elif block == 6:
        if rotation == 0:
            return([[x, y], [x, y - 2], [x, y - 1], [x + 1, y]])
        elif rotation == 90:
            return([[x, y], [x, y + 1], [x + 1, y], [x + 2, y]])
        elif rotation == 180:
            return([[x, y], [x - 1, y], [x, y + 1], [x, y + 2]])
        elif rotation == 270:
            return([[x, y], [x - 2, y], [x - 1, y], [x, y -1]])
    # J Block
    elif block == 7:
        if rotation == 0:
            return([[x, y], [x, y - 2], [x, y - 1], [x - 1, y]])
        elif rotation == 90:
            return([[x, y], [x, y - 1], [x + 1, y], [x + 2, y]])
        elif rotation == 180:
            return([[x, y], [x + 1, y], [x, y + 1], [x, y + 2]])
        elif rotation == 270:
            return([[x, y], [x - 2, y], [x - 1, y], [x, y + 1]])
            

def drawDisplay():
    if paused:
        windowSurface.blit(pauseText, pauseRect)
        windowSurface.blit(infoText1, infoRect1)
        windowSurface.blit(infoText2, infoRect2)
    else:
        # Division Lines
        pygame.draw.rect(windowSurface, WHITE, (405, 5, 5, 800))
        pygame.draw.rect(windowSurface, WHITE, (5, 805, 595, 5))
        # Text Box
        pygame.draw.rect(windowSurface, WHITE, (415, 5, 185, 72))
        pygame.draw.rect(windowSurface, BLACK, (420, 10, 175, 62))
        scoreText = smolFont.render(str(score), True, WHITE)
        scoreRect = scoreText.get_rect()
        scoreRect.centerx = 510
        scoreRect.centery = 55
        windowSurface.blit(labelText, labelRect)
        windowSurface.blit(scoreText, scoreRect)
        # Level Display
        levelText = smallFont.render(str(level), True, WHITE)
        levelRect = levelText.get_rect()
        levelRect.left = 155
        levelRect.top = 805
        windowSurface.blit(levelText, levelRect)
        # Level Text
        windowSurface.blit(labelText1, labelRect1)
        # Lines Cleared Text
        windowSurface.blit(labelText2, labelRect2)
        # Line Cleared Display
        linesText = smallFont.render(str(totalLineClears), True, WHITE)
        linesRect = linesText.get_rect()
        linesRect.left = 460
        linesRect.top = 805
        windowSurface.blit(linesText, linesRect)
        # HOLD
        windowSurface.blit(holdText, holdRect)
        pygame.draw.rect(windowSurface, WHITE, (433, 125, 150, 150))
        pygame.draw.rect(windowSurface, BLACK, (438, 130, 140, 140))
        # HOLD Block
        if holdBlock == 1:
            pygame.draw.rect(windowSurface, LONG, (495, 140, 30, 120))
        elif holdBlock == 2:
            pygame.draw.rect(windowSurface, SQUARE, (480, 170, 60, 60))
        elif holdBlock == 3:
            pygame.draw.rect(windowSurface, SBLOCK, (495, 170, 60, 30))
            pygame.draw.rect(windowSurface, SBLOCK, (465, 200, 60, 30))
        elif holdBlock == 4:
            pygame.draw.rect(windowSurface, ZBLOCK, (465, 170, 60, 30))
            pygame.draw.rect(windowSurface, ZBLOCK, (495, 200, 60, 30))
        elif holdBlock == 5:
            pygame.draw.rect(windowSurface, TBLOCK, (495, 170, 30, 30))
            pygame.draw.rect(windowSurface, TBLOCK, (465, 200, 90, 30))
        elif holdBlock == 6:
            pygame.draw.rect(windowSurface, LBLOCK, (480, 155, 30, 90))
            pygame.draw.rect(windowSurface, LBLOCK, (510, 215, 30, 30))
        elif holdBlock == 7:
            pygame.draw.rect(windowSurface, JBLOCK, (510, 155, 30, 90))
            pygame.draw.rect(windowSurface, JBLOCK, (480, 215, 30, 30))
        # NEXT1
        windowSurface.blit(nextText, nextRect)
        pygame.draw.rect(windowSurface, WHITE, (433, 325, 150, 150))
        pygame.draw.rect(windowSurface, BLACK, (438, 330, 140, 140))
        # NEXT Block
        if nextBlock1 == 1:
            pygame.draw.rect(windowSurface, LONG, (495, 340, 30, 120))
        elif nextBlock1 == 2:
            pygame.draw.rect(windowSurface, SQUARE, (480, 370, 60, 60))
        elif nextBlock1 == 3:
            pygame.draw.rect(windowSurface, SBLOCK, (495, 370, 60, 30))
            pygame.draw.rect(windowSurface, SBLOCK, (465, 400, 60, 30))
        elif nextBlock1 == 4:
            pygame.draw.rect(windowSurface, ZBLOCK, (465, 370, 60, 30))
            pygame.draw.rect(windowSurface, ZBLOCK, (495, 400, 60, 30))
        elif nextBlock1 == 5:
            pygame.draw.rect(windowSurface, TBLOCK, (495, 370, 30, 30))
            pygame.draw.rect(windowSurface, TBLOCK, (465, 400, 90, 30))
        elif nextBlock1 == 6:
            pygame.draw.rect(windowSurface, LBLOCK, (480, 355, 30, 90))
            pygame.draw.rect(windowSurface, LBLOCK, (510, 415, 30, 30))
        elif nextBlock1 == 7:
            pygame.draw.rect(windowSurface, JBLOCK, (510, 355, 30, 90))
            pygame.draw.rect(windowSurface, JBLOCK, (480, 415, 30, 30))
        # NEXT2
        pygame.draw.rect(windowSurface, WHITE, (433, 480, 150, 150))
        pygame.draw.rect(windowSurface, BLACK, (438, 485, 140, 140))
        # NEXT Block2
        if nextBlock2 == 1:
            pygame.draw.rect(windowSurface, LONG, (495, 495, 30, 120))
        elif nextBlock2 == 2:
            pygame.draw.rect(windowSurface, SQUARE, (480, 525, 60, 60))
        elif nextBlock2 == 3:
            pygame.draw.rect(windowSurface, SBLOCK, (495, 525, 60, 30))
            pygame.draw.rect(windowSurface, SBLOCK, (465, 555, 60, 30))
        elif nextBlock2 == 4:
            pygame.draw.rect(windowSurface, ZBLOCK, (465, 525, 60, 30))
            pygame.draw.rect(windowSurface, ZBLOCK, (495, 555, 60, 30))
        elif nextBlock2 == 5:
            pygame.draw.rect(windowSurface, TBLOCK, (495, 525, 30, 30))
            pygame.draw.rect(windowSurface, TBLOCK, (465, 555, 90, 30))
        elif nextBlock2 == 6:
            pygame.draw.rect(windowSurface, LBLOCK, (480, 510, 30, 90))
            pygame.draw.rect(windowSurface, LBLOCK, (510, 570, 30, 30))
        elif nextBlock2 == 7:
            pygame.draw.rect(windowSurface, JBLOCK, (510, 510, 30, 90))
            pygame.draw.rect(windowSurface, JBLOCK, (480, 570, 30, 30))
        # NEXT3
        pygame.draw.rect(windowSurface, WHITE, (433, 635, 150, 150))
        pygame.draw.rect(windowSurface, BLACK, (438, 640, 140, 140))
        # NEXT Block3
        if nextBlock3 == 1:
            pygame.draw.rect(windowSurface, LONG, (495, 650, 30, 120))
        elif nextBlock3 == 2:
            pygame.draw.rect(windowSurface, SQUARE, (480, 680, 60, 60))
        elif nextBlock3 == 3:
            pygame.draw.rect(windowSurface, SBLOCK, (495, 680, 60, 30))
            pygame.draw.rect(windowSurface, SBLOCK, (465, 710, 60, 30))
        elif nextBlock3 == 4:
            pygame.draw.rect(windowSurface, ZBLOCK, (465, 680, 60, 30))
            pygame.draw.rect(windowSurface, ZBLOCK, (495, 710, 60, 30))
        elif nextBlock3 == 5:
            pygame.draw.rect(windowSurface, TBLOCK, (495, 680, 30, 30))
            pygame.draw.rect(windowSurface, TBLOCK, (465, 710, 90, 30))
        elif nextBlock3 == 6:
            pygame.draw.rect(windowSurface, LBLOCK, (480, 665, 30, 90))
            pygame.draw.rect(windowSurface, LBLOCK, (510, 725, 30, 30))
        elif nextBlock3 == 7:
            pygame.draw.rect(windowSurface, JBLOCK, (510, 665, 30, 90))
            pygame.draw.rect(windowSurface, JBLOCK, (480, 725, 30, 30))
        # Gameboard
        for y in range(20):
            for x in range(10):
                d = display[y + 4][x]
                xmove = x * 40
                ymove = y * 40
                if d == 1:
                    pygame.draw.rect(windowSurface, LONG, (5 + xmove, 5 + ymove, 35, 35))
                elif d == 2:
                    pygame.draw.rect(windowSurface, SQUARE, (5 + xmove, 5 + ymove, 35, 35))
                elif d == 3:
                    pygame.draw.rect(windowSurface, SBLOCK, (5 + xmove, 5 + ymove, 35, 35))
                elif d == 4:
                    pygame.draw.rect(windowSurface, ZBLOCK, (5 + xmove, 5 + ymove, 35, 35))
                elif d == 5:
                    pygame.draw.rect(windowSurface, TBLOCK, (5 + xmove, 5 + ymove, 35, 35))
                elif d == 6:
                    pygame.draw.rect(windowSurface, LBLOCK, (5 + xmove, 5 + ymove, 35, 35))
                elif d == 7:
                    pygame.draw.rect(windowSurface, JBLOCK, (5 + xmove, 5 + ymove, 35, 35))
        # Displays gameover Text
        if gameover == True:
            windowSurface.blit(endText, endRect)
    # Draws screen
    pygame.display.update()
    # Empties Gameboard Array
    for y in range(24):
        for x in range(10):
            display[y][x] = 0

# Run the game loop.
while gameover == False:
    # Haults the loop while paused
    while paused:
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    paused = False
                if event.key == K_e:
                    pygame.quit()
                    sys.exit()
    #Refreshes the screen by filling it with black and then load the display array with settled.
    windowSurface.fill(BLACK)
    positions = getPosition(currentBlock, rotation, xCurrent, yCurrent)
    for y in range(24):
        for x in range(10):
            display[y][x] = settled[y][x]
    # Gets the player keyboard inputs.
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_LEFT or event.key == K_a:
                inputLeft = True
            if event.key == K_RIGHT or event.key == K_d:
                inputRight = True
                inputRightHold += 1
            if event.key == K_UP or event.key == K_w:
                inputUp = True
            if event.key == K_DOWN or event.key == K_s:
                inputDown = True
            if event.key == K_e:
                inputE = True
            if event.key == K_q:
                inputQ = True
            if event.key == K_SPACE or event.key == K_LSHIFT:
                inputSpace = True
                    
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                if paused == False:
                    paused = True
            if event.key == K_LEFT or event.key == K_a:
                inputLeft = False
                inputLeftHold = 0
            if event.key == K_RIGHT or event.key == K_d:
                inputRight = False
                inputRightHold = 0
            if event.key == K_UP or event.key == K_w:
                inputUp = False
            if event.key == K_DOWN or event.key == K_s:
                inputDown = False
            if event.key == K_e:
                inputE = False
            if event.key == K_q:
                inputQ = False
            if event.key == K_SPACE or event.key == K_LSHIFT:
                inputSpace = False
            if event.key == K_m:
                if musicPlaying:
                    pygame.mixer.music.stop()
                else:
                    pygame.mixer.music.play(-1, 0.0)
                musicPlaying = not musicPlaying
        # Listens for quit and ends the game.
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    # Changes the block x and y position based on the input.
    if inputLeft and xCurrent > 0 and delayLR == 0 and not inputRight:
        move = True
        testPositions = getPosition(currentBlock, rotation, xCurrent - 1, yCurrent)
        for i in range(4):
            if testPositions[i][0] < 0 or settled[testPositions[i][1]][testPositions[i][0]] > 0:
                move = False
                break
        if move:
            positions = testPositions
            xCurrent -= 1
            if inputLeftHold >= 16:
                delayLR = 3
            else:
                delayLR = 8
            for i in range(4):
                if positions[i][1] == 23 or settled[positions[i][1] + 1][positions[i][0]] > 0:
                    tic += slide
                    slide = math.floor(slide/2)
            if musicPlaying:
                moveSound.play()
    if inputRight and xCurrent < 9 and delayLR == 0 and not inputLeft:
        move = True
        testPositions = getPosition(currentBlock, rotation, xCurrent + 1, yCurrent)
        for i in range(4):
            if testPositions[i][0] > 9 or settled[testPositions[i][1]][testPositions[i][0]] > 0:
                move = False
                break
        if move:
            positions = testPositions
            xCurrent += 1
            if inputRightHold >= 16:
                delayLR = 3
            else:
                delayLR = 8
            for i in range(4):
                if positions[i][1] == 23 or settled[positions[i][1] + 1][positions[i][0]] > 0:
                    tic += slide
                    slide = math.floor(slide/2)
            if musicPlaying:
                moveSound.play()
    if inputDown and delayDown == 0:
        move = True
        testPositions = getPosition(currentBlock, rotation, xCurrent, yCurrent + 1)
        for i in range(4):
            if testPositions[i][1] > 23 or settled[testPositions[i][1]][testPositions[i][0]] > 0:
                move = False
                break
        if move:
            positions = testPositions
            yCurrent += 1
            delayDown = 4
        else:
            if downCount == 16:
                for i in range(4):
                    settled[positions[i][1]][positions[i][0]] = currentBlock
                nextBlock = True
                delayDown = 4
                if musicPlaying:
                    softDropSound.play()
                downCount = 0
            else:
                downCount += 1
        tic = gameSpeed
        slide = math.ceil(gameSpeed/2)
    if inputUp and delaySlam == 0:
        highY = 24
        for y in range(23, yCurrent, -1):
            testPositions = getPosition(currentBlock, rotation, xCurrent, y)
            for i in range(4):
                if testPositions[i][1] > 23 or settled[testPositions[i][1]][testPositions[i][0]] > 0:
                    highY = y
        testPositions = getPosition(currentBlock, rotation, xCurrent, highY - 1)
        for j in range(4):
            settled[testPositions[j][1]][testPositions[j][0]] = currentBlock
        nextBlock = True
        delayDown = 4
        slide = math.ceil(gameSpeed/2)
        tic = gameSpeed
        if musicPlaying:
            slamSound.play()
        delaySlam = 20
    if (inputE or inputQ) and delayRotate == 0:
        if inputE:
            if rotation == 270:
                testRotation = 0
            else:
                testRotation = rotation + 90
        elif inputQ:
            if rotation == 0:
                testRotation = 270
            else:
                testRotation = rotation - 90
        testX = xCurrent
        testY = yCurrent
        while rotated < 4:
            move = True
            rotated = 0
            testPositions = getPosition(currentBlock, testRotation, testX, testY)
            for i in range(4):
                if testPositions[i][1] > 23:
                    testY -= testPositions[i][1] - 23
                    break
                elif testX > 7 and testPositions[i][0] > 9:
                    testX -= testPositions[i][0] - 9
                    break
                elif testX < 2 and testPositions[i][0] < 0:
                    testX += testPositions[i][0] * -1
                    break
                elif settled[testPositions[i][1]][testPositions[i][0]] > 0:
                    move = False
                rotated += 1
        rotated = 0                        
        if move:
            positions = testPositions
            rotation =testRotation
            xCurrent = testX
            yCurrent = testY
            for i in range(4):
                if positions[i][1] == 23 or settled[positions[i][1] + 1][positions[i][0]] > 0:
                    tic += slide
                    slide = math.floor(slide/2)
            if musicPlaying:
                rotateSound.play()
            delayRotate = 16
    if inputSpace and holdDelay == False:
        if holdBlock == 0:
            holdBlock = currentBlock
            currentBlock = nextBlock1
            nextBlock1 = nextBlock2
            nextBlock2 = nextBlock3
            nextBlock3 = random.randint(1, 7)
            nextBlock = False
            yCurrent = 2
            xCurrent = 4
            tic = gameSpeed
        else:
            temp = currentBlock
            currentBlock = holdBlock
            holdBlock = temp
            yCurrent = 2
            xCurrent = 4
            tic = gameSpeed
        holdDelay = True

    # Count gravity.
    if tic <= 0:
        move = True
        testPositions = getPosition(currentBlock, rotation, xCurrent, yCurrent + 1)
        for i in range(4):
            if testPositions[i][1] > 23 or settled[testPositions[i][1]][testPositions[i][0]] > 0:
                move = False
                break
        if move:
            positions = testPositions
            yCurrent += 1
        else:
            for i in range(4):
                settled[positions[i][1]][positions[i][0]] = currentBlock
            settled[yCurrent][xCurrent] = currentBlock
            nextBlock = True
            if musicPlaying:
                touchDownSound.play()
        tic = gameSpeed
        slide = math.ceil(gameSpeed/2)
    else:
        tic -= 1
    # Draws the current piece on the screen
    for i in range(4):
        display[positions[i][1]][positions[i][0]] = currentBlock
    # Checks to seen if the player made a complete line
    for y in range(24):
        for x in range(10):
            if settled[y][x] > 0:
                clear += 1
        if clear == 10:
            for a in range(y, 1, -1):
                for b in range(10):
                    settled[a][b] = settled[a-1][b]
            clearCount += 1
        clear = 0
    # Plays the corrent sound for the amount of clears
    if clearCount == 1:
        score += 40 * level
        if musicPlaying:
            singleClearSound.play()
    if clearCount == 2:
        score += 100 * level	
        if musicPlaying:
            doubleClearSound.play()
    if clearCount == 3:
        score += 300 * level
        if musicPlaying:
            tripleClearSound.play()
    if clearCount == 4:
        score += 1200 * level
        if musicPlaying:
            tetrisSound.play()
    totalLineClears += clearCount
    clearCount = 0
    
    if totalLineClears < 101:
        level = math.floor(totalLineClears / 10)
    elif totalLineClears < 251:
        level = math.floor((totalLineClears + 50) / 15)
    elif totalLineClears < 451:
        level = math.floor((totalLineClears + 150) / 20)
    else:
        level = 29
    gameSpeed = round(120 * .874916 ** (level))

    # Finds out if you've lost
    for y in range(4):
        for x in range(10):
            if settled[y][x] > 0:
                gameover = True

    # Decrements the delay variables for various inputs
    if delayLR > 0:
        delayLR -= 1
    if delaySlam > 0:
        delaySlam -= 1
    if delayRotate > 0:
        delayRotate -= 1
    if delayDown > 0:
        delayDown -= 1
    # Held Button Logic
    if inputLeft:
        inputLeftHold += 1
    if inputRight:
        inputRightHold += 1


    drawDisplay()
    if nextBlock == True:
        currentBlock = nextBlock1
        nextBlock1 = nextBlock2
        nextBlock2 = nextBlock3
        nextBlock3 = random.randint(1, 7)
        nextBlock = False
        yCurrent = 2
        xCurrent = 4
        tic = gameSpeed
        rotaion = 0
        holdDelay = False

    mainClock.tick(120)

print("End")

while True:
    for event in pygame.event.get():
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
    mainClock.tick(30)