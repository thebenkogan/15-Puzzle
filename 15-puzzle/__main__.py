import board
import solver
import time

bd = board.Board()
bd.shuffle()

while True:
    moves = solver.next_moves(bd)
    if len(moves) == 0:
        print("Could not find path")
        exit()
    for move in moves:
        bd.move(move)
        print("")
        print(bd)
        time.sleep(0.1)
