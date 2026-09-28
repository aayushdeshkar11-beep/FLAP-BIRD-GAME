import random
import sys
import pygame   # my code
from pygame.locals import *
pygame.init()

#Global variables
FPS = 32
SCREEN_WIDTH = 289
SCREEN_HEIGHT = 511
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
GROUNDY = SCREEN_HEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'ASSETS/yellowbird-midflap.png'
BACKGROUND = 'ASSETS/background-day.png'
PIPE = 'ASSETS/pipe-green.png'

def welcomeScreen():

    # shows welcome image on screen

    playerx = int(SCREEN_WIDTH / 5)
    playery = int((SCREEN_HEIGHT - GAME_SPRITES['player'].get_height()) / 2)
    messagex = int((SCREEN_WIDTH - GAME_SPRITES['message'].get_width()) / 2)
    messagey = int(SCREEN_HEIGHT * 0.13)
    basex = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
                #  if user press space or up arrow key game starts

            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                screen.blit(GAME_SPRITES['background'], (0, 0))
                screen.blit(GAME_SPRITES['player'], (playerx, playery))
                screen.blit(GAME_SPRITES['message'], (messagex, messagey))
                screen.blit(GAME_SPRITES['base'], (basex,GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score = 0
    playerx = int(SCREEN_WIDTH/5)
    playery = int(SCREEN_HEIGHT/2)
    basex = 0

    #create 2 pipes for bliting onscreen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    #list of upper pipes and lower pipes
    upperPipes = [
        {'x':SCREEN_WIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREEN_WIDTH + 200 + (SCREEN_WIDTH / 2), 'y': newPipe2[0]['y']},

    ]

    lowerPipes = [
        {'x':SCREEN_WIDTH + 200, 'y':newPipe1[1]['y']},
        {'x': SCREEN_WIDTH + 200 + (SCREEN_WIDTH / 2), 'y': newPipe2[1]['y']},

    ]

    pipevelx = -4

    playervely = -9
    playerMaxvely = 10
    playerMinvely = -8
    playerAccvely = 1

    playerFlapAccv = -8 # velocity flapping
    playerFlapped = False # it is true oonly when the bird is flaping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playervely  = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crashtest = iscollide(playerx, playery, upperPipes, lowerPipes)
        if crashtest:
            return

        # check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f'YOUR SCORE IS {score}')
                GAME_SOUNDS['point'].play()

        if playervely < playerMaxvely and not playerFlapped:
            playervely += playerAccvely

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playervely,GROUNDY - playery - playerHeight)

        # moves pipes to left
        for upperpipe , lowerpipe in zip(upperPipes , lowerPipes):
            upperpipe['x'] +=pipevelx
            lowerpipe['x'] +=pipevelx

        # addd a new pipe when the firsst is about the to go to cross the leftmost part of screen
        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])
            
        '''  THIS THE OLD CODE AND THERE ARE SOME FEW MISTAKE SOLVED BY A.I (PARTICUALLRY TALKING ABOUT THIS CODE)
        THE MISTAKE I HAVE DONE IS IN THE DIGITS AND IF UPPER CASE OF LOOP BECAUSE OF THAT THE GAME STUCKS
        AND WE CANNOT PLAY IT AND ONLY THE GAME_SOUND IS COMMING THE PLAYING SCREEN IS NOT VISIBLE 
        <------------------------------------------->
        
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
    upperPipes.pop(0)
    lowerPipes.pop(0)

    screen.blit(GAME_SPRITES['background-day'], (0, 0))
    for upperpipe, lowerpipe in zip(upperPipes, lowerPipes):
        screen.blit(GAME_SPRITES['pipe'][0], (upperpipe['x'], upperpipe['y']))
        screen.blit(GAME_SPRITES['pipe'][1], (lowerpipe['x'], lowerpipe['y']))

    screen.blit(GAME_SPRITES['base'], (basex, GROUNDY))
    screen.blit(GAME_SPRITES['player'], (playerx, playery))

    myDigits = [int(x) for x in list(str(score))]
    width = 0

    for digits in myDigits:
        width += GAME_SPRITES['numbers'][digit].get_width()

    Xoffset = (SCREEN_WIDTH - width) / 2

    for digits in myDigits:
        screen.blit(GAME_SPRITES['numbers'][digits], (Xoffset, SCREEN_HEIGHT*0.12))
        Xoffset += GAME_SPRITES['numbers'][digits].get_width()

    pygame.display.update()
    FPSCLOCK.tick(FPS)
    
    <--------------------------------------------------------------------------------->
        '''
        


        #if the pipe if out of screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        screen.blit(GAME_SPRITES['background'], (0, 0))

        for upperpipe, lowerpipe in zip(upperPipes, lowerPipes):
            screen.blit(GAME_SPRITES['pipe'][0], (upperpipe['x'], upperpipe['y']))
            screen.blit(GAME_SPRITES['pipe'][1], (lowerpipe['x'], lowerpipe['y']))

        screen.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        screen.blit(GAME_SPRITES['player'], (playerx, playery))

        myDigits = [int(x) for x in str(score)]
        width = 0

        for digits in myDigits:
            width += GAME_SPRITES['numbers'][digits].get_width()

        Xoffset = (SCREEN_WIDTH - width) / 2

        for digits in myDigits:
            screen.blit(GAME_SPRITES['numbers'][digits], (Xoffset, SCREEN_HEIGHT * 0.12))
            Xoffset += GAME_SPRITES['numbers'][digits].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def iscollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY - 25 or playery < 0 :
        GAME_SOUNDS['hit'].play()
        return  True

    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (playery < pipeHeight +  pipe['y'] and (abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width())):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    return False

def getRandomPipe():
    """GENERATE POSITIONS OF TWO PIPES FOR BLITTING ONSCREEN
    (ONE BOTTM STARIGHT AND ONE TOP ROTATED)"""

    PipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREEN_HEIGHT / 3
    y2 = offset + random.randrange(0,int(SCREEN_HEIGHT - GAME_SPRITES['base'].get_height()-1.2 * offset))
    pipeX = SCREEN_WIDTH + 10
    y1 = PipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, # lower pipe
        {'x': pipeX, 'y': y2} # upper pipe
    ]
    return pipe


if __name__ == '__main__':
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')
    GAME_SPRITES['numbers'] = (
        pygame.image.load('ASSETS/numbers/0.png').convert_alpha(),
        pygame.image.load('ASSETS/numbers/1.png').convert_alpha(),
        pygame.image.load('ASSETS/numbers/2.png').convert_alpha(),
        pygame.image.load('ASSETS/numbers/3.png').convert_alpha(),
        pygame.image.load('ASSETS/numbers/4.png').convert_alpha(),
        pygame.image.load('ASSETS/numbers/5.png').convert_alpha(),
        pygame.image.load('ASSETS/numbers/6.png').convert_alpha(),
        pygame.image.load('ASSETS/numbers/7.png').convert_alpha(),
        pygame.image.load('ASSETS/numbers/8.png').convert_alpha(),
        pygame.image.load('ASSETS/numbers/9.png').convert_alpha(),

    )

    GAME_SPRITES['message'] = pygame.image.load('ASSETS/message.png').convert_alpha()
    GAME_SPRITES['background-day'] = pygame.image.load('ASSETS/background-day.png').convert_alpha()
    GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load('ASSETS/pipe-green.png').convert_alpha(), 180),
        pygame.image.load('ASSETS/pipe-green.png').convert_alpha()
    )

    # Game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('Sound Efects/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('Sound Efects/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('Sound Efects/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('Sound Efects/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('Sound Efects/wing.wav')

    GAME_SPRITES['background'] = pygame.image.load('ASSETS/background-day.png').convert_alpha()
    GAME_SPRITES['player'] = pygame.image.load('ASSETS/yellowbird-midflap.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('ASSETS/base.png').convert_alpha()


    while True:
        welcomeScreen() #shows welcomescreen
        mainGame() # main game function
        
        
        
        ''' IN THIS FILE I HAVE ALSO PROVIDED THE UP FLY AND DOWN FLY BIRD IMAGE HOW CAN I
            IMPLEMENT IN THE WHILE LOOP IF YOU KNOW JUST IMPLEMENT IT AND TELL THE LOGIC IN README FILE
            SO THAT IT IS HELPFUL 
        
        ''' 