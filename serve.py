
from flask import (Flask, render_template, request, jsonify)

from strategy import create_board, computer_play, is_win_state

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('index.html')


@app.route('/game', methods=['GET', 'POST'])
def game():
    """A REST adaptation discusses state of a
    Tic-Tac-Toe game with an external player."""

    # A `GET` to the API simply returns a new, blank game.
    if request.method == 'GET':
        return jsonify(board_state=create_board(),
                       win=(False, None))

    # If API is accessed with a `POST`, it is the external
    # player submitting his move.
    elif request.method == 'POST':
        board_state = request.json['board_state']

        # Check if the human has won or tied the game.
        win = is_win_state(board_state)
        if win[0]:
            return jsonify(board_state=board_state, win=win)
        else:
            board_state[computer_play(board_state)] = 'O'
            return jsonify(board_state=board_state, win=is_win_state(board_state))


if __name__ == "__main__":

    # Explicitly bind to 0.0.0.0 so I can access
    # across network on my phone
    app.run(host='0.0.0.0')
