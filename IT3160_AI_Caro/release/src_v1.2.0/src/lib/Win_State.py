import lib.Settings as S
import lib.Shared_Variable as V

x, y = 0, 0
bw = ''
v1 = []
v2 = []
for i in range(1, S.WIN):
    v1.append(i)
for i in range(-1, -S.WIN, -1):
    v2.append(i)

def check_win():
    global x, y, bw
    x, y = V.Move_history[-1]
    bw = V.Board[x][y]
    
    if check_win_f(1, 0):
        return True
    if check_win_f(0, 1):
        return True
    if check_win_f(1, 1):
        return True
    if check_win_f(1, -1):
        return True
    return False

def check_win_f(dx, dy):
    global x, y, bw
    w = 1
    for i in v1:
        try:
            if V.Board[x + i*dx][y + i*dy] == bw:
                w += 1
            else:
                break
        except IndexError:
            None
    
    if w == S.WIN:
        return True
    
    for i in v2:
        try:
            if V.Board[x + i*dx][y + i*dy] == bw:
                w += 1
            else:
                break
        except IndexError:
            None
    
    if w == S.WIN:
        return True
    
    return False
