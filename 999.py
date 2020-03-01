import pygame
import random
import sys
from pygame.locals import *


WWIDTH = 600 #размер поля ширина
WHEIGHT = 600 # размер поля высота
OSPEED = 5 # скорость открыти/закрытия ячеек
BOXSIZE = 50 # размер ячеек
PROMSIZE = 10 # расстояние между ячеек
BWIDTH = 6 # линии ячеек
BHEIGHT = 6 # колонки ячеек
FPS = 40 # скорость работы программы


WHITE = (255, 255, 255)
RED = (255,   0,   0)
GREEN = (0, 255,   0)
BLUE = (0,   0, 255)
YELLOW = (255, 255,   0)
ORANGE = (255, 128,   0)
PURPLE = (255,   0, 255)
CYAN = (0, 255, 255)
GRAY = (100, 100, 100)


ROUND = 'round'
SQUARE = 'square'
ROMB = 'romb'
OVAL = 'oval'

COLORS = (RED, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
SHAPES = (ROUND, SQUARE, ROMB, OVAL)

XC = int((WWIDTH - (BWIDTH * (BOXSIZE + PROMSIZE))) / 2)
YC = int((WHEIGHT - (BHEIGHT * (BOXSIZE + PROMSIZE))) / 2)

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WWIDTH, WHEIGHT))
    mousex = 0 
    mousey = 0 
    pygame.display.set_caption('КАЗИНО 777')
    mainBoard = RandomBoard()
    rBoxes = GRB(False)
    FS = None
    DISPLAYSURF.fill(GREEN)
    startGame(mainBoard)
    while True: 
        mouseClicked = False
        DISPLAYSURF.fill(GREEN) 
        drawBoard(mainBoard, rBoxes)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
        boxx, boxy = GBP(mousex, mousey)
        if boxx != None and boxy != None:
            if not rBoxes[boxx][boxy]:
                HB(boxx, boxy)
            if not rBoxes[boxx][boxy] and mouseClicked:
                RBA(mainBoard, [(boxx, boxy)])
                rBoxes[boxx][boxy] = True 
                if FS == None: 
                    FS = (boxx, boxy)
                else: 
                    icon1shape, icon1color = GSC(mainBoard, FS[0], FS[1])
                    icon2shape, icon2color = GSC(mainBoard, boxx, boxy)
                    if icon1shape != icon2shape or icon1color != icon2color:
                        pygame.time.wait(1000) 
                        CBA(mainBoard, [(FS[0], FS[1]), (boxx, boxy)])
                        rBoxes[FS[0]][FS[1]] = False
                        rBoxes[boxx][boxy] = False
                    elif Win(rBoxes):
                        gameWin(mainBoard)
                        pygame.time.wait(10)
                        mainBoard = RandomBoard()
                        rBoxes = GRB(False)
                        drawBoard(mainBoard, rBoxes)
                        pygame.display.update()
                        pygame.time.wait(1000)
                        startGame(mainBoard)
                    FS = None         
        pygame.display.update()
        FPSCLOCK.tick(FPS)
def GRB(val):
    rBoxes = []
    for i in range(BWIDTH):
        rBoxes.append([val] * BHEIGHT)
    return rBoxes
def RandomBoard():
    icons = []
    for color in COLORS:
        for shape in SHAPES:
            icons.append( (shape, color) )
    random.shuffle(icons) 
    numIconsUsed = int(BWIDTH * BHEIGHT / 2) 
    icons = icons[:numIconsUsed] * 2 
    random.shuffle(icons)
    board = []
    for x in range(BWIDTH):
        column = []
        for y in range(BHEIGHT):
            column.append(icons[0])
            del icons[0] 
        board.append(column)
    return board
def splitIn(groupSize, theList):
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result
def LTB(boxx, boxy):
    left = boxx * (BOXSIZE + PROMSIZE) + XC
    top = boxy * (BOXSIZE + PROMSIZE) + YC
    return (left, top)
def GBP(x, y):
    for boxx in range(BWIDTH):
        for boxy in range(BHEIGHT):
            left, top = LTB(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)
def drawIcon(shape, color, boxx, boxy):
    quarter = int(BOXSIZE * 0.25) 
    half =    int(BOXSIZE * 0.5)  
    left, top = LTB(boxx, boxy) 
    if shape == ROUND:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
    elif shape == ROMB:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BOXSIZE - 1, top + half), (left + half, top + BOXSIZE - 1), (left, top + half)))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half))
def GSC(board, boxx, boxy):
    return board[boxx][boxy][0], board[boxx][boxy][1]
def DBC(board, boxes, cov):
    for box in boxes:
        left, top = LTB(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, GREEN, (left, top, BOXSIZE, BOXSIZE))
        shape, color = GSC(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if cov > 0:
            pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, cov, BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)
def RBA(board, BTR):
    for cov in range(BOXSIZE, (-OSPEED) - 1, -OSPEED):
        DBC(board, BTR, cov)
def CBA(board, BTC):
    for cov in range(0, BOXSIZE + OSPEED, OSPEED):
        DBC(board, BTC, cov)
def drawBoard(board, rev):
    for boxx in range(BWIDTH):
        for boxy in range(BHEIGHT):
            left, top = LTB(boxx, boxy)
            if not rev[boxx][boxy]:
                pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, BOXSIZE, BOXSIZE))
            else:
                shape, color = GSC(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)
def HB(boxx, boxy):
    left, top = LTB(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, BLUE, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)
def startGame(board):
    cBoxes = GRB(False)
    boxes = []
    for x in range(BWIDTH):
        for y in range(BHEIGHT):
            boxes.append( (x, y) )
    random.shuffle(boxes)
    boxGroups = splitIn(6, boxes)
    drawBoard(board, cBoxes)
    for boxGroup in boxGroups:
        RBA(board, boxGroup)
        CBA(board, boxGroup)
def gameWin(board):
    cBoxes = GRB(True)
    color1 = RED
    color2 = GREEN
    for i in range(13):
        color1, color2 = color2, color1
        DISPLAYSURF.fill(color1)
        drawBoard(board, cBoxes)
        pygame.display.update()
        pygame.time.wait(100)
def Win(rBoxes):
    for i in rBoxes:
        if False in i:
            return False 
    return True
if __name__ == '__main__':
    main()
