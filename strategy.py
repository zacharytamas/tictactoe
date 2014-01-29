
import random

MIDDLE = 4
WINNING_MASKS = [
    73, 146, 292,  # Vertical wins
    7, 56, 448,    # Horizontal wins
    273, 84        # Diagonal wins
]
CORNERS = [0, 2, 6, 8]
EDGES = [1, 3, 5, 7]
OPPOSITE_CORNER = {
    0: 8,
    2: 6,
    6: 2,
    8: 0
}
CORNER_PLAYS = {
    (5, 7): 8,
    (1, 3): 0,
    (1, 5): 2,
    (3, 7): 6
}
LATERAL_CORNERS = {
    0: [2, 6],
    2: [0, 8],
    6: [0, 8],
    8: [2, 6]
}


def is_win_state(board_state):
    """
    Returns whether the current board state is a winning state.

    Output: Tuple of 3 values.
    Tuple of two values
    (<X|O|TIE|None>, <mask of winning state that was met>)

    # Board is empty
    >>> is_win_state([None] * 9)
    (None, None)

    # Horizontal wins
    >>> is_win_state(['X', 'X', 'X'] + [None] * 6)
    ('X', 7)
    >>> is_win_state([None] * 3 + ['X', 'X', 'X'] + [None] * 3)
    ('X', 56)
    >>> is_win_state([None] * 6 + ['X', 'X', 'X'])
    ('X', 448)

    # Vertical wins
    >>> is_win_state(['O', None, None] * 3)
    ('O', 73)
    >>> is_win_state([None, 'O', None] * 3)
    ('O', 146)
    >>> is_win_state([None, None, 'O'] * 3)
    ('O', 292)

    # Diagonal wins
    >>> is_win_state(['X', None, None, None] * 3)
    ('X', 273)
    >>> is_win_state([None, None, 'X', None, 'X', None, 'X', None, None])
    ('X', 84)

    # Ties
    >>> is_win_state(list('XOOOXXOXO'))
    ('TIE', None)
    >>> is_win_state(list('OOXXXOOXO'))
    ('TIE', None)
    """

    masks = { 'X': 0, 'O': 0 }

    for i, cell in enumerate(board_state):
        if cell is not None:
            masks[cell] |= 1 << i

    for mask in WINNING_MASKS:
        for player in ['X', 'O']:
            if masks[player] & mask == mask:
                return (player, mask)

    # If all squares are filled yet there is no
    # winner, it is a tie.
    if all(board_state):
        return ('TIE', None)

    return (None, None)


def _look_for(board_state, needle='X'):
    """Accepts a board_state and a square value that it is
    looking for. It attempts to find columns, rows, and
    diagonals where the needle occurs twice accompanied
    by an empty square. If so, returns that empty square's
    number. If not, returns False.

    >>> _look_for(string_state_to_list('XX-------'), 'X')
    2
    >>> _look_for(string_state_to_list('---X-X---'), 'X')
    4
    >>> _look_for(string_state_to_list('X--X-----'), 'X')
    6
    >>> _look_for(string_state_to_list('-X--X----'), 'X')
    7
    >>> _look_for(string_state_to_list('--X--X---'), 'X')
    8
    >>> _look_for(string_state_to_list('--X-----X'), 'X')
    5
    >>> _look_for(string_state_to_list('-X-------'), 'X')
    False
    """

    # Horizontals
    for i in range(3):
        row_start = 3 * i
        row = board_state[row_start:row_start + 3]
        if row.count(None) and row.count(needle) == 2:
            return row_start + row.index(None)

    # Verticals
    for i in range(3):
        col = board_state[i:9:3]
        if col.count(None) and col.count(needle) == 2:
            return col.index(None) * 3 + i

    # Diagonals
    if board_state[MIDDLE] == needle:
        for i in CORNERS:
            if board_state[i] is None and board_state[OPPOSITE_CORNER[i]] == needle:
                return i

    return False


def can_win(board_state):
    """Accepts a board state and inspects it for winning
    opportunities. Returns the square number where the
    win can occur, or False if no win can happen."""
    return _look_for(board_state, 'O')


def should_block(board_state):
    """Accepts a board state, inspects it for the need
    to block the human player. If a block is needed,
    returns number of square needing block, otherwise
    return False."""
    return _look_for(board_state, 'X')


def computer_play(board_state):

    highest = -2
    possibilities = []
    plays = len(filter(None, board_state))

    # If none of the squares are occupied, select
    # the middle square.
    if not any(board_state) or board_state[MIDDLE] is None:
        return MIDDLE

    # If the human has played the center, choose a random corner.
    if plays == 1: return random.choice(CORNERS)

    # If we can win, do so.
    win = can_win(board_state)
    if win is not False: return win

    # If we can block, do so.
    block = should_block(board_state)
    if block is not False: return block

    # Check for corner plays and play them if they're available.
    for a, b in CORNER_PLAYS.keys():
        if [board_state[a], board_state[b]] == ['X', 'X']:
            square_to_mark = CORNER_PLAYS[(a, b)]
            if board_state[square_to_mark] is None:
                return square_to_mark

    if plays == 3:
        # If we own the middle square but the human owns two
        # opposing corners, we must claim one of the edges
        # to ensure a tie.
        if board_state[MIDDLE] == 'O':
            for corner in CORNERS:
                if [board_state[corner], board_state[OPPOSITE_CORNER[corner]]] == ['X', 'X']:
                    return random.choice(EDGES)

        # If the human owns the middle and a corner, we need
        # to play one of the corners lateral to their corner
        # in order to prevent them from setting up a situation
        # where they can win two different ways.
        elif board_state[MIDDLE] == 'X':
            for corner in CORNERS:
                if board_state[corner] == 'X':
                    for c in LATERAL_CORNERS[corner]:
                        if board_state[c] is None:
                            return c

    # If we haven't identified a situation, use minimax to
    # find possible routes.
    for possibility, square in visitable_states(board_state):

        score = state_score(possibility, player='O')

        # If this possibility's score is higher than we've
        # found before, reset the possibilities list with this one.
        if score > highest:
            highest = score
            possibilities = [square]

        # If this possibility's score is the same as the
        # current highest, it is equally likely to lead to
        # a win for us. Add it to the list of possibilities.
        elif score == highest:
            possibilities.append(square)

    return random.choice(possibilities)


def state_score(board_state, player='O', depth=0):
    winner, win_state = is_win_state(board_state)

    # Recursion base-cases: return score of favorability
    if winner == 'X':
        return -1
    elif winner == 'TIE':
        return 0
    elif winner == 'O':
        return 1

    if player == 'O':
        best_bet = float('-inf')
    else:
        best_bet = float('inf')

    remaining = []
    for i, square in enumerate(board_state):
        if square is None:
            remaining.append(i)

    for square in remaining:
        state = board_state[:]
        state[square] = player

        score = state_score(state, opponent(player), depth + 1)
        if player == 'O':
            best_bet = max([score, best_bet])
        elif player == 'X':
            best_bet = min([score, best_bet])

    return best_bet


def opponent(who):
    """
    >>> opponent('X')
    'O'
    >>> opponent('O')
    'X'
    """
    if who == 'X': return 'O'
    return 'X'

#
# Testing utilities
#

def string_state_to_list(board_state_string):
    """
    >>> string_state_to_list('XOOOXXOXO')
    ['X', 'O', 'O', 'O', 'X', 'X', 'O', 'X', 'O']
    >>> string_state_to_list('X--------')
    ['X', None, None, None, None, None, None, None, None]
    >>> string_state_to_list('X-O-XXXXX')
    ['X', None, 'O', None, 'X', 'X', 'X', 'X', 'X']
    """
    return map(lambda c: c if c != '-' else None, list(board_state_string))

def create_board():
    """
    >>> create_board()
    [None, None, None, None, None, None, None, None, None]
    """
    return [None] * 9

def visitable_states(board_state, player='X'):
    """
    >>> visitable_states([None])
    [(['X'], 0)]
    >>> visitable_states([None, None])
    [(['X', None], 0), ([None, 'X'], 1)]
    >>> visitable_states([None, None, 'O'])
    [(['X', None, 'O'], 0), ([None, 'X', 'O'], 1)]
    """
    possibilities = []

    for i, square in enumerate(board_state):
        if square is None:
            temp = board_state[:]
            temp[i] = player
            possibilities.append((temp, i))

    return possibilities


def exhaustive_search():
    """Performs a breadth-first, exhaustive search of
    the whole problem space to prove the correctness of
    this algorithm. Will stop immediately when it loses
    a game, which it should never."""

    # Seed the search frontier with all the visitable
    # states at the start: that is, one where one X is
    # placed in every available square.
    frontier = [[i[0]] for i in visitable_states(create_board())]
    winning = True

    while len(frontier) and winning:
        state_chain = frontier.pop()
        board_state = state_chain[-1]

        winning = is_win_state(board_state)
        if winning[0] in ['TIE', 'O']:
            continue
        elif winning[0] == 'X':
            print "Test failed. Human won."
            print state_chain
            winning = False
            continue

        # Get the computer's counter play to this
        # state and play it.
        computer_response = computer_play(board_state)
        board_state[computer_response] = 'O'

        winning = is_win_state(board_state)
        if winning[0] in ['TIE', 'O']:
            continue

        # Add to the search frontier all the states that
        # are visitable from this one. We'll search those
        # states later.
        for p_state in visitable_states(board_state):
            p_state_chain = state_chain[:]
            p_state_chain.append(p_state[0])
            frontier.append(p_state_chain)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    exhaustive_search()
