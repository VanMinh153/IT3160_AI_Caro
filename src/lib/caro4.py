import lib.Settings as S
import lib.Shared_Variable as V


# AI Engine
def forward(x, y, dx, dy, length):
    """
    Return the point with coordinates (x2,y2) = (x,y) + length*(dx,dy) if the point is within the board,
    otherwise reduce the length.
    """
    x2 = x + length * dx
    y2 = y + length * dy
    while not (0 <= x2 < S.BOARD_SIZE and 0 <= y2 < S.BOARD_SIZE):
        x2 -= dx
        y2 -= dy

    return x2, y2


def get_score_sum(score_dict):
    """
    Merge scores from each direction.
    """
    for key in score_dict:
        if key == 4:  # Adjust for 4 in line
            score_dict[4] = int(1 in score_dict[4].values())
        else:
            score_dict[key] = sum(score_dict[key].values())


def score_section(begin_point, dx, dy, end_point, bw):
    """
    Return a list with each element representing the score of 4 blocks.
    (dx, dy) = direction vector from begin_point to end_point
    """
    x, y = begin_point
    xf, yf = end_point
    # Get line from begin_point to end_point
    line = [V.Board[x][y]]
    while x != xf or y != yf:
        x += dx
        y += dy
        line.append(V.Board[x][y])

    line_score = []
    for i in range(len(line) - (S.WIN - 1)):  # Adjust for S.WIN
        blank = line[i: i + S.WIN].count('')
        hit = line[i: i + S.WIN].count(bw)
        if blank + hit != S.WIN:  # opponent has a hit in this line
            score = -1
        else:
            score = hit
        line_score.append(score)

    return line_score


def score_all(bw):
    """
    Calculate scores in all directions for bw.
    """
    END = S.BOARD_SIZE - 1
    # scores of 4 directions
    score = {(1, 0): [], (0, 1): [], (1, 1): [], (-1, 1): []}
    for i in range(S.BOARD_SIZE):
        score[(1, 0)] += score_section((0, i), 1, 0, (END, i), bw)
        score[(0, 1)] += score_section((i, 0), 0, 1, (i, END), bw)

    score[(1, 1)] += score_section((0, 0), 1, 1, (END, END), bw)
    score[(-1, 1)] += score_section((0, END), 1, -1, (END, 0), bw)
    for i in range(1, S.BOARD_SIZE - (S.WIN - 1)):
        score[(1, 1)] += score_section((i, 0), 1, 1, (END, END - i), bw)
        score[(1, 1)] += score_section((0, i), 1, 1, (END - i, END), bw)
        score[(-1, 1)] += score_section((i, END), 1, -1, (END, i), bw)

    for i in range(S.WIN - 1, S.BOARD_SIZE):
        score[(-1, 1)] += score_section((i, 0), -1, 1, (0, i), bw)

    return score_combine(score)


def score_point(x, y, bw):
    """
    Return the score of a column in x, y in 4 directions,
    key: score of that unit block -> only check 4 blocks instead of all
    """

    score = {(0, 1): [], (-1, 1): [], (1, 0): [], (1, 1): []}

    score[(1, 0)] += score_section(forward(x, y, -1, 0, 3), 1, 0, forward(x, y, 1, 0, 3), bw)  # Adjust for 4 in line
    score[(0, 1)] += score_section(forward(x, y, 0, -1, 3), 0, 1, forward(x, y, 0, 1, 3), bw)  # Adjust for 4 in line
    score[(1, 1)] += score_section(forward(x, y, -1, -1, 3), 1, 1, forward(x, y, 1, 1, 3), bw)  # Adjust for 4 in line
    score[(-1, 1)] += score_section(forward(x, y, -1, 1, 3), 1, -1, forward(x, y, 1, -1, 3), bw)  # Adjust for 4 in line

    return score_combine(score)

def score_combine(score_all: object):
    """
    Khởi tạo hệ thống điểm
    :type score_all: object
    """
    score_sum = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, -1: {}}
    for key in score_all:
        for score in score_all[key]:
            if key in score_sum[score]:
                score_sum[score][key] += 1
            else:
                score_sum[score][key] = 1

    return score_sum


def TF34score(score2, score3):
    """
    trả lại trường hợp chắc chắn có thể thắng(4 ô liên tiếp)
    """
    for key3 in score3:
        if score3[key3] >= 1:
            for key2 in score2:
                if key2 != key3 and score2[key2] >= 2:
                    return True
    return False


def win_situation(score_sum):
    """
    Return the win situation like:
    {0: {}, 1: {(0, 1): 3, (-1, 1): 2, (1, 0): 3, (1, 1): 3}, 2: {}, 3: {}, 4: {}, -1: {}}
    1-4 stores scores from low to high danger level,
    -1 is in bad state, need defense
    """

    if 1 in score_sum[4].values(): 
        return 4
    elif len(score_sum[3]) >= 2 or (len(score_sum[3]) >= 1 and max(score_sum[3].values()) >= 2):
        return 3
    else:
        score3 = sorted(score_sum[3].values(), reverse=True)
        if len(score3) >= 2 and score3[0] >= score3[1] >= 2:
            return 3
    return 0


def AI_calc_score(x, y):
    """
    Try to move x, y
    Return representative advantage score
    """
    Multiplier = 10000
    result, attack, defense = 0, 0, 0
    # attack
    V.Board[x][y] = 'w'
    scores = score_point(x, y, 'w')
    a = win_situation(scores)
    attack += a * Multiplier
    get_score_sum(scores)
    attack += (
            scores[-1]
            + scores[1]
            + 4 * scores[2]
            + 8 * scores[3]
            # + 16 * scores[4]
            )

    # defense
    V.Board[x][y] = 'b'
    scores = score_point(x, y, 'b')
    d = win_situation(scores)
    defense += d * (Multiplier - 100)
    get_score_sum(scores)
    defense += (
            scores[-1]
            + scores[1]
            + 4 * scores[2]
            + 8 * scores[3]
            # + 16 * scores[4]
            )

    result = attack + defense
    V.Board[x][y] = ''
    return result


def get_expect_move():
    """
    1: Get hit cells
    2: Get x_min -> x_max, y_min -> y_max coordinates of the rectangle surrounding the hit cells
    3: Return cells that can be moved within a wider range of 4 cells each direction of that rectangle
    """
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

    x_min2 = x_min - 4
    x_max2 = x_max + 4
    y_min2 = y_min - 4
    y_max2 = y_max + 4
    while x_min2 < 0:
        x_min2 += 1
    while x_max2 >= S.BOARD_SIZE:
        x_max2
        unhit = []
    for i in range(x_min, x_max + 1):
        for j in range(y_min, y_max + 1):
            if V.Board[i][j] == '':
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
    global move
    (0, 0)
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
