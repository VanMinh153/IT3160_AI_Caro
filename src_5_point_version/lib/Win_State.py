import lib.Settings as S
import lib.Shared_Variable as V

_x, _y = 0, 0
bw = ''
v1 = []
v2 = []
for i in range(1, S.WIN):
    v1.append(i)
for i in range(-1, -S.WIN, -1):
    v2.append(i)

def check_win():
    global _x, _y, bw
    _x, _y = V.Move_history[-1]
    bw = V.Board[_x][_y]
    
    if V.Number_move == S.BOARD_SIZE*S.BOARD_SIZE:
        return "Draw"
    if check_win_f(1, 0):
        return "Win"
    if check_win_f(0, 1):
        return "Win"
    if check_win_f(1, 1):
        return "Win"
    if check_win_f(1, -1):
        return "Win"
    return 0

def check_win_f(dx, dy):
    global _x, _y, bw
    w = 1
    for i in v1:
        x, y = _x + i*dx, _y + i*dy
        if x < 0 or y < 0:
            break
        if x >= S.BOARD_SIZE or y >= S.BOARD_SIZE:
            break
        if V.Board[x][y] == bw:
            w += 1
        else:
            break
    
    if w == S.WIN:
        return True
    
    for i in v2:
        x, y = _x + i*dx, _y + i*dy
        if x < 0 or y < 0:
            break
        if x >= S.BOARD_SIZE or y >= S.BOARD_SIZE:
            break
        if V.Board[x][y] == bw:
            w += 1
        else:
            break
    
    if w == S.WIN:
        return True
    
    return False
