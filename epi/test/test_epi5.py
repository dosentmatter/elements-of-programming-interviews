import unittest
from epi.epi5 import *
import random

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
        
class P5_Powerset_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P5_Powerset
        
        f = frozenset
        
        self.input = []
        self.output = []
        
        self.input.append({})
        self.output.append({ f({}) })
        
        self.input.append({0})
        self.output.append({ f({}), f({0}) })
        
        self.input.append({0, 1})
        self.output.append({ f({}), f({0}), f({1}), f({0, 1}) })
        
        self.input.append({0, 1, 2})
        self.output.append({ f({}), f({0}), f({1}), f({0, 1}),
                         f({2}), f({0, 2}), f({1, 2}), f({0, 1, 2}) })

    def test_bit_array_map(self):
        bit_array_map = self.cls.bit_array_map
        self.assertEqual(bit_array_map(self.input[0]), self.output[0])
        self.assertEqual(bit_array_map(self.input[1]), self.output[1])
        self.assertEqual(bit_array_map(self.input[2]), self.output[2])
        self.assertEqual(bit_array_map(self.input[3]), self.output[3])

    def test_bit_array_map_rand(self):
        bit_array_map = self.cls.bit_array_map

        NUM_TESTS_RUN = 10
        MAX_SET_SIZE = 15
        for i in range(NUM_TESTS_RUN):
            random_length = random.randint(0, MAX_SET_SIZE)
            S = set(range(random_length))
            powerset_length = len(bit_array_map(S))
            self.assertEqual(powerset_length, 2 ** random_length)

    def test_recursive_default(self):
        recursive_default = self.cls.recursive_default
        self.assertEqual(recursive_default(self.input[0]), self.output[0])
        self.assertEqual(recursive_default(self.input[1]), self.output[1])
        self.assertEqual(recursive_default(self.input[2]), self.output[2])
        self.assertEqual(recursive_default(self.input[3]), self.output[3])

    def test_recursive_default_rand(self):
        recursive_default = self.cls.recursive_default

        NUM_TESTS_RUN = 10
        MAX_SET_SIZE = 15
        for i in range(NUM_TESTS_RUN):
            random_length = random.randint(0, MAX_SET_SIZE)
            S = set(range(random_length))
            powerset_length = len(recursive_default(S))
            self.assertEqual(powerset_length, 2 ** random_length)

    def test_recursive_choice(self):
        recursive_choice = self.cls.recursive_choice
        self.assertEqual(recursive_choice(self.input[0]), self.output[0])
        self.assertEqual(recursive_choice(self.input[1]), self.output[1])
        self.assertEqual(recursive_choice(self.input[2]), self.output[2])
        self.assertEqual(recursive_choice(self.input[3]), self.output[3])

    def test_recursive_choice_rand(self):
        recursive_choice = self.cls.recursive_choice

        NUM_TESTS_RUN = 10
        MAX_SET_SIZE = 15
        for i in range(NUM_TESTS_RUN):
            random_length = random.randint(0, MAX_SET_SIZE)
            S = set(range(random_length))
            powerset_length = len(recursive_choice(S))
            self.assertEqual(powerset_length, 2 ** random_length)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
