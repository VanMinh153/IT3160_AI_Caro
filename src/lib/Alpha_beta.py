import lib.Settings as S
import lib.Shared_Variable as V
import lib.Win_State as W

def alpha_beta_pruning(depth, alpha, beta, maximizing_player):
    if depth == 0 or W.check_win():
        return evaluate_board()

    if maximizing_player:
        max_eval = -float('inf')
        for move in get_expect_move():
            x, y = move
            V.Board[x][y] = 'w'
            eval = alpha_beta_pruning(depth - 1, alpha, beta, False)
            V.Board[x][y] = ''
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in get_expect_move():
            x, y = move
            V.Board[x][y] = 'b'
            eval = alpha_beta_pruning(depth - 1, alpha, beta, True)
            V.Board[x][y] = ''
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def evaluate_board():
    player_score = score_all('b')
    ai_score = score_all('w')

    player_sum = get_score_sum(player_score)
    ai_sum = get_score_sum(ai_score)

    player_total = (
            player_sum[1] * 1 +
            player_sum[2] * 10 +
            player_sum[3] * 100 +
            player_sum[4] * 1000 +
            player_sum[5] * 10000
    )

    ai_total = (
            ai_sum[1] * 1 +
            ai_sum[2] * 10 +
            ai_sum[3] * 100 +
            ai_sum[4] * 1000 +
            ai_sum[5] * 10000
    )

    return ai_total - player_total

def get_expect_move():
    hit = []
    x_min, x_max, y_min, y_max = 0, S.BOARD_SIZE - 1, 0, S.BOARD_SIZE - 1
    for i in range(S.BOARD_SIZE):
        for j in range(S.BOARD_SIZE):
            if V.Board[i][j] != '':
                hit.append((i, j))
                if i < x_min:
                    x_min = i
                elif i > x_max:
                    x_max = i
                if j < y_min:
                    y_min = j
                elif j > y_max:
                    y_max = j

    x_min2 = max(x_min - 4, 0)
    x_max2 = min(x_max + 4, S.BOARD_SIZE - 1)
    y_min2 = max(y_min - 4, 0)
    y_max2 = min(y_max + 4, S.BOARD_SIZE - 1)

    unhit = []
    for i in range(x_min2, x_max2 + 1):
        for j in range(y_min2, y_max2 + 1):
            if V.Board[i][j] == '':
                unhit.append((i, j))
    return unhit

def best_move_alpha_beta(depth):
    best_score = -float('inf')
    move = None
    for m in get_expect_move():
        x, y = m
        V.Board[x][y] = 'w'
        score = alpha_beta_pruning(depth - 1, -float('inf'), float('inf'), False)
        V.Board[x][y] = ''
        if score > best_score:
            best_score = score
            move = m
    return move
