
import random

WINNING_MASKS = [
    73, 146, 292,  # Vertical wins
    7, 56, 448,    # Horizontal wins
    273, 84        # Diagonal wins
]


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
        for cell in ['X', 'O']:
            if masks[cell] & mask == mask:
                return (True, cell, mask)

    # If all squares are filled yet there is no
    # winner, it is a tie.
    if all(board_state):
        return (False, 'TIE', None)

    return (False, None, None)


def computer_play(board_state):
    available = []
    for i in range(len(board_state)):
        if board_state[i] is None:
            available.append(i)
    return random.choice(available)


#
# Testing utilities
#

def create_board():
    """
    >>> create_board()
    [None, None, None, None, None, None, None, None, None]
    """
    return [None] * 9

def possible_states_after_human(board_state):
    """
    >>> possible_states_after_human([None])
    [['X']]
    >>> possible_states_after_human([None, None])
    [['X', None], [None, 'X']]
    >>> possible_states_after_human([None, None, 'O'])
    [['X', None, 'O'], [None, 'X', 'O']]
    """
    possibilities = []

    for i, square in enumerate(board_state):
        if square is None:
            temp = board_state[:]
            temp[i] = 'X'
            possibilities.append(temp)

    return possibilities


def exhaustive_search():
    """Performs a breadth-first, exhaustive search of
    the whole problem space to prove the correctness of
    this algorithm. Will stop immediately when it loses
    a game, which it should never."""

    frontier = [[i] for i in possible_states_after_human(create_board())]
    wins = 0

    while len(frontier):
        state_chain = frontier.pop()
        board_state = state_chain[-1]

        winning = is_win_state(board_state)
        if winning[0] or winning[1] == 'TIE':
            if winning[1] in ['O', 'TIE']:
                wins += 1
                print "WON!", wins
                continue
            else:
                print "Test failed. Computer lost."
                print state_chain
                break

        computer_response = computer_play(board_state)
        board_state[computer_response] = 'O'

        winning = is_win_state(board_state)
        if winning[0] or winning[1] == 'TIE':
            if winning[1] in ['O', 'TIE']:
                wins += 1
                print "WON!", wins
                continue
            else:
                print "Test failed. Computer lost."
                print state_chain
                break

        for p_state in possible_states_after_human(board_state):
            p_state_chain = state_chain[:]
            p_state_chain.append(p_state)
            frontier.append(p_state_chain)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    exhaustive_search()
