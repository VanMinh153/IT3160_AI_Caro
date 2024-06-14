# Interface_Turtle.py

import turtle
import random
import lib.Settings as S
import lib.Shared_Variable as V
from lib.AI_Minimax import best_move
from lib.Win_State import check_win

Colors = {}

def click(x, y):
    print(f"Click at: {round(x)}, {round(y)}")

    if abs(x - round(x)) > 0.4 or abs(y - round(y)) > 0.4 or V.Win != '':
        return
    x, y = round(x), round(y)

    if V.Board[x][y] == '':
        draw_stone(x, y, 'b')
        V.Board[x][y] = 'b'
        V.Number_move += 1
        V.Move_history.append((x, y))
        if check_win():  # Check if black wins
            V.Win = 'b'
            print("Player wins")
            display_winner("Player Wins!")
            return
        # AI's turn
        ax, ay = best_move()
        draw_stone(ax, ay, 'w')
        V.Board[ax][ay] = 'w'
        V.Number_move += 1
        V.Move_history.append((ax, ay))
        if check_win():  # Check if white wins
            V.Win = 'w'
            print("AI wins")
            display_winner("AI Wins!")
            return

def display_winner(winner_text):
    """
    Display the winner on the screen
    """
    winner_turtle = turtle.Turtle()
    winner_turtle.hideturtle()
    winner_turtle.penup()
    winner_turtle.goto(S.BOARD_SIZE / 2 - 3, -1)
    winner_turtle.write(winner_text, align="center", font=("Arial", 24, "bold"))

def start_game(x, y):
    """
    Start the game by initializing the board and setting up the click event
    """
    
    print("Game started")

    global Colors
    
    size = S.BOARD_SIZE

    # Clear any existing drawings
    turtle.clearscreen()

    # Make empty board
    V.Board = [['' for _ in range(size)] for _ in range(size)]
    V.Move_history = []
    V.Number_move = 0
    V.Win = ''

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
        border.goto(start - 0.5, size - 0.5)
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

def draw_stone(x, y, bw):
    global Colors
    Colors[bw].goto(x, y - 0.3)
    Colors[bw].pendown()
    Colors[bw].begin_fill()
    Colors[bw].circle(0.3)
    Colors[bw].end_fill()
    Colors[bw].penup()

def init():
    """
    Initialize the screen with a "Play" button
    """
    screen = turtle.Screen()
    screen.title("Caro Game")
    screen.bgcolor("orange")
    screen.setup(width=600, height=600)

    play_button = turtle.Turtle()
    play_button.shape("square")
    play_button.shapesize(stretch_wid=2, stretch_len=4)
    play_button.color("green")
    play_button.penup()
    play_button.goto(0, 0)

    text_turtle = turtle.Turtle()
    text_turtle.hideturtle()
    text_turtle.penup()
    text_turtle.goto(0, -10)
    text_turtle.write("Play", align="center", font=("Arial", 16, "bold"))

    def on_play_click(x, y):
        print("Play button clicked")
        play_button.clear()
        play_button.hideturtle()
        text_turtle.clear()
        start_game(x, y)

    play_button.onclick(on_play_click)

    screen.mainloop()
