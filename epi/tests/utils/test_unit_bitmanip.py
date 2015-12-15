import unittest
from epi.utils.bitmanip import *

class ones_Test(unittest.TestCase):

    def test_ones(self):
        self.assertEqual(ones(float('inf')), -1)
        self.assertEqual(ones(1), 1)
        self.assertEqual(ones(3), 7)
        self.assertEqual(ones(3, 1), 14)

class get_bit_Test(unittest.TestCase):

    def test_get_bit(self):
        x = 15

        self.assertEqual(get_bit(x, 0), 1)
        self.assertEqual(get_bit(x, 1), 1)
        self.assertEqual(get_bit(x, 2), 1)
        self.assertEqual(get_bit(x, 3), 1)

class get_bit_position_Test(unittest.TestCase):

    def test_get_bit_position(self):
        x = 15

        self.assertEqual(get_bit_position(x, 0), 1)
        self.assertEqual(get_bit_position(x, 1), 2)
        self.assertEqual(get_bit_position(x, 2), 4)
        self.assertEqual(get_bit_position(x, 3), 8)

class set_bit_Test(unittest.TestCase):

    def test_set_bit(self):
        x = 0

        self.assertEqual(get_bit(x, 0), 0)
        x = set_bit(x, 0)
        self.assertEqual(get_bit(x, 0), 1)

        self.assertEqual(get_bit(x, 1), 0)
        x = set_bit(x, 1)
        self.assertEqual(get_bit(x, 1), 1)

        self.assertEqual(get_bit(x, 2), 0)
        x = set_bit(x, 2)
        self.assertEqual(get_bit(x, 2), 1)

        self.assertEqual(get_bit(x, 3), 0)
        x = set_bit(x, 3)
        self.assertEqual(get_bit(x, 3), 1)

class unset_bit_Test(unittest.TestCase):

    def test_unset_bit(self):
        x = 15

        self.assertEqual(get_bit(x, 0), 1)
        x = unset_bit(x, 0)
        self.assertEqual(get_bit(x, 0), 0)

        self.assertEqual(get_bit(x, 1), 1)
        x = unset_bit(x, 1)
        self.assertEqual(get_bit(x, 1), 0)

        self.assertEqual(get_bit(x, 2), 1)
        x = unset_bit(x, 2)
        self.assertEqual(get_bit(x, 2), 0)

        self.assertEqual(get_bit(x, 3), 1)
        x = unset_bit(x, 3)
        self.assertEqual(get_bit(x, 3), 0)

class same_bits_up_Test(unittest.TestCase):

    def test_same_bits_up(self):
        self.assertEqual(same_bits_up(15), 23)
        self.assertEqual(same_bits_up(14), 19)
        self.assertEqual(same_bits_up(13), 14)
        self.assertEqual(same_bits_up(12), 17)
        self.assertEqual(same_bits_up(11), 13)
        self.assertEqual(same_bits_up(10), 12)
        self.assertEqual(same_bits_up(9), 10)
        self.assertEqual(same_bits_up(8), 16)
        self.assertEqual(same_bits_up(7), 11)
        self.assertEqual(same_bits_up(6), 9)
        self.assertEqual(same_bits_up(5), 6)
        self.assertEqual(same_bits_up(4), 8)
        self.assertEqual(same_bits_up(3), 5)
        self.assertEqual(same_bits_up(2), 4)
        self.assertEqual(same_bits_up(1), 2)
        self.assertEqual(same_bits_up(0), 0)

        self.assertEqual(same_bits_up(-1), -1)
        self.assertEqual(same_bits_up(-2), -2)
        self.assertEqual(same_bits_up(-3), -2)
        self.assertEqual(same_bits_up(-4), -4)
        self.assertEqual(same_bits_up(-5), -3)
        self.assertEqual(same_bits_up(-6), -4)
        self.assertEqual(same_bits_up(-7), -6)
        self.assertEqual(same_bits_up(-8), -8)
        self.assertEqual(same_bits_up(-9), -5)
        self.assertEqual(same_bits_up(-10), -7)
        self.assertEqual(same_bits_up(-11), -10)
        self.assertEqual(same_bits_up(-12), -8)
        self.assertEqual(same_bits_up(-13), -11)
        self.assertEqual(same_bits_up(-14), -12)
        self.assertEqual(same_bits_up(-15), -14)

class same_bits_down_Test(unittest.TestCase):

    def test_same_bits_down(self):
        self.assertEqual(same_bits_down(15), 15)
        self.assertEqual(same_bits_down(14), 13)
        self.assertEqual(same_bits_down(13), 11)
        self.assertEqual(same_bits_down(12), 10)
        self.assertEqual(same_bits_down(11), 7)
        self.assertEqual(same_bits_down(10), 9)
        self.assertEqual(same_bits_down(9), 6)
        self.assertEqual(same_bits_down(8), 4)
        self.assertEqual(same_bits_down(7), 7)
        self.assertEqual(same_bits_down(6), 5)
        self.assertEqual(same_bits_down(5), 3)
        self.assertEqual(same_bits_down(4), 2)
        self.assertEqual(same_bits_down(3), 3)
        self.assertEqual(same_bits_down(2), 1)
        self.assertEqual(same_bits_down(1), 1)
        self.assertEqual(same_bits_down(0), 0)

        self.assertEqual(same_bits_down(-1), -1)
        self.assertEqual(same_bits_down(-2), -3)
        self.assertEqual(same_bits_down(-3), -5)
        self.assertEqual(same_bits_down(-4), -6)
        self.assertEqual(same_bits_down(-5), -9)
        self.assertEqual(same_bits_down(-6), -7)
        self.assertEqual(same_bits_down(-7), -10)
        self.assertEqual(same_bits_down(-8), -12)
        self.assertEqual(same_bits_down(-9), -17)
        self.assertEqual(same_bits_down(-10), -11)
        self.assertEqual(same_bits_down(-11), -13)
        self.assertEqual(same_bits_down(-12), -14)
        self.assertEqual(same_bits_down(-13), -18)
        self.assertEqual(same_bits_down(-14), -15)
        self.assertEqual(same_bits_down(-15), -20)

class log2_Test(unittest.TestCase):

    def test_log2(self):
        self.assertEqual(log2(0), -float("inf"))
        self.assertEqual(log2(1 << 63), 63)
        self.assertEqual(log2(1 << 7), 7)
        self.assertEqual(log2(1 << 8), 8)
        self.assertEqual(log2(1 << 90), 90)
        self.assertEqual(log2(1 << 4), 4)
        self.assertEqual(log2(1 << 21), 21)

    def test_log2_cached(self):
        log2_cached = log2_cached_creator()
        self.assertEqual(log2_cached(0), -float("inf"))
        self.assertEqual(log2_cached(1 << 63), 63)
        self.assertEqual(log2_cached(1 << 7), 7)
        self.assertEqual(log2_cached(1 << 8), 8)
        self.assertEqual(log2_cached(1 << 90), 90)
        self.assertEqual(log2_cached(1 << 4), 4)
        self.assertEqual(log2_cached(1 << 21), 21)
        self.assertEqual(log2_cached(1 << 99), 99)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
