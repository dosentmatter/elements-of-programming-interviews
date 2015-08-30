import unittest
from epi.epi5 import *

class P1_Parity_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P1_Parity

    def test_direct(self):
        direct = self.cls.direct
        self.assertEqual(direct(5), 0)
        self.assertEqual(direct(3), 0)
        self.assertEqual(direct(12), 0)
        self.assertEqual(direct(13), 1)
        self.assertEqual(direct(1), 1)
        self.assertEqual(direct(2), 1)

    def test_drop(self):
        drop = self.cls.drop
        self.assertEqual(drop(5), 0)
        self.assertEqual(drop(3), 0)
        self.assertEqual(drop(12), 0)
        self.assertEqual(drop(13), 1)
        self.assertEqual(drop(1), 1)
        self.assertEqual(drop(2), 1)

    def test_precompute(self):
        precompute = self.cls.precompute
        self.assertEqual(precompute(5), 0)
        self.assertEqual(precompute(3), 0)
        self.assertEqual(precompute(12), 0)
        self.assertEqual(precompute(13), 1)
        self.assertEqual(precompute(1), 1)
        self.assertEqual(precompute(2), 1)

class P2_SwapBits_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P2_SwapBits

    def test_quick_swap(self):
        quick_swap = self.cls.quick_swap
        self.assertEqual(quick_swap(1, 0, 1), 2)
        self.assertEqual(quick_swap(2, 1, 0), 1)
        self.assertEqual(quick_swap(1, 63, 0), 1 << 63)

class P3_Reverse_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P3_Reverse

    def test_swap_reverse(self):
        swap_reverse = self.cls.swap_reverse
        self.assertEqual(swap_reverse(0xAAAAAAAAAAAAAAAA), 0x5555555555555555)
        self.assertEqual(swap_reverse(0x5555555555555555), 0xAAAAAAAAAAAAAAAA)
        self.assertEqual(swap_reverse(1), 1 << 63)
        self.assertEqual(swap_reverse(3), 3 << 62)

    def test_precompute(self):
        precompute = self.cls.precompute
        self.assertEqual(precompute(0xAAAAAAAAAAAAAAAA), 0x5555555555555555)
        self.assertEqual(precompute(0x5555555555555555), 0xAAAAAAAAAAAAAAAA)
        self.assertEqual(precompute(1), 1 << 63)
        self.assertEqual(precompute(3), 3 << 62)

class P4_ClosestSameBits_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P4_ClosestSameBits

    def test_first_consecutive_diff(self):
        first_consecutive_diff = self.cls.first_consecutive_diff
        self.assertEqual(first_consecutive_diff(5), 6)
        self.assertEqual(first_consecutive_diff(9), 10)
        self.assertEqual(first_consecutive_diff(12), 10)

def main():
    unittest.main()

if __name__ == '__main__':
    main()