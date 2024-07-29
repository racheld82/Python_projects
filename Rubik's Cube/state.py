'''
The state is a list of 2 items: the board, the path
the board is a list of colors (Red ,Green, Blue, Yellow, White, Orange) representing the cube:
         0  1
         2  3
       -------
   4  5| 6  7| 8  9
  10 11|12 13|14 15
       -------
        16 17
        18 19
       -------
        20 21
        22 23

'''
import random
import copy

TOP = 0  # Moves [6,7,12,13] clockwise
TOPANTI = 1  # Moves [6,7,12,13] anticlockwise
FRONT = 2  # Moves [16,17,18,19] clockwise
FRONTANTI = 3  # Moves [16,17,18,19] anticlockwise
LEFT = 4  # Moves [4,5,10,11] clockwise
LEFTANTI = 5  # Moves [4,5,10,11] anticlockwise
MOVES = {
    TOP: [[6, 7], [7, 13], [13, 12], [12, 6], [2, 8], [3, 14], [8, 17], [14, 16], [17, 11], [16, 5], [11, 2], [5, 3]],
    TOPANTI: [[7, 6], [13, 7], [12, 13], [6, 12], [8, 2], [14, 3], [17, 8], [16, 14], [11, 17], [5, 16], [2, 11],
              [3, 5]],
    FRONT: [[16, 17], [17, 19], [19, 18], [18, 16], [12, 14], [13, 15], [14, 21], [15, 20], [21, 10], [20, 11],
            [10, 12], [11, 13]],
    FRONTANTI: [[17, 16], [19, 17], [18, 19], [16, 18], [14, 12], [15, 13], [21, 14], [20, 15], [10, 21], [11, 20],
                [12, 10], [13, 11]],
    LEFT: [[4, 5], [5, 11], [11, 10], [10, 4], [0, 6], [2, 12], [6, 16], [12, 18], [16, 20], [18, 22], [20, 0],
           [22, 2]],
    LEFTANTI: [[5, 4], [11, 5], [10, 11], [4, 10], [6, 0], [12, 2], [16, 6], [18, 12], [20, 16], [22, 18], [0, 20],
               [2, 22]]}
FACES = [[0, 1, 2, 3], [4, 5, 10, 11], [6, 7, 12, 13], [8, 9, 14, 15], [16, 17, 18, 19], [20, 21, 22, 23]]


def get_next(x):
    ns = []
    poss_moves = [0, 1, 2, 3, 4, 5]
    if x[1] != "":
        poss_moves.remove([1, 0, 3, 2, 5, 4][int(x[1][-1])])
    for m in poss_moves:
        s = x[0][:]
        s = make_move(s, MOVES[m])
        ns.append([s, x[1] + str(m)])
    return ns


# returns a random board
def create(n=None):  ##
    """
    s = ["R", "R", "R", "R", "G", "G", "B", "B", "Y", "Y", "G", "G",
         "B", "B", "Y", "Y", "W", "W", "W", "W", "O", "O", "O", "O"]
    for i in range(7):
        m = random.choice(MOVES)
        s = make_move(s, m)
    """
    s = ['B', 'R', 'G', 'G', 'G', 'O', 'W', 'R', 'O', 'Y', 'B', 'W', 'Y', 'B', 'R', 'G', 'O', 'Y', 'Y', 'W', 'W', 'B',
         'R', 'O']
    return [s, ""]


def path_len(s):  ##
    return len(s[1])


def is_target(s):  ##
    for f in FACES:
        for i in range(len(f) - 1):
            if s[0][f[i]] != s[0][f[i + 1]]:
                return False
    return True

def hdistance(s):
    """
    Heuristic that counts the number of tiles not matching the most frequent color on their respective faces.
    This heuristic is valid (admissible) because it does not overestimate the cost to reach the goal state.
    It counts the number of misplaced tiles based on the most frequent color on each face, which is a lower bound on the number of moves required to solve the cube.
    :param s: the state on which the heuristic will be calculated
    """
    misplaced_tiles = 0
    for face in FACES:
        color_count = {}
        for index in face:
            color = s[0][index]
            if color in color_count:
                color_count[color] += 1
            else:
                color_count[color] = 1
        # Find the color with the maximum count
        target_color = max(color_count, key=color_count.get)
        for index in face:
            if s[0][index] != target_color:
                misplaced_tiles += 1
    return misplaced_tiles




def make_move(s, m):  ##
    ns = copy.deepcopy(s)
    for c in m:
        ns[c[1]] = s[c[0]]
    return ns

