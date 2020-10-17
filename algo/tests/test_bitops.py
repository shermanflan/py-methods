import pytest

from algolib.apply.math.bitops import BitMath


def test_get_bit():
    x = 0b0101
    bit = BitMath.get_bit(x, 2)

    assert bit == 1


def test_set_bit():
    x = 0b1010
    bit = BitMath.set_bit(x, 2)

    assert bit == 14


def test_clear_bit():
    x = 0b1111
    bit = BitMath.clear_bit(x, 2)

    assert bit == 11


def test_clear_msb():
    x = 0b11111111
    bit = BitMath.clear_msb(x, 4)

    assert bit == 15


def test_clear_lsb():
    x = 0b11111111
    bit = BitMath.clear_lsb(x, 3)

    assert bit == 240


def test_update_bit():
    x = 0b11111110
    bit = BitMath.update_bit(x, 4, False)

    assert f"{bit:b}" == "11110110"

    x = 0b11110110
    bit = BitMath.update_bit(x, 4, True)

    assert f"{bit:b}" == "11111110"


def test_reverse():

    x = 0b100011
    x_r = BitMath.reverse(x)

    assert f"{x_r:b}" == "110001"

    x = 0b101011
    x_r = BitMath.reverse(x)

    assert f"{x_r:b}" == "110101"
