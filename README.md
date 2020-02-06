# 16_Puzzle_Solver
The game board consists of a 4x4 grid, but with
no empty space, so there are 16 tiles instead of 15. In each turn, the player can either (1) choose a row of
the puzzle and slide the entire row of tiles left or right, with the left- or right-most tile \wrapping around"
to the other side of the board, or (3) choose a column of the puzzle and slide the entire the column up or
down, with the top- or bottom-most tile "wrapping around."

The goal of the puzzle is to find the shortest sequence of moves that restores the canonical configuration (on
the left above) given an initial board configuration.

The problem is that it is quite slow for complicated boards. Using this code as a starting point, implement a faster version, using
A* search with a suitable heuristic function that guarantees finding a solution in is few moves as possible.
