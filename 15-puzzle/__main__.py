import board

bd = board.Board()
print(bd)

while True:
    num = input()
    if num == "q":
        exit()
    try:
        num = int(num)
    except:
        print("Try again.")
        continue
    coord = bd.find_num(num)
    if coord == None:
        print("Number not on board, try again.")
        continue
    else:
        if bd.move(coord):
            print(bd)
        else:
            print("Illegal move.")
