import os
import random
import sys
import pygame
from pygame.locals import *

Background_Color = (255, 255, 255)
Num_random = 50
FPS = 20

def GetImagePath(filepath):
    imgs = os.listdir(filepath)
    return os.path.join(filepath, random.choice(imgs))


def stop():
    pygame.quit()
    sys.exit()

def show_end_interface(Demo, width, height, over):
   Demo.fill(Background_Color)
   font = pygame.font.Font('./font/simkai.ttf', width//8)
   font2 = pygame.font.Font('./font/simkai.ttf', width//12)
   title = font.render('You have win!', True, (233,150,122))
   title2 = font2.render('press enter to continue', True, (233,150,122))
   rect = title.get_rect()
   rect2 = title2.get_rect()
   rect.midtop = (width/2, height/3)
   rect2.midtop = (width/2, height/2)
   Demo.blit(title, rect)
   Demo.blit(title2, rect2)
   pygame.display.update()
   pygame.time.wait(500)
   while True:
       for event in pygame.event.get():
           if event.type == QUIT:
               stop()

           elif event.type == KEYDOWN:
               if event.key == K_ESCAPE:
                   stop()
               if event.key == K_RETURN:
                   over = False
                   main()

#设置开始界面，获得选择的拼图模式
def show_start_interface(Demo, width, height):
    Demo.fill(Background_Color)
    tfont = pygame.font.Font('./font/simkai.ttf', width//4)
    cfont = pygame.font.Font('./font/simkai.ttf', width//20)
    title = tfont.render('拼图游戏', True, (255,0,0))
    content1 = cfont.render('按h或m或l键开始游戏', True, (0,255,0))
    content2 = cfont.render('H为5*5模式，M为4*4模式，L为3*3模式', True, (0,0,255))
    trect = title.get_rect()
    trect.midtop = (width / 2, height / 10)
    crect1 = content1.get_rect()
    crect1.midtop = (width / 2, height / 2.2)
    crect2 = content2.get_rect()
    crect2.midtop = (width / 2, height / 1.8)
    Demo.blit(title, trect)
    Demo.blit(content1, crect1)
    Demo.blit(content2, crect2)
    pygame.display.update()
    while True:
        size = None
        for event in pygame.event.get():
            if event.type == QUIT:
                stop()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    stop()
                if event.key == ord('l'):
                    size = 3
                elif event.key == ord('m'):
                    size = 4
                elif event.key == ord('h'):
                    size = 5
        if size:
            break
    return size

# 将空白Cell右边的Cell左移到空白Cell位置
def moveL(board, blankCell, columns):
    if (blankCell+1) % columns == 0:
        return blankCell
    board[blankCell+1], board[blankCell] = board[blankCell], board[blankCell+1]
    return blankCell + 1

# 将空白Cell左边的Cell右移到空白Cell位置
def moveR(board, blankCell, colunms):
    if blankCell % colunms == 0:
        return blankCell
    board[blankCell - 1], board[blankCell] = board[blankCell], board[blankCell - 1]
    return blankCell - 1

# 将空白Cell下边的Cell上移到空白Cell位置
def moveU(board, blankCell, row, columns):
    if blankCell >= (row-1) * columns:
        return blankCell
    board[blankCell+columns], board[blankCell] = board[blankCell], board[blankCell+columns]
    return blankCell + columns

#将空白Cell上边的Cell下移到空白Cell位置
def moveD(board, blankCell, columns):
    if blankCell < columns:
        return blankCell
    board[blankCell-columns], board[blankCell] = board[blankCell], board[blankCell-columns]
    return blankCell - columns


#获得打乱的拼图
def createBoard(row, columns, num_cell):
    board = []
    for i in range(num_cell):
        board.append(i)
    #去掉右下角那块，即第9块
    blankCell = num_cell - 1
    board[blankCell] = -1

    #循环100次让第一个空白位随机
    for i in range(Num_random):
        # 0: left
        # 1: right
        # 2: up
        # 3: down
        direction = random.randint(0, 3)
        if direction == 0:
            blankCell = moveL(board, blankCell, columns)
        elif direction == 1:
            blankCell = moveR(board, blankCell, columns)
        elif direction == 2:
            blankCell = moveU(board, blankCell, row, columns)
        elif direction == 3:
            blankCell = moveD(board, blankCell, columns)
    return board, blankCell

def isOver(board, size):
    try:
        num_cell = size * size
    except:
        num_cell = size[0] * size[1]
    for i in range(num_cell-1):
        if board[i] != i:
            return False
    return True

def main():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("./music/bg.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

    mainClock = pygame.time.Clock()
    gameImg = pygame.image.load(GetImagePath(filepath))
    #获取宽高
    ImgRect = gameImg.get_rect()
    #定义界面和标题
    Demo = pygame.display.set_mode((ImgRect.width, ImgRect.height))
    pygame.display.set_caption('拼图游戏')
    #开始游戏界面设置
    size =show_start_interface(Demo, ImgRect.width, ImgRect.height)
    if isinstance(size, int):
        row,columns = size, size
        num_Cell = size * size
    else:
        stop()

    #计算cell大小
    cellwidth = ImgRect.width // columns
    cellheight = ImgRect.height // row

    #游戏是否结束
    over = False

    #避免初始化为原图
    while True:
        gameBoard, blankCell = createBoard(row, columns, num_Cell)
        if not isOver(gameBoard, size):
            break

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                stop()
            if over:
                show_end_interface(Demo, ImgRect.width, ImgRect.height, over)

            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == ord('a'):
                    blankCell = moveL(gameBoard, blankCell, columns)
                elif event.key == K_RIGHT or event.key == ord('d'):
                    blankCell = moveR(gameBoard, blankCell, columns)
                elif event.key == K_UP or event.key == ord('w'):
                    blankCell = moveU(gameBoard, blankCell, row, columns)
                elif event.key == K_DOWN or event.key == ord('s'):
                    blankCell = moveD(gameBoard, blankCell, columns)

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                x_pos = x // cellwidth
                y_pos = y // cellheight
                idx = x_pos + y_pos * columns
                if idx == blankCell-1 or idx == blankCell+1 or idx == \
                    blankCell+columns or idx == blankCell-columns:
                    gameBoard[blankCell], gameBoard[idx] = gameBoard[idx], gameBoard[blankCell]
                    blankCell = idx
        if isOver(gameBoard, size):
            gameBoard[blankCell] = num_Cell - 1
            over = True
        Demo.fill(Background_Color)
        for i in range(num_Cell):
            if gameBoard[i] == -1:
                continue
            x_pos = i % columns
            y_pos = i // columns
            rect = pygame.Rect(x_pos*cellwidth, y_pos*cellheight, cellwidth, cellheight)
            ImgArea = pygame.Rect((gameBoard[i]%columns)*cellwidth, (gameBoard[i]//columns)*
                                  cellheight, cellwidth, cellheight)
            Demo.blit(gameImg, rect, ImgArea)
        for i in range(columns+1):
            pygame.draw.line(Demo, (0, 0, 0), (i*cellwidth, 0), (i*cellwidth, ImgRect.height))
        for i in range(row+1):
            pygame.draw.line(Demo, (0, 0, 0), (0, i*cellheight), (ImgRect.width, i*cellheight))
        pygame.display.update()
        mainClock.tick(FPS)

if __name__ == '__main__':
    filepath = './pictures'
    main()