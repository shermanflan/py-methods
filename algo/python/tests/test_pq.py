
from algolib.model.heap import Heap


def test_heap():
    min_heap = Heap()

    min_heap.add(7, 'a')
    min_heap.add(6, 'b')
    min_heap.add(5, 'c')
    min_heap.add(4, 'v')
    min_heap.add(3, 'y')
    min_heap.add(2, 'x')
    min_heap.add(1, 'z')

    assert min_heap.peek_min() == (1, 'z')

    items = []
    while not min_heap.is_empty():

        key_tmp, val_temp = min_heap.remove_min()
        items.append((key_tmp, val_temp))

    assert items[:] == [(1, 'z'), (2, 'x'), (3, 'y'), (4, 'v'), (5, 'c'),
                     (6, 'b'), (7, 'a')]


def test_heap_from_array():
    min_heap = Heap()
    min_heap.from_array([(4, 'v'), (3, 'y'), (2, 'x'), (1, 'z')])

    assert min_heap.peek_min() == (1, 'z')

    items = []
    while not min_heap.is_empty():

        key_tmp, val_temp = min_heap.remove_min()
        items.append((key_tmp, val_temp))

    assert items[:4] == [(1, 'z'), (2, 'x'), (3, 'y'), (4, 'v')]


def test_remove():
    min_heap = Heap()

    loc_1 = min_heap.add(7, 'a')
    loc_2 = min_heap.add(6, 'b')
    loc_3 = min_heap.add(5, 'c')
    loc_4 = min_heap.add(4, 'v')
    loc_5 = min_heap.add(3, 'y')
    loc_6 = min_heap.add(2, 'x')
    loc_7 = min_heap.add(1, 'z')

    min_heap.remove(loc_6)
    min_heap.remove_min()
    assert min_heap.peek_min() == (3, 'y')


def test_update():
    min_heap = Heap()

    loc_1 = min_heap.add(7, 'a')
    loc_2 = min_heap.add(6, 'b')
    loc_3 = min_heap.add(5, 'c')
    loc_4 = min_heap.add(4, 'v')
    loc_5 = min_heap.add(3, 'y')
    loc_6 = min_heap.add(2, 'x')
    loc_7 = min_heap.add(1, 'z')

    min_heap.update(loc_4, 0, 'rko')

    assert min_heap.peek_min() == (0, 'rko')
