
import copy

VIC = 10 ** 20  # The value of a winning board (for max)
LOSS = -VIC  

SIZE = 4  
'''
The state of the game is represented by a list of 2 items:
0. The game board - a matrix (list of lists) of strings. 
   An empty cell = space and an occupied cell = #
1. Who's turn is it: "Human" or "Computer"
'''


def create():
    # Returns an empty board. The human plays first.
    board = []
    for i in range(SIZE):
        board = board + [SIZE * ["#"]]
    return [board, "Human"]

"""
The function first checks if the game is about to finish, and also if we have a state of 2x2 board,
so in that case the second player wil always win (notice that 2x2 is not necessarily four adjacent cards but any two 
different pairs of cards or four completely separate cards), the function returns a positive or negative (1 or -1) value
according to the next player. The function also returns a positive/negative value if there is only one card left.
We can see that the heuristic is admissible since it returns a positive value only when the computer is guaranteed 
victory and vice versa.
"""
def value(s):
    if isFinished(s):
        if s[1] == "Human":
            return VIC
        else:
            return LOSS
    def is_2x2_or_separated_4(board):
        for r in range(SIZE - 1):
            for c in range(SIZE - 1):
                if (board[r][c] == '#' and board[r][c + 1] == '#' and
                        board[r + 1][c] == '#' and board[r + 1][c + 1] == '#'):
                    return True
        separate_cards = [(r, c) for r in range(SIZE) for c in range(SIZE) if board[r][c] == '#']
        if len(separate_cards) == 4:
            for i in range(len(separate_cards)):
                for j in range(i + 1, len(separate_cards)):
                    r1, c1 = separate_cards[i]
                    r2, c2 = separate_cards[j]
                    if abs(r1 - r2) <= 1 and abs(c1 - c2) <= 1:
                        return False
            return True
        return False

    if is_2x2_or_separated_4(s[0]):
        if s[1] == "Human":
            return 1
        else:
            return -1
    rows_with_cards = sum(1 for row in s[0] if '#' in row)
    cols_with_cards = sum(1 for col in zip(*s[0]) if '#' in col)
    if rows_with_cards == 1 or cols_with_cards == 1:
        if s[1] == "Human":
            return -1
        else:
            return 1

    return 0


def printState(s):
    # Prints the board.
    for r in range(SIZE):
        print("abcdefghij"[r], end="")
        for c in range(SIZE):
            print(s[0][r][c], end="")
            if s[0][r][c] == "+":  # + indicates the computer's move
                s[0][r][c] = " "  # change to space after printing
        print()
    print(" 0123456789"[:SIZE + 1])

    if isFinished(s):
        if s[1] == "Human":
            print("I won.")
        else:
            print("You won.")


def isFinished(s):
    # Returns True iff the game ended
    for r in range(SIZE):
        for c in range(SIZE):
            if s[0][r][c] == "#":
                return False
    return True


def isHumTurn(s):
    # Returns True iff it the human's turn to play
    return s[1] == "Human"


def whoIsFirst(s):
    # The user decides who plays first
    if input("Who plays first? 1-me / anything else-you. : ") == "1":
        s[1] = "Computer"
    else:
        s[1] == "Human"


def inputMove(s):
    # Reads, enforces legality and executes the user's move.
    printState(s)
    flag = True
    while flag:
        move = input("The form of a single place is row and col without space (e.g. a1)\n\
        and for a range is row and col of the beginning and row and col for the end without space (e.g. a1a3)\n\
        Enter your next move: ")
        flag = not isLegal(s, move, " ")


def getNext(s):
    # returns a list of the next states of s
    ns = []
    for r in range(SIZE):
        for c in range(SIZE):
            c1 = c
            st = copy.deepcopy(s)
            if st[1] == "Human":
                st[1] = "Computer"
                # x is the sign for cards taken at the current move
                x = " "
            else:
                st[1] = "Human"
                x = "+"
            while c1 < SIZE and st[0][r][c1] == "#":
                st[0][r][c1] = x
                ns += [copy.deepcopy(st)]
                c1 += 1
            r1 = r
            st = copy.deepcopy(s)
            if st[1] == "Human":
                st[1] = "Computer"
                x = " "
            else:
                st[1] = "Human"
                x = "+"
            while r1 < SIZE and st[0][r1][c] == "#":
                st[0][r1][c] = x
                if r1 > r:  # To prevent multiplications
                    ns += [copy.deepcopy(st)]
                r1 += 1
    return ns


##############################################
# Check if move is legal in state s and if so will put x in the new empty cell/s
def isLegal(s, move, x):
    # Convert move to coordinates
    if len(move) % 2 != 0 or len(move) < 2 or len(move) > SIZE * 2:
        return False  # Invalid move format
    positions = [(move[i], move[i + 1]) for i in range(0, len(move), 2)]
    try:
        positions = [("abcdefghij".index(pos[0]), int(pos[1])) for pos in positions]
    except (ValueError, IndexError):
        return False  # Invalid position values
    # Check if all positions are in the same row or column
    rows = [pos[0] for pos in positions]
    cols = [pos[1] for pos in positions]
    if not (all(r == rows[0] for r in rows) or all(c == cols[0] for c in cols)):
        return False
    # Check if all positions contain '#'
    for r, c in positions:
        if s[0][r][c] != "#":
            return False
    # Check if positions are contiguous
    if all(r == rows[0] for r in rows):
        # All positions in the same row
        if sorted(cols) != list(range(min(cols), max(cols) + 1)):
            return False
    else:
        # All positions in the same column
        if sorted(rows) != list(range(min(rows), max(rows) + 1)):
            return False
    for r, c in positions:
        s[0][r][c] = x
    s[1] = "Human" if s[1] == "Computer" else "Computer"
    return True
