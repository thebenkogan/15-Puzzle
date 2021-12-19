from puzzle import *

# True if 'lst1' and 'lst2' contain the same elements.
# Both lists must be sortable.
def equal_sets(lst1, lst2):
    lst1.sort()
    lst2.sort()
    return lst1 == lst2


def test_board():
    bd = board.Board()
    assert bd.hole == (3, 0)
    assert bd.path == []
    assert bd.prev == None

    holes = bd.hole_squares()
    expected = [(3, 1), (2, 0)]
    assert equal_sets(holes, expected)

    assert bd.move((3, 1))
    assert bd.move((2, 1))

    holes = bd.hole_squares()
    expected = [(2, 2), (2, 0), (1, 1), (3, 1)]
    assert equal_sets(holes, expected)

    assert not bd.move((0, 3))

    assert bd.find_num(11) == (3, 1)
    assert bd.find_num(63) == None

    bd_copy = bd.copy()
    assert bd.board == bd_copy.board
    bd.move((1, 1))
    assert not bd.board == bd_copy.board
