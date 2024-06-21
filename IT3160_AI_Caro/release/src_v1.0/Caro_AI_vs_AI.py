# AI chơi cờ Caro - Nhóm 4 Caro - New
# IT3160 - Nhập môn trí tuệ nhân tạo
import turtle
import random

'''
Default settings:
    Player is 'b'
    AI is 'w'
'''
BOARD_SIZE = 25
WIN = 5
FIRST_HIT = 0 # 0: Player first | 1: AI first
PLAYER_COLOR = 'b' # Color of player
Win = 0 # | 'b' - Player win | 'w' - AI win |
Number_move = 0
Board = []
Move_history = []
Colors = {}

# AI Engine
def forward(x, y, dx, dy, len):
    """
    trả về điểm có toạ độ (x2,y2) = (x,y) + length*(dx,dy) nếu điểm đó nằm trong bàn cờ
    , nếu không thì giảm length
    """
    x2 = x + len*dx
    y2 = y + len*dy
    while not (0 <= x2 < BOARD_SIZE and 0 <= y2 < BOARD_SIZE):
        x2 -= dx
        y2 -= dy

    return (x2, y2)


def sum_sumcol_values(score_sum):
    """
    hợp nhất điểm của mỗi hướng
    """
    for key in score_sum:
        if key == 5:
            score_sum[5] = int(1 in score_sum[5].values())
        else:
            score_sum[key] = sum(score_sum[key].values())


def score_of_line(begin_point, dx, dy, end_point, bw):
    """
    trả về một list với mỗi phần tử đại diện cho số điểm của 5 khối
    (dx, dy) = vector hướng từ begin_point đến end_point
    """
    x, y = begin_point
    xf, yf = end_point
    # Get line from begin_point to end_point
    line = []
    line.append(Board[x][y])
    while x != xf or y != yf:
        x += dx
        y += dy
        line.append(Board[x][y])

    line_score = []
    for i in range(len(line) - (WIN - 1)):
        blank = line[i : i + WIN].count('')
        hit = line[i : i + WIN].count(bw)
        if blank + hit != WIN: # opponent has a hit in this line
            score = -1
        else:
            score = hit
        line_score.append(score)

    return line_score


def score_all(bw):
    """
    tính toán điểm số mỗi trên toàn bộ các hướng của bw
    """
    END = BOARD_SIZE - 1
    # scores của 4 hướng đi
    score = {(1, 0): [], (0, 1): [], (1, 1): [], (-1, 1): []}
    for i in range(BOARD_SIZE):
        score[(1, 0)] += score_of_line((0, i), 1, 0, (END, i), bw)
        score[(0, 1)] += score_of_line((i, 0), 0, 1, (i, END), bw)

    score[(1, 1)] += score_of_line((0, 0), 1, 1, (END, END), bw)
    score[(-1, 1)] += score_of_line((0, END), 1, -1, (END, 0), bw)
    for i in range(1, BOARD_SIZE - (WIN - 1)):
        score[(1, 1)] += score_of_line((i, 0), 1, 1, (END, END - i), bw)
        score[(1, 1)] += score_of_line((0, i), 1, 1, (END - i, END), bw)
        score[(-1, 1)] += score_of_line((i, END), 1, -1, (END, i), bw)

    for i in range(WIN - 1, BOARD_SIZE):
        score[(-1, 1)] += score_of_line((i, 0), -1, 1, (0, i), bw)
    
    return score_ready(score)


def score_of_col_one(x, y, bw):
    """
    trả lại điểm số của column trong x,y theo 4 hướng,
    key: điểm số khối đơn vị đó -> chỉ ktra 5 khối thay vì toàn bộ
    """

    scores = {(0, 1): [], (-1, 1): [], (1, 0): [], (1, 1): []}
    
    scores[(1, 0)] += score_of_line(forward(x, y, -1, 0, 4), 1, 0, forward(x, y, 1, 0, 4), bw)
    scores[(0, 1)] += score_of_line(forward(x, y, 0, -1, 4), 0, 1, forward(x, y, 0, 1, 4), bw)
    scores[(1, 1)] += score_of_line(forward(x, y, -1, -1, 4), 1, 1, forward(x, y, 1, 1, 4), bw)
    scores[(-1, 1)] += score_of_line(forward(x, y, -1, 1, 4), 1, -1, forward(x, y, 1, -1, 4), bw)

    return score_ready(scores)


def score_ready(score_all):
    """
    Khởi tạo hệ thống điểm
    """
    score_sum = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, -1: {}}
    for key in score_all:
        for score in score_all[key]:
            if key in score_sum[score]:
                score_sum[score][key] += 1
            else:
                score_sum[score][key] = 1

    return score_sum

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


def winning_situation(score_sum):
    """
    trả lại tình huống chiến thắng dạng như:
    {0: {}, 1: {(0, 1): 4, (-1, 1): 3, (1, 0): 4, (1, 1): 4}, 2: {}, 3: {}, 4: {}, 5: {}, -1: {}}
    1-5 lưu điểm có độ nguy hiểm từ thấp đến cao,
    -1 là rơi vào trạng thái tồi, cần phòng thủ
    """

    # một bên thắng
    if 1 in score_sum[5].values():
        return 5
    elif len(score_sum[4]) >= 2 or (len(score_sum[4]) >= 1 and max(score_sum[4].values()) >= 2):
        return 4
    elif TF34score(score_sum[3], score_sum[4]):
        return 4
    else:
        score3 = sorted(score_sum[3].values(), reverse=True)
        if len(score3) >= 2 and score3[0] >= score3[1] >= 2:
            return 3
    return 0


def AI_calc_score(x, y):
    """
    cố gắng di chuyển x,y
    trả về điểm số tượng trưng lợi thế
    """
    Multiplier = 1000
    result, attack, defense = 0, 0, 0
    # attack
    Board[x][y] = 'w'
    score_sum = score_of_col_one(x, y, 'w')
    a = winning_situation(score_sum)
    attack += a*Multiplier
    sum_sumcol_values(score_sum)
    attack += ( 
        score_sum[-1] 
        + score_sum[1] 
        + 4*score_sum[2] 
        + 8*score_sum[3] 
        + 16*score_sum[4])

    # phòng thủ
    Board[x][y] = 'b'
    score_sum = score_of_col_one(x, y, 'b')
    d = winning_situation(score_sum)
    defense += d*(Multiplier/10)
    sum_sumcol_values(score_sum)
    defense += (
        score_sum[-1]
        + score_sum[1]
        + 4*score_sum[2]
        + 8*score_sum[3]
        + 16*score_sum[4])
    
    result = attack + defense
    Board[x][y] = ''
    return result


def get_expect_move():
    """
    1: Lấy những ô đã đánh
    2: lấy toạ độ x_min -> x_max, y_min -> y_max của hình chữ nhật bao quanh các ô đã đánh
    3: trả về các ô có thể đi trong phạm vi rộng hơn 4 ô mỗi chiều của hình chữ nhật đó
    """
    global Board
    # mảng hit lưu những ô đã đánh, cả X và O
    hit = []
    x_min, x_max, y_min, y_max = 0, BOARD_SIZE - 1, 0, BOARD_SIZE - 1
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if Board[i][j] != '':
                hit.append((i, j))
                if i < x_min:
                    x_min = i
                elif i > x_max:
                    x_max = i
                if j < y_min:
                    y_min = j
                elif j > y_max:
                    y_max = j
    
    x_min2 = x_min - 4
    x_max2 = x_max + 4
    y_min2 = y_min - 4
    y_max2 = y_max + 4
    while x_min2 < 0:
        x_min2 += 1
    while x_max2 >= BOARD_SIZE:
        x_max2 -= 1
    while y_min2 < 0:
        y_min2 += 1
    while y_max2 >= BOARD_SIZE:
        y_max2 -= 1
    
    unhit = []
    for i in range(x_min, x_max + 1):
        for j in range(y_min, y_max + 1):
            if Board[i][j] == '':
                unhit.append((i, j))
    
    for x in range(x_min2, x_max2 + 1):
        for y in range(y_min2, y_max2 + 1):
            if not (x_min <= x <= x_max and y_min <= y <= y_max):
                unhit.append((x, y))
    return unhit


def best_move():
    """
    trả lại điểm số của mảng trong lợi thế của từng màu
    """
    global Board, Number_move
    move_tmp = (0, 0)
    best_score = ""
    
    expect_move = get_expect_move()
    for move_tmp in expect_move:
        x, y = move_tmp
        if best_score == "":
            score = AI_calc_score(x, y)
            best_score = score
            move = move_tmp
        else:
            score = AI_calc_score(x, y)
            if score > best_score:
                best_score = score
                move = move_tmp
    return move


def is_win():
    global Win
    black = score_all('b')
    white = score_all('w')

    sum_sumcol_values(black)
    sum_sumcol_values(white)

    if 5 in black and black[5] == 1:
        Win = 'b'
        print("Player win")
        return True
    elif 5 in white and white[5] == 1:
        Win = 'w'
        print("AI win")
        return True
    
    return False


# Graphics Engine
def click(x, y):
    global Win, Number_move, Board, Move_history, Colors
    # print(round(x), round(y))

    if abs(x - round(x)) > 0.4 or abs(y - round(y)) > 0.4 or Win != 0:
        return
    x, y = round(x), round(y)

    if Board[x][y] == '':
        draw_stone(x, y, 'b')
        Board[x][y] = 'b'
        Number_move += 1
        Move_history.append((x, y))
        if is_win(): # Check if black win
            return
        # AI's turn
        ax, ay = best_move()
        draw_stone(ax, ay, 'w')
        Board[ax][ay] = 'w'
        Number_move += 1
        Move_history.append((ax, ay))
        if is_win(): # Check if white win
            return


def init():
    global BOARD_SIZE, WIN, FIRST_HIT, PLAYER_COLOR
    global Win, Number_move, Board, Move_history, Colors
    size = BOARD_SIZE

    # Make empty board
    Board = []
    for i in range(size):
        Board.append(['']*size)

    screen = turtle.Screen()
    screen.title("Caro Game")
    screen.bgcolor("orange")
    screen.setup(0.5, 0.75)
    # print(screen.screensize())
    # > (400, 300) ???
    screen.onclick(click)
    screen.setworldcoordinates(-1, size, size, -1)
    screen.tracer(5, 0)

    Colors = {'w': turtle.Turtle(), 'b': turtle.Turtle()}
    if PLAYER_COLOR == 'b':
        Colors['w'].color("white")
        Colors['b'].color("black")
    else:
        Colors['w'].color("black")
        Colors['b'].color("white")
    for key in Colors:
        Colors[key].ht()
        Colors[key].speed(0)
        Colors[key].penup()

    # Draw board
    border = turtle.Turtle()
    border.ht()
    border.penup()
    for start in range(size + 1):
        border.goto(start - 0.5, -0.5)
        border.pendown()
        border.goto(start - 0.5, size - 1 + 0.5)
        border.penup()

    for start in range(size + 1):
        border.goto(-0.5, start - 0.5)
        border.pendown()
        border.goto(size - 0.5, start - 0.5)
        border.penup()
    if FIRST_HIT == 1:
        mid = int(BOARD_SIZE/2) - 1
        q = int(BOARD_SIZE/4) - 1
        x, y = (mid + random.randint(-q, q), mid + random.randint(-q, q))
        draw_stone(x, y, 'w')
        Board[x][y] = 'w'
        Number_move += 1
        Move_history.append((x, y))
# ----------------------------------------------------------------
    bw = 'b'
    while (Win == 0) :
        if bw == 'b':
            bw = 'w'
        else:
            bw = 'b'
        x, y = best_move()
        draw_stone(x, y, bw)
        Board[x][y] = bw
        # Number_move += 1
        # Move_history.append((x, y))
        if is_win(): # Check if white win
            break
# ----------------------------------------------------------------
    screen.listen()
    screen.mainloop()

def draw_stone(x, y, bw):
    global Colors
    Colors[bw].goto(x, y - 0.3)
    Colors[bw].pendown()
    Colors[bw].begin_fill()
    Colors[bw].circle(0.3)
    Colors[bw].end_fill()
    Colors[bw].penup()


if __name__ == "__main__":
    print("Welcome to Caro game!")
    init()