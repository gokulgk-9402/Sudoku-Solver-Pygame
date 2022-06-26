import pygame
import time

pygame.font.init()

screen = pygame.display.set_mode((450, 650))

pygame.display.set_caption("Sudoku Solver")
img = pygame.image.load('icon.png')
pygame.display.set_icon(img)

# bg = pygame.image.load('bg.png')

x = 0
y = 0
diff = 50
val = 0

HIGHLIGHT = 0
HIGHLIGHT_X = -1
HIGHLIGHT_Y = -1

grid = [[0 for _ in range(9)] for _ in range(9)]

initial = [[0 for _ in range(9)] for _ in range(9)]
user = [[0 for _ in range(9)] for _ in range(9)]
solution = [[0 for _ in range(9)] for _ in range(9)]

def import_puzzle():
    with open("data.txt", "r") as f:
        data = f.readlines()

    for i, line in enumerate(data):
        line = line.strip()
        line = line.split()
        for j, ele in enumerate(line):
            grid[i][j] = int(ele)
            solution[i][j] = int(ele)

    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                initial[i][j] = 1
            else:
                initial[i][j] = 0
            user[i][j] = 0

font1 = pygame.font.SysFont("comicsans", 35)
font2 = pygame.font.SysFont("comicsans", 20)
font3 = pygame.font.SysFont("comicsans", 25)

def get_cord(pos):
    global x
    x = pos[0]//diff
    global y
    y = pos[1]//diff

def draw_box():
    for i in range(2):
        pygame.draw.line(screen, (255, 0, 0), (x*diff -3, (y+i)* diff), (x*diff + diff +3, (y+i)*diff), 7)
        pygame.draw.line(screen, (255, 0, 0), ((x+i)*diff -3, y* diff), ((x+i)*diff, y*diff + diff), 7)

def draw_board(puzzle, iswrong = False, row = -1, col = -1):
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] != 0:
                if iswrong and i == row and j == col:
                    clr = (255, 51, 51)
                elif user[i][j] != 0:
                    clr = (255, 255, 100)
                elif initial[i][j] != 0:
                    clr = (180, 180, 180)
                else:
                    clr = (0, 230, 230)
                pygame.draw.rect(screen, clr, (j*diff, i*diff, diff+1, diff+1))
                text1 = font1.render(str(puzzle[i][j]), 1, (0,0,0))
                screen.blit(text1, (j*diff +15, i*diff))

    for i in range(10):
        if i %3 == 0:
            thickness = 5

        else:
            thickness = 1

        pygame.draw.line(screen, (0,0,0), (0, i*diff), (450, i*diff), thickness)
        pygame.draw.line(screen, (0,0,0), (i*diff, 0), (i*diff, 450), thickness)

def draw_buttons():
    pygame.draw.rect(screen, (128, 0, 0), pygame.Rect(25, 575, 100, 50))
    SolveButton = font3.render("CHECK", True, (255, 255, 255), (128, 0, 0))
    textRect = SolveButton.get_rect()
    textRect.center = (75, 600)
    screen.blit(SolveButton, textRect)
    pygame.draw.rect(screen, (128, 0, 0), pygame.Rect(175, 575, 100, 50))
    ResetButton = font3.render("SOLVE", True, (255, 255, 255), (128, 0, 0))
    textRect2 = SolveButton.get_rect()
    textRect2.center = (225, 600)
    screen.blit(ResetButton, textRect2)
    pygame.draw.rect(screen, (128, 0, 0), pygame.Rect(325, 575, 100, 50))
    ResetButton = font3.render("RESET", True, (255, 255, 255), (128, 0, 0))
    textRect3 = SolveButton.get_rect()
    textRect3.center = (375, 600)
    screen.blit(ResetButton, textRect3)
    pygame.draw.rect(screen, (128, 0, 0), pygame.Rect(175, 475, 100, 50))
    ResetButton = font2.render("IMPORT", True, (255, 255, 255), (128, 0, 0))
    textRect4 = SolveButton.get_rect()
    textRect4.center = (225, 500)
    screen.blit(ResetButton, textRect4)

def draw_solving():
    SolveButton = font1.render("SOLVING...", True, (255, 255, 255), (0, 150, 150))
    textRect = SolveButton.get_rect()
    textRect.center = (225, 550)
    screen.blit(SolveButton, textRect)

def draw_correctness(crt, val):
    if val:
        clr = (0, 204, 0)
    else:
        clr = (255, 51, 51)
    SolveButton = font1.render(crt, True, (0, 0, 0), clr)
    textRect = SolveButton.get_rect()
    textRect.center = (225, 225)
    screen.blit(SolveButton, textRect)

def is_import_button(pos):
    if pos[0] >= 175 and pos[0] <= 275 and pos[1] >= 475 and pos[1] <= 525:
        return 1
    return 0

def is_check_button(pos):
    if pos[0] >= 25 and pos[0] <= 125 and pos[1] >= 575 and pos[1] <= 625:
        return 1
    return 0

def is_solve_button(pos):
    if pos[0] >= 175 and pos[0] <= 275 and pos[1] >= 575 and pos[1] <= 625:
        return 1
    return 0

def is_reset_button(pos):
    if pos[0] >= 325 and pos[0] <= 425 and pos[1] >= 575 and pos[1] <= 625:
        return 1
    return 0

def is_grid(pos):
    if pos[0] >= 0 and pos[0] <= 450 and pos[1] >= 0 and pos[1] <= 450:
        return 1
    return 0

def get_box(pos):
    return pos[0]//50, pos[1]//50

def highlight_box():
    pygame.draw.line(screen, (255, 0, 0), (HIGHLIGHT_X * 50, HIGHLIGHT_Y*50), (HIGHLIGHT_X*50 + 50, HIGHLIGHT_Y*50), 4)
    pygame.draw.line(screen, (255, 0, 0), (HIGHLIGHT_X * 50, HIGHLIGHT_Y*50), (HIGHLIGHT_X*50, HIGHLIGHT_Y*50 + 50), 4)
    pygame.draw.line(screen, (255, 0, 0), (HIGHLIGHT_X * 50, HIGHLIGHT_Y*50 + 50), (HIGHLIGHT_X*50 + 50, HIGHLIGHT_Y*50 + 50), 4)
    pygame.draw.line(screen, (255, 0, 0), (HIGHLIGHT_X * 50 + 50, HIGHLIGHT_Y*50), (HIGHLIGHT_X*50 + 50, HIGHLIGHT_Y*50 + 50), 4)

import time

def find_next_empty(puzzle):
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:
                return i,j

    return None, None

def is_valid(puzzle, guess, row, col):
    if guess in puzzle[row]:
        return False
    col_values = [puzzle[r][col] for r in range(9)]
    if guess in col_values:
        return False

    square_r = row//3
    square_c = col//3
    start_r = square_r * 3
    start_c = square_c * 3

    for r in range(start_r, start_r + 3):
        for c in range(start_c, start_c + 3):
            if puzzle[r][c] == guess:
                return False

    return True

def solve_sudoku (puzzle, visualize = True):

    row, col = find_next_empty(puzzle)


    if row is None:
        return True

    for guess in range(1, 10):

        if is_valid(puzzle, guess, row, col):
            puzzle[row][col] = guess
            if visualize:
                screen.fill((255, 255, 255))
                # screen.blit(bg, (0,0))
                draw_board(grid)
                draw_solving()
                if HIGHLIGHT:
                    highlight_box()
                pygame.display.update()

            if solve_sudoku(puzzle, visualize):
                return True
        
        if visualize:
            screen.fill((255, 255, 255))
            # screen.blit(bg, (0,0))
            draw_board(grid, True, row, col)
            draw_solving()
            pygame.display.update()
            time.sleep(0.1)
        puzzle[row][col] = 0
    return False

run = True
correct = True
while run:

    screen.fill((255, 255, 255))
    # screen.blit(bg, (0,0))
    draw_board(grid)
    draw_buttons()
    if HIGHLIGHT:
        highlight_box()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if is_solve_button(pos):
                HIGHLIGHT = 0
                solvable = solve_sudoku(grid)
                if not solvable:
                    draw_correctness("UNSOLVABLE", False)
                else:
                    draw_correctness("SOLVED!", True)
                pygame.display.update()
                time.sleep(1)
            elif is_reset_button(pos):
                HIGHLIGHT = 0
                grid = [[0 for _ in range(9)] for _ in range(9)]

                initial = [[0 for _ in range(9)] for _ in range(9)]
                user = [[0 for _ in range(9)] for _ in range(9)]
                solution = [[0 for _ in range(9)] for _ in range(9)]

            elif is_check_button(pos):
                # correct = solve_sudoku(grid, False)
                # correct = True
                # for i in range(9):
                #     for j in range(9):
                #         if user[i][j]:
                #             correct = is_valid(grid, grid[i][j], i, j
                correct = True
                # print('user: ')
                # for row in user:
                #     print(row)
                # print('grid: ')
                # for row in grid:
                #     print(row)
                # print('solution: ')
                # for row in solution:
                #     print(row)
                if correct:
                    for i in range(9):
                        for j in range(9):
                            if user[i][j] == 1:
                                # print(grid[i][j] == solution[i][j])
                                correct = (grid[i][j] == solution[i][j])
                correct = correct and solve_sudoku(grid, False)

                if correct:
                    draw_correctness("CORRECT", True)
                else:
                    draw_correctness("WRONG", False)
                pygame.display.update()
                time.sleep(0.5)

                for i in range(9):
                    for j in range(9):
                        if not (initial[i][j] or user[i][j]):
                            grid[i][j] = 0
            
            elif is_import_button(pos):
                import_puzzle()
                correct = solve_sudoku(solution, False)

            elif is_grid(pos):
                press_r, press_c = get_box(pos)
                if not initial[press_c][press_r]:
                    HIGHLIGHT = 1
                    HIGHLIGHT_X = press_r
                    HIGHLIGHT_Y = press_c
                    highlight_box()
                    pygame.display.update()
                else:
                    HIGHLIGHT = 0

            else:
                HIGHLIGHT = 0
        
        elif event.type == pygame.KEYDOWN:
            val = -1
            if event.key == pygame.K_1:
                val = 1
            elif event.key == pygame.K_2:
                val = 2
            elif event.key == pygame.K_3:
                val = 3
            elif event.key == pygame.K_4:
                val = 4
            elif event.key == pygame.K_5:
                val = 5
            elif event.key == pygame.K_6:
                val = 6
            elif event.key == pygame.K_7:
                val = 7
            elif event.key == pygame.K_8:
                val = 8
            elif event.key == pygame.K_9:
                val = 9
            elif event.key == pygame.K_0:
                val = 0
            elif event.key == pygame.K_BACKSPACE:
                val = 0

            if HIGHLIGHT and val!=-1:
                if val:
                    user[HIGHLIGHT_Y][HIGHLIGHT_X] = 1
                else:
                    user[HIGHLIGHT_Y][HIGHLIGHT_X] = 0
                grid[HIGHLIGHT_Y][HIGHLIGHT_X] = val

pygame.quit()
