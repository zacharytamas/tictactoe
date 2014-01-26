
WINNING_MASKS = [
    73, 146, 292,  # Vertical wins
    7, 56, 448,    # Horizontal wins
    273, 84        # Diagonal wins
]


def is_win_state(board_state):
    """
    Returns whether the current board state is a winning state.

    Output: Tuple of 3 values.
    (<whether is win or not>, <who won, if applicable>, <what winning state was met>)

    # Board is empty
    >>> is_win_state([None] * 9)
    (False, None, None)

    # Horizontal wins
    >>> is_win_state(['X', 'X', 'X'] + [None] * 6)
    (True, 'X', 7)
    >>> is_win_state([None] * 3 + ['X', 'X', 'X'] + [None] * 3)
    (True, 'X', 56)
    >>> is_win_state([None] * 6 + ['X', 'X', 'X'])
    (True, 'X', 448)

    # Vertical wins
    >>> is_win_state(['O', None, None] * 3)
    (True, 'O', 73)
    >>> is_win_state([None, 'O', None] * 3)
    (True, 'O', 146)
    >>> is_win_state([None, None, 'O'] * 3)
    (True, 'O', 292)

    # Diagonal wins
    >>> is_win_state(['X', None, None, None] * 3)
    (True, 'X', 273)
    >>> is_win_state([None, None, 'X', None, 'X', None, 'X', None, None])
    (True, 'X', 84)

    # Ties
    >>> is_win_state(list('XOOOXXOXO'))
    (False, 'TIE', None)
    >>> is_win_state(list('OOXXXOOXO'))
    (False, 'TIE', None)
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

if __name__ == "__main__":
    import doctest
    doctest.testmod()
