import lib.Shared_Variable as V
from lib.AI_Minimax import score_all, get_score_sum

def is_win():
    black = score_all('b')
    white = score_all('w')

    get_score_sum(black)
    get_score_sum(white)

    if 5 in black and black[5] == 1:
        V.Win = 'b'
        print("Player win")
        return True
    elif 5 in white and white[5] == 1:
        V.Win = 'w'
        print("AI win")
        return True
    
    return False
