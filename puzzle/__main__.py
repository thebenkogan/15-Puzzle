import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import board
import solver
import time

bd = board.Board()
print(bd)

while False:
    bd.shuffle()
    print(bd)
    path = solver.new_solver(bd)
    print(len(path))
    for mv in path:
        bd.move(mv)
    print(bd)

while True:
    print("")
    num = input()
    if num == "q":
        exit()
    if num == "s":
        bd.shuffle()
        print(bd)
        continue
    if num == "solve":
        if bd.board == board.solved:
            print("Already solved.")
            continue
        path = solver.solve_full(bd)
        if len(path) == 0:
            print("No path found.")
        else:
            for mv in path:
                bd.move(mv)
                print(bd)
                if bd.board == board.solved:
                    print("Solved in " + str(len(path)) + " moves!")
                else:
                    print("")
                time.sleep(0.7)
        continue
    try:
        num = int(num)
    except:
        print("Try again.")
        continue
    coord = bd.find_num(num)
    if coord == None:
        print("Number not on board, try again.")
    else:
        if bd.move(coord):
            print(bd)
        else:
            print("Illegal move.")

bd = board.Board()
for i in range(50):
    bd.shuffle()
    path = solver.new_solver(bd)
    print(i)
