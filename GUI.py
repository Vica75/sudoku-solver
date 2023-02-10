import pygame
from solver import is_valid, find_empty
pygame.font.init()


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600


class Grid:

    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.cells = [[Cell(width, height, self.board[i][j], i, j) for j in range(cols)] for i in range(rows)]
        self.model = None
        self.win = win

    def draw(self):
        gap = self.width / 9  # the gap between lines is the same width as one tile
        pad = 10

        for i in range(self.rows + 1):  # because we want 10 lines
            # we want the 0th one, 3rd one 6th one etc to be thicker
            if i % 3 == 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, BLACK, (pad, i*gap + pad), (self.width + pad, i*gap + pad), thick)
            pygame.draw.line(self.win, BLACK, (i*gap + pad, pad), (i*gap + pad, self.height + pad), thick)

        # draw cells
        for row in self.cells:
            for cell in row:
                cell.draw(self.win)

    def update_model(self):
        self.model = [[self.cells[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def solve_gui(self):
        self.update_model()
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if is_valid(self.model, (row, col), i):
                self.cells[row][col].set_value(i)
                self.update_model()
                self.cells[row][col].draw_change(self.win, True)
                pygame.display.update()
                pygame.time.delay(100)
                print(i)

                if self.solve_gui():
                    return True

                self.cells[row][col].set_value(0)
                self.update_model()
                self.cells[row][col].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False


class Cell:
    rows = 9
    cols = 9

    def __init__(self, width, height, value, row, col):
        self.width = width
        self.height = height
        self.value = value
        self.row = row
        self.col = col

    def set_value(self, value):
        self.value = value

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.value != 0:
            text = fnt.render(str(self.value), True, DARK_BLUE)
            win.blit(text, (x + (gap/2 - text.get_width()/2) + 10, y + (gap/2 - text.get_height()/2) + 10))

    # separate function needed so that the numbers are not drawn on top of each other
    def draw_change(self, win, correct):
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, WHITE, (x, y, self.width, self.height))
        fnt = pygame.font.SysFont("comicsans", 40)

        if correct:
            color = GREEN
        else:
            color = RED

        text = fnt.render(str(self.value), True, color)
        win.blit(text, (x + (gap / 2 - text.get_width() / 2) + 10, y + (gap / 2 - text.get_height() / 2) + 10))


def redraw_window(win, board):
    win.fill(WHITE)
    board.draw()


def main():
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Sudoku Solver!")

    board = Grid(9, 9, 540, 540, win)
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    board.solve_gui()

        redraw_window(win, board)
        pygame.display.update()


main()
