from puzzle import *


def test_board():
    bd = board.Board()
    assert bd.hole == (3, 0)
