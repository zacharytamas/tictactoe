
# Tic Tac Toe submission

by Zachary Jones <zacharytamas@gmail.com>
* http://zacharytamas.me/
* https://github.com/zacharytamas

## Initial Thoughts

The problem statement for this project is pretty vague:

> Create a program that can interactively play the game of Tic-Tac-Toe against a human player and never lose.

I note that it says that the computer can never lose. I think that I will initially work towards a solution where the computer always attempts specifically to tie the player. My suspicion is that in doing this it will "accidentally" win sometimes, too. But that's alright.

Right now I'm thinking I'll use a derivation of the minimax algorithm since it's the de facto algorithm for zero-sum turn-taking games like this. I may try to find a more novel way of doing it later, but I'd prefer to get a functional version done first. To make things more interesting, though, I'll take some liberties in my state representations. For example, I have an idea for determining if a board is in a winning state using bitmasks.
