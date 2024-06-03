import turtle
import random
import lib.Settings as S
import lib.Shared_Variable as V
from lib.AI_Minimax import best_move
from lib.Win_State import check_win

Colors = {}


# Graphics Engine
def click(x, y):
    print(round(x), round(y))

    if abs(x - round(x)) > 0.4 or abs(y - round(y)) > 0.4 or V.Win != '':
        return
    x, y = round(x), round(y)

    if V.Board[x][y] == '':
        draw_stone(x, y, 'b')
        V.Board[x][y] = 'b'
        V.Number_move += 1
        V.Move_history.append((x, y))
        if check_win():  # Check if black win
            V.Win = 'b'
            print("Player wins")
            return
        # AI's turn
        ax, ay = best_move()
        draw_stone(ax, ay, 'w')
        V.Board[ax][ay] = 'w'
        V.Number_move += 1
        V.Move_history.append((ax, ay))
        if check_win():  # Check if white win
            V.Win = 'w'
            print("AI wins")
            return


def init():
    global Colors
    size = S.BOARD_SIZE

    # Make empty board
    V.Board = []
    for i in range(size):
        V.Board.append([''] * size)

    screen = turtle.Screen()
    screen.title("Caro Game")
    screen.bgcolor("orange")
    screen.onclick(click)
    screen.setworldcoordinates(-1, size, size, -1)
    screen.tracer(5, 0)

    Colors = {'w': turtle.Turtle(), 'b': turtle.Turtle()}
    if S.PLAYER_COLOR == 'b':
        Colors['w'].color("white")
        Colors['b'].color("black")
    else:
        Colors['w'].color("black")
        Colors['b'].color("white")
    for key in Colors:
        Colors[key].ht()
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
    if S.FIRST_HIT == 1:
        mid = int(S.BOARD_SIZE / 2) - 1
        q = int(S.BOARD_SIZE / 4) - 1
        x, y = (mid + random.randint(-q, q), mid + random.randint(-q, q))
        draw_stone(x, y, 'w')
        V.Board[x][y] = 'w'
        V.Number_move += 1
        V.Move_history.append((x, y))

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
