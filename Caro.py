# AI chơi cờ Caro - Nhóm 4
# IT3160 - Nhập môn trí tuệ nhân tạo
import turtle
import random

global move_history
BOARD_SIZE = 17


def is_win(board):

    black = score_of_col(board, "b")
    white = score_of_col(board, "w")

    sum_sumcol_values(black)
    sum_sumcol_values(white)

    if 5 in black and black[5] == 1:
        return "Black won"
    elif 5 in white and white[5] == 1:
        return "White won"

    if (
        sum(black.values()) == black[-1]
        and sum(white.values()) == white[-1]
        or possible_moves(board) == []
    ):
        return "Draw"

    return "Continue playing"


# AI Engine

def march(board, x, y, dx, dy, length):
    """
    trả về điểm có toạ độ (x2,y2) = (x,y) + length*(dx,dy) nếu điểm đó nằm trong bàn cờ
    , nếu không thì giảm length
    """
    x2 = x + length*dx
    y2 = y + length*dy
    while not (0 <= x2 < BOARD_SIZE and 0 <= y2 < BOARD_SIZE):
        x2 -= dx
        y2 -= dy

    return x2, y2


def score_ready(scorecol):
    """
    Khởi tạo hệ thống điểm
    """
    sumcol = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, -1: {}}
    for key in scorecol:
        for score in scorecol[key]:
            if key in sumcol[score]:
                sumcol[score][key] += 1
            else:
                sumcol[score][key] = 1

    return sumcol


def sum_sumcol_values(sumcol):
    """
    hợp nhất điểm của mỗi hướng
    """

    for key in sumcol:
        if key == 5:
            sumcol[5] = int(1 in sumcol[5].values())
        else:
            sumcol[key] = sum(sumcol[key].values())


def score_of_list(lis, col):

    blank = lis.count(" ")
    filled = lis.count(col)

    if blank + filled < 5:
        return -1
    elif blank == 5:
        return 0
    else:
        return filled


def row_to_list(board, x, y, dx, dy, xf, yf):
    """
    trả về list của x,y từ xf,yf

    """
    row = []
    while x != xf + dx or y != yf + dy:
        row.append(board[x][y])
        x += dx
        y += dy
    return row


def score_of_row(board, cordi, dx, dy, cordf, col):
    """
    trả về một list với mỗi phần tử đại diện cho số điểm của 5 khối

    """
    colscores = []
    x, y = cordi
    xf, yf = cordf
    row = row_to_list(board, x, y, dx, dy, xf, yf)
    for start in range(len(row) - 4):
        score = score_of_list(row[start : start + 5], col)
        colscores.append(score)

    return colscores


def score_of_col(board, col):
    """
    tính toán điểm số mỗi hướng của column dùng cho is_win;
    """

    f = BOARD_SIZE
    # scores của 4 hướng đi
    scores = {(0, 1): [], (-1, 1): [], (1, 0): [], (1, 1): []}
    for start in range(BOARD_SIZE):
        scores[(0, 1)].extend(
            score_of_row(board, (start, 0), 0, 1, (start, f - 1), col)
        )
        scores[(1, 0)].extend(
            score_of_row(board, (0, start), 1, 0, (f - 1, start), col)
        )
        scores[(1, 1)].extend(
            score_of_row(board, (start, 0), 1, 1, (f - 1, f - 1 - start), col)
        )
        scores[(-1, 1)].extend(score_of_row(board, (start, 0), -1, 1, (0, start), col))

        if start + 1 < BOARD_SIZE:
            scores[(1, 1)].extend(
                score_of_row(board, (0, start + 1), 1, 1, (f - 2 - start, f - 1), col)
            )
            scores[(-1, 1)].extend(
                score_of_row(board, (f - 1, start + 1), -1, 1, (start + 1, f - 1), col)
            )

    return score_ready(scores)


def score_of_col_one(board, col, x, y):
    """
    trả lại điểm số của column trong x,y theo 4 hướng,
    key: điểm số khối đơn vị đó -> chỉ ktra 5 khối thay vì toàn bộ
    """

    scores = {(0, 1): [], (-1, 1): [], (1, 0): [], (1, 1): []}

    scores[(0, 1)].extend(
        score_of_row(
            board, march(board, x, y, 0, -1, 4), 0, 1, march(board, x, y, 0, 1, 4), col
        )
    )

    scores[(1, 0)].extend(
        score_of_row(
            board, march(board, x, y, -1, 0, 4), 1, 0, march(board, x, y, 1, 0, 4), col
        )
    )

    scores[(1, 1)].extend(
        score_of_row(
            board, march(board, x, y, -1, -1, 4), 1, 1, march(board, x, y, 1, 1, 4), col
        )
    )

    scores[(-1, 1)].extend(
        score_of_row(
            board,
            march(board, x, y, -1, 1, 4),
            1,
            -1,
            march(board, x, y, 1, -1, 4),
            col,
        )
    )

    return score_ready(scores)


def possible_moves(board):
    """
    khởi tạo danh sách tọa độ có thể có tại danh giới các nơi đã đánh phạm vi 3 đơn vị
    """
    # mảng taken lưu giá trị của người chơi và của máy trên bàn cờ
    taken = []
    # mảng directions lưu hướng đi (8 hướng)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]
    # cord: lưu các vị trí không đi
    cord = {}

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] != " ":
                taken.append((i, j))
    """ duyệt trong hướng đi và mảng giá trị trên bàn cờ của người chơi và máy, kiểm tra nước không thể đi(trùng với
    nước đã có trên bàn cờ)
    """
    for direction in directions:
        dx, dy = direction
        for coord in taken:
            x, y = coord
            for length in [1, 2, 3, 4]:
                move = march(board, x, y, dx, dy, length)
                if move not in taken and move not in cord:
                    cord[move] = False
    return cord


def TF34score(score3, score4):
    """
    trả lại trường hợp chắc chắn có thể thắng(4 ô liên tiếp)
    """
    for key4 in score4:
        if score4[key4] >= 1:
            for key3 in score3:
                if key3 != key4 and score3[key3] >= 2:
                    return True
    return False


def stupid_score(board, col, anticol, x, y):
    """
    cố gắng di chuyển x,y
    trả về điểm số tượng trưng lợi thế
    """

    global colors
    M = 1000
    res, adv, dis = 0, 0, 0

    # tấn công
    board[x][y] = col
    # draw_stone(x, y,colors[col])
    sumcol = score_of_col_one(board, col, x, y)
    a = winning_situation(sumcol)
    adv += a*M
    sum_sumcol_values(sumcol)
    # {0: 0, 1: 15, 2: 0, 3: 0, 4: 0, 5: 0, -1: 0}
    adv += sumcol[-1] + sumcol[1] + 4*sumcol[2] + 8*sumcol[3] + 16*sumcol[4]

    # phòng thủ
    board[x][y] = anticol
    sumanticol = score_of_col_one(board, anticol, x, y)
    d = winning_situation(sumanticol)
    dis += d*(M - 100)
    sum_sumcol_values(sumanticol)
    dis += (
        sumanticol[-1]
        + sumanticol[1]
        + 4*sumanticol[2]
        + 8*sumanticol[3]
        + 16*sumanticol[4]
    )

    res = adv + dis

    board[x][y] = " "
    return res


def winning_situation(sumcol):
    """
    trả lại tình huống chiến thắng dạng như:
    {0: {}, 1: {(0, 1): 4, (-1, 1): 3, (1, 0): 4, (1, 1): 4}, 2: {}, 3: {}, 4: {}, 5: {}, -1: {}}
    1-5 lưu điểm có độ nguy hiểm từ thấp đến cao,
    -1 là rơi vào trạng thái tồi, cần phòng thủ
    """

    if 1 in sumcol[5].values():
        return 5
    elif len(sumcol[4]) >= 2 or (len(sumcol[4]) >= 1 and max(sumcol[4].values()) >= 2):
        return 4
    elif TF34score(sumcol[3], sumcol[4]):
        return 4
    else:
        score3 = sorted(sumcol[3].values(), reverse=True)
        if len(score3) >= 2 and score3[0] >= score3[1] >= 2:
            return 3
    return 0


def best_move(board, col):
    """
    trả lại điểm số của mảng trong lợi thế của từng màu
    """
    if col == "w":
        anticol = "b"
    else:
        anticol = "w"

    movecol = (0, 0)
    maxscorecol = ""
    # kiểm tra nếu bàn cờ rỗng thì cho vị trí random nếu không thì đưa ra giá trị trên bàn cờ nên đi
    if board == [[" "]*BOARD_SIZE]*BOARD_SIZE:
        movecol = (
            int((BOARD_SIZE)*random.random()),
            int((len(board[0]))*random.random()),
        )
    else:
        moves = possible_moves(board)

        for move in moves:
            x, y = move
            if maxscorecol == "":
                scorecol = stupid_score(board, col, anticol, x, y)
                maxscorecol = scorecol
                movecol = move
            else:
                scorecol = stupid_score(board, col, anticol, x, y)
                if scorecol > maxscorecol:
                    maxscorecol = scorecol
                    movecol = move
    return movecol


##Graphics Engine
def click(x, y):
    global board, colors, win, move_history

    x, y = round(x), round(y)

    if x == -1 and y == -1 and len(move_history) != 0:
        x, y = move_history[-1]

        del move_history[-1]
        board[x][y] = " "
        x, y = move_history[-1]

        del move_history[-1]
        board[x][y] = " "
        return

    if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
        return

    if board[x][y] == " ":

        draw_stone(x, y, colors["b"])
        board[x][y] = "b"

        move_history.append((x, y))

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            print(game_res)
            win = True
            return

        ax, ay = best_move(board, "w")
        draw_stone(ax, ay, colors["w"])
        board[ax][ay] = "w"

        move_history.append((ax, ay))

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            print(game_res)
            win = True
            return


def initialize(size):
    global win, board, screen, colors, move_history

    move_history = []
    win = False
    # Make empty board
    board = []
    for i in range(size):
        board.append([" "]*size)

    screen = turtle.Screen()
    screen.onclick(click)
    screen.setup(screen.screensize()[1]*2, screen.screensize()[1]*2)
    screen.setworldcoordinates(-1, size, size, -1)
    screen.bgcolor("orange")
    screen.tracer(500)

    colors = {"w": turtle.Turtle(), "b": turtle.Turtle(), "g": turtle.Turtle()}
    colors["w"].color("white")
    colors["b"].color("black")

    for key in colors:
        colors[key].ht()
        colors[key].penup()
        colors[key].speed(0)

    border = turtle.Turtle()
    border.speed(9)
    border.penup()

    side = (size - 1) / 2

    i = -1
    for start in range(size):
        border.goto(start, side + side*i)
        border.pendown()
        i *= -1
        border.goto(start, side + side*i)
        border.penup()

    i = 1
    for start in range(size):
        border.goto(side + side*i, start)
        border.pendown()
        i *= -1
        border.goto(side + side*i, start)
        border.penup()
        border.begin_poly()

    border.ht()

    screen.listen()
    screen.mainloop()


def draw_stone(x, y, color):
    color.goto(x, y - 0.3)
    color.pendown()
    color.begin_fill()
    color.circle(0.3)
    color.end_fill()
    color.penup()


if __name__ == "__main__":
    print("Welcome to Caro game!")
    initialize(BOARD_SIZE)
