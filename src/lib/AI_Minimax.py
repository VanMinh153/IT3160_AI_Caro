import lib.Settings as S
import lib.Shared_Variable as V


# AI Engine
def forward(x, y, dx, dy, len):
    """
    trả về điểm có toạ độ (x2,y2) = (x,y) + length*(dx,dy) nếu điểm đó nằm trong bàn cờ
    , nếu không thì giảm length
    """
    x2 = x + len * dx
    y2 = y + len * dy
    while not (0 <= x2 < S.BOARD_SIZE and 0 <= y2 < S.BOARD_SIZE):
        x2 -= dx
        y2 -= dy

    return (x2, y2)


def get_score_sum(score_dict):
    """
    hợp nhất điểm của mỗi hướng
    """
    for key in score_dict:
        if key == 5:
            score_dict[5] = int(1 in score_dict[5].values())
        else:
            score_dict[key] = sum(score_dict[key].values())


def score_section(begin_point, dx, dy, end_point, bw):
    """
    trả về một list với mỗi phần tử đại diện cho số điểm của 5 khối
    (dx, dy) = vector hướng từ begin_point đến end_point
    """
    x, y = begin_point
    xf, yf = end_point
    # Get line from begin_point to end_point
    line = []
    line.append(V.Board[x][y])
    while x != xf or y != yf:
        x += dx
        y += dy
        line.append(V.Board[x][y])

    line_score = []
    for i in range(len(line) - (S.WIN - 1)):
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
    tính toán điểm số mỗi trên toàn bộ các hướng của bw
    """
    END = S.BOARD_SIZE - 1
    # scores của 4 hướng đi
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
    trả lại điểm số của column trong x,y theo 4 hướng,
    key: điểm số khối đơn vị đó -> chỉ ktra 5 khối thay vì toàn bộ
    """

    score = {(0, 1): [], (-1, 1): [], (1, 0): [], (1, 1): []}

    score[(1, 0)] += score_section(forward(x, y, -1, 0, 4), 1, 0, forward(x, y, 1, 0, 4), bw)
    score[(0, 1)] += score_section(forward(x, y, 0, -1, 4), 0, 1, forward(x, y, 0, 1, 4), bw)
    score[(1, 1)] += score_section(forward(x, y, -1, -1, 4), 1, 1, forward(x, y, 1, 1, 4), bw)
    score[(-1, 1)] += score_section(forward(x, y, -1, 1, 4), 1, -1, forward(x, y, 1, -1, 4), bw)

    return score_combine(score)


def score_combine(score_all):
    """
    Khởi tạo hệ thống điểm
    :type score_all: object
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


def win_situation(score_sum):
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
            + 16 * scores[4])

    # phòng thủ
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
            + 16 * scores[4])

    result = attack + defense
    V.Board[x][y] = ''
    return result


def get_expect_move():
    """
    1: Lấy những ô đã đánh
    2: lấy toạ độ x_min -> x_max, y_min -> y_max của hình chữ nhật bao quanh các ô đã đánh
    3: trả về các ô có thể đi trong phạm vi rộng hơn 4 ô mỗi chiều của hình chữ nhật đó
    """
    # mảng hit lưu những ô đã đánh, cả X và O
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
        x_max2 -= 1
    while y_min2 < 0:
        y_min2 += 1
    while y_max2 >= S.BOARD_SIZE:
        y_max2 -= 1

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
