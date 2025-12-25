
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
                    pygame.draw.line(screen, (255, 255, 51),(win_tuple[0][1]*200 + 100,win_tuple[0][0]*200 + 25),(win_tuple[1][1]*200 + 100 , win_tuple[1][0]*200 + 575) , 10)
                    game_over = True
                chance = True
            if IS_FULL():
                game_over = True
                

        screen.fill((0,0,0))

        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] != 0:
                    DRAW_PLAYERS(col,row,board[row][col])
        
        DRAW_LINES()  
        pygame.display.update()