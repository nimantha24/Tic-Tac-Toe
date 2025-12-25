import pygame
import numpy as np
import sys

BG_COLOR = ((0, 0, 0))
HEIGH = 600
WIDTH = 600
COL_SIZE = 200
ROW_SIZE = 200
LINE_COLOR = (255,255,255)
click_positions = []
MARK_COLOR = (255, 255, 0)
BOARD_ROWS = 3
BOARD_COLS = 3
win_tuple = []

# 1 == player 
# 2 == AI


board = np.zeros((3,3))

pygame.init()
font = pygame.font.SysFont("Arial", 100 , bold=True)
screen = pygame.display.set_mode((HEIGH,WIDTH))
pygame.display.set_caption("games")
screen.fill(BG_COLOR)

def MARK_SQUARE(row , col , player):
    board[row][col] = player

def DRAW_LINES():
        pygame.draw.line(screen , LINE_COLOR , (200,0) , (200 ,600),5)
        pygame.draw.line(screen , LINE_COLOR , (400,0) , (400 ,600),5)
        pygame.draw.line(screen , LINE_COLOR , (0,200) , (600 ,200),5)
        pygame.draw.line(screen , LINE_COLOR , (0,400) , (600 ,400),5)

def IS_FULL():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if  board[row][col] == 0:
                return False
    return True

def draw_text(text,color):
    text_surface = font.render(text, True, color)

    # screen.blit(text_surface, (WIDTH//2 - text_surface.get_width()//2, HEIGHT//2 - text_surface.get_height()//2))
    screen.blit(text_surface, (170, 250))


def DRAW_PLAYERS(col,row,player):
    if player == 1:
        pygame.draw.line(screen , (255,0,0) , (col*200 + 50 ,row*200 + 50) , (col*200 + 150 , row*200 +150),20)
        pygame.draw.line(screen , (255,0,0) , (col*200 + 150 ,row*200 + 50) , (col*200 + 50 , row*200 +150),20)

    elif player == 2:
        pygame.draw.circle(screen, (0,0,255), (col*200 + 100 , row*200 + 100), 60, 15)


def IS_AVAILABLE(row,col):
    return board[row][col] == 0

def MARK_WIN(board,player):
    win_tuple.clear()
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] == player :
            win_tuple.append((row,0))          #horizontal
            win_tuple.append((row,2))
            return True
    for col in range(BOARD_ROWS):
        if board[0][col] == board[1][col] == board[2][col] == player :
            win_tuple.append((0,col))           #vertical
            win_tuple.append((2,col))
            return True
    if board[0][0] == board[1][1] ==board[2][2] == player:
        win_tuple.append((0,0))
        win_tuple.append((2,2))
        return True
    if board[0][2] == board[1][1] ==board[2][0] == player:
        win_tuple.append((0,2))
        win_tuple.append((2,0))
        return True
    return False

def minimax(value):
    if MARK_WIN(board,2):
        return 1
    if MARK_WIN(board,1):
        return -1
    if IS_FULL():
        return 0
    
    if value:
        best_value = -1000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 0:
                    board[row][col] = 2
                    score = minimax(False)
                    best_value = max(best_value ,score)
                    board[row][col] = 0
        return best_value


    else:
        best_value = 1000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 0:
                    board[row][col] = 1
                    score = minimax(True)
                    best_value = min(best_value ,score)
                    board[row][col] = 0
        return best_value       

def BEST_MOVE():
    best_value = -1000
    best_move = None
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 2 # AI move 
                score = minimax(False)
                board[row][col] = 0
                if score > best_value:
                    best_value = score
                    best_move = (row,col)
    return best_move
                

def display():
    chance = True
    game_over = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP and chance and not game_over:
                pos = pygame.mouse.get_pos()
                mouseX = pos[0] // 200
                mouseY = pos[1] // 200 
                if IS_AVAILABLE(mouseY, mouseX):
                    MARK_SQUARE(mouseY, mouseX, 1)
                    if MARK_WIN(board,1):

                        game_over = True
                    chance = False

        if chance == False and not game_over:
            move = BEST_MOVE()
            if move and IS_AVAILABLE(move[0], move[1]):
                MARK_SQUARE(move[0], move[1], 2)
                if MARK_WIN(board,2):
                    game_over = True
                chance = True
            if IS_FULL():
                game_over = True
                

        screen.fill((BG_COLOR))

        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] != 0:
                    DRAW_PLAYERS(col,row,board[row][col])
                
                if MARK_WIN(board,2):
                    if win_tuple[0][1] == win_tuple[1][1] :#VETICAL
                        pygame.draw.line(screen, (255, 255, 51),(win_tuple[0][1]*200 + 100,win_tuple[0][0]*200 + 25),(win_tuple[1][1]*200 + 100 , win_tuple[1][0]*200 + 175) , 10)
                    elif  win_tuple[0][0] == win_tuple[1][0] :#HORIZONTAL
                        pygame.draw.line(screen, (255, 255, 51),(win_tuple[0][1]*200 + 25 , win_tuple[0][0]*200 + 100),(win_tuple[1][1]*200 + 175 , win_tuple[1][0]*200 + 100) , 10)
                    elif win_tuple[0][0] == win_tuple[1][1] :
                        pygame.draw.line(screen, (255, 255, 51),(win_tuple[0][1]*200 + 175 , win_tuple[0][0]*200 + 25),(win_tuple[1][1]*200 + 25 , win_tuple[1][0]*200 + 175) , 10)
                    else:
                        pygame.draw.line(screen, (255, 255, 51),(win_tuple[0][1]*200 + 25 , win_tuple[0][0]*200 + 25),(win_tuple[1][1]*200 + 175 , win_tuple[1][0]*200 + 175) , 10)

        if game_over:
            draw_text("AI WIN", (0, 255, 0))





        DRAW_LINES()  
        pygame.display.update()

display()