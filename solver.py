

def solve(board):
    # Base case
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if is_valid(board, (row, col), i):
            board[row][col] = i

            if solve(board):
                return True

            board[row][col] = 0
    return False


def find_empty(board):

    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == 0:
                return row, col

    return None


def is_valid(board, pos, num):
    # check row
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and i != pos[1]:
            return False

    # check column
    for i in range(len(board)):
        if board[i][pos[1]] == num and i != pos[0]:
            return False

    # check box
    # find out in which box is the current cell
    box_x = pos[0] // 3
    box_y = pos[1] // 3

    # coordinates of top left box corner
    x_start = box_x * 3
    y_start = box_y * 3

    for i in range(x_start, x_start + 3):
        for j in range(y_start, y_start + 3):
            if board[i][j] == num and pos != (i, j):
                return False

    return True

