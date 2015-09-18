import unittest
from epi.epi5 import *
from epi.util import bitmanip, mathextra
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
        self.assertEqual(direct(bitmanip.ones(64)), 0)
        self.assertEqual(direct(bitmanip.ones(70)), 0)

    def test_drop(self):
        drop = self.cls.drop
        self.assertEqual(drop(5), 0)
        self.assertEqual(drop(3), 0)
        self.assertEqual(drop(12), 0)
        self.assertEqual(drop(13), 1)
        self.assertEqual(drop(1), 1)
        self.assertEqual(drop(2), 1)
        self.assertEqual(drop(bitmanip.ones(64)), 0)
        self.assertEqual(drop(bitmanip.ones(70)), 0)

    def test_precompute(self):
        self.cls.fill_cache()

        precompute = self.cls.precompute
        self.assertEqual(precompute(5), 0)
        self.assertEqual(precompute(3), 0)
        self.assertEqual(precompute(12), 0)
        self.assertEqual(precompute(13), 1)
        self.assertEqual(precompute(1), 1)
        self.assertEqual(precompute(2), 1)
        self.assertEqual(precompute(bitmanip.ones(64)), 0)
        self.assertEqual(precompute(bitmanip.ones(70)), 0)

    def test_precompute_rand(self):
        drop = self.cls.drop
        precompute = self.cls.precompute

        NUM_TESTS_RUN = 10
        MAX_BIT_SIZE = 256
        MAX_CACHE_BIT_SIZE = 18
        for _ in range(NUM_TESTS_RUN):
            self.cls.fill_cache(random.randint(1, MAX_CACHE_BIT_SIZE))

            random_number = random.randint(0, 2**MAX_BIT_SIZE)
            self.assertEqual(drop(random_number), precompute(random_number))

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
        self.assertEqual(swap_reverse(0xAAAAAAAAAAAAAAAA, 4, 60),
                                           0xA55555555555555A)
        self.assertEqual(swap_reverse(0x5555555555555555, 4, 60),
                                           0x5AAAAAAAAAAAAAA5)
        self.assertEqual(swap_reverse(1, 0, 59), 1 << 58)
        self.assertEqual(swap_reverse(3, 1, 4), 9)
        self.assertEqual(swap_reverse(0b00110011, 2, 6), 0b00001111)

    def test_swap_reverse_size(self):
        swap_reverse_size = self.cls.swap_reverse_size
        self.assertEqual(swap_reverse_size(0xAAAAAAAAAAAAAAAA),
                                           0x5555555555555555)
        self.assertEqual(swap_reverse_size(0x5555555555555555),
                                           0xAAAAAAAAAAAAAAAA)
        self.assertEqual(swap_reverse_size(1), 1 << 63)
        self.assertEqual(swap_reverse_size(3), 3 << 62)

    def test_precompute(self):
        precompute = self.cls.precompute

        self.cls.fill_cache(5)

        self.assertEqual(precompute(0xAAAAAAAAAAAAAAAA, 4, 60),
                                           0xA55555555555555A)
        self.assertEqual(precompute(0x5555555555555555, 4, 60),
                                           0x5AAAAAAAAAAAAAA5)
        self.assertEqual(precompute(1, 0, 59), 1 << 58)
        self.assertEqual(precompute(3, 1, 4), 9)
        self.assertEqual(precompute(0b00110011, 2, 6), 0b00001111)

    def test_precompute_size(self):
        precompute_size = self.cls.precompute_size

        self.cls.fill_cache()

        self.assertEqual(precompute_size(0xAAAAAAAAAAAAAAAA), 0x5555555555555555)
        self.assertEqual(precompute_size(0x5555555555555555), 0xAAAAAAAAAAAAAAAA)
        self.assertEqual(precompute_size(1), 1 << 63)
        self.assertEqual(precompute_size(3), 3 << 62)

    def test_precompute_rand(self):
        swap_reverse = self.cls.swap_reverse
        precompute = self.cls.precompute

        NUM_TESTS_RUN = 10
        MAX_BIT_SIZE = 256
        MAX_CACHE_BIT_SIZE = 18
        for _ in range(NUM_TESTS_RUN):
            self.cls.fill_cache(random.randint(1, MAX_CACHE_BIT_SIZE))

            random_number = random.randint(0, 2**MAX_BIT_SIZE)
            bit_length = random_number.bit_length()
            random_start = random.randint(0, bit_length)
            random_end = random.randint(random_start, bit_length)
            self.assertEqual(
                    swap_reverse(random_number, random_start, random_end),
                    precompute(random_number, random_start, random_end))

class P4_ClosestSameBits_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P4_ClosestSameBits

    def test_first_consecutive_diff_iterate(self):
        first_consecutive_diff_iterate = self.cls.first_consecutive_diff_iterate
        self.assertEqual(first_consecutive_diff_iterate(5), 6)
        self.assertEqual(first_consecutive_diff_iterate(9), 10)
        self.assertEqual(first_consecutive_diff_iterate(12), 10)

    def test_first_consecutive_diff_bitmanip(self):
        first_consecutive_diff_bitmanip = self.cls.first_consecutive_diff_bitmanip
        self.assertEqual(first_consecutive_diff_bitmanip(5), 6)
        self.assertEqual(first_consecutive_diff_bitmanip(9), 10)
        self.assertEqual(first_consecutive_diff_bitmanip(12), 10)
        
class P5_Powerset_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P5_Powerset
        
        f = frozenset
        
        self.sets = []
        self.powersets = []
        
        self.sets.append({})
        self.powersets.append({ f({}) })
        
        self.sets.append({0})
        self.powersets.append({ f({}), f({0}) })
        
        self.sets.append({0, 1})
        self.powersets.append({ f({}), f({0}), f({1}), f({0, 1}) })
        
        self.sets.append({0, 1, 2})
        self.powersets.append({ f({}), f({0}), f({1}), f({0, 1}),
                         f({2}), f({0, 2}), f({1, 2}), f({0, 1, 2}) })

    def test_bit_array_map(self):
        bit_array_map = self.cls.bit_array_map

        for i in range(len(self.sets)):
            self.assertEqual(bit_array_map(self.sets[i]), self.powersets[i])

    def test_bit_array_map_rand(self):
        bit_array_map = self.cls.bit_array_map

        NUM_TESTS_RUN = 10
        MAX_SET_SIZE = 15
        for _ in range(NUM_TESTS_RUN):
            random_set_length = random.randint(0, MAX_SET_SIZE)
            S = set(range(random_set_length))
            powerset_length = len(bit_array_map(S))
            self.assertEqual(powerset_length, 2 ** random_set_length)

    def test_recursive_default(self):
        recursive_default = self.cls.recursive_default

        for i in range(len(self.sets)):
            self.assertEqual(recursive_default(self.sets[i]), self.powersets[i])

    def test_recursive_default_rand(self):
        recursive_default = self.cls.recursive_default

        NUM_TESTS_RUN = 10
        MAX_SET_SIZE = 15
        for _ in range(NUM_TESTS_RUN):
            random_set_length = random.randint(0, MAX_SET_SIZE)
            S = set(range(random_set_length))
            powerset_length = len(recursive_default(S))
            self.assertEqual(powerset_length, 2 ** random_set_length)

    def test_recursive_choice(self):
        recursive_choice = self.cls.recursive_choice

        for i in range(len(self.sets)):
            self.assertEqual(recursive_choice(self.sets[i]), self.powersets[i])

    def test_recursive_choice_rand(self):
        recursive_choice = self.cls.recursive_choice

        NUM_TESTS_RUN = 10
        MAX_SET_SIZE = 15
        for _ in range(NUM_TESTS_RUN):
            random_set_length = random.randint(0, MAX_SET_SIZE)
            S = set(range(random_set_length))
            powerset_length = len(recursive_choice(S))
            self.assertEqual(powerset_length, 2 ** random_set_length)

class P5_1_Subsets_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P5_1_Subsets
        
        f = frozenset
        
        self.sets = []
        self.subsets_list = []
        
        self.sets.append({})
        self.subsets_list.append({ f({}) })
        
        self.sets.append({0})
        self.subsets_list.append({ f({}), f({0}) })
        
        self.sets.append({0, 1})
        self.subsets_list.append({ f({}), f({0}), f({1}), f({0, 1}) })
        
        self.sets.append({0, 1, 2})
        self.subsets_list.append({ f({}), f({0}), f({1}), f({0, 1}),
                         f({2}), f({0, 2}), f({1, 2}), f({0, 1, 2}) })

    def filter_set(self, S, k):
        """
        Return a set with items in S that are of length k.
        """

        return {s for s in S if len(s) == k}

    def test_bit_array_map(self):
        bit_array_map = self.cls.bit_array_map
        filter_set = self.filter_set

        for i in range(len(self.sets)):
            for j in range(i + 1):
                self.assertEqual(bit_array_map(self.sets[i], j),
                                 filter_set(self.subsets_list[i], j))

    def test_bit_array_map_rand(self):
        bit_array_map = self.cls.bit_array_map

        NUM_TESTS_RUN = 10
        MAX_SET_SIZE = 15
        for _ in range(NUM_TESTS_RUN):
            random_set_length = random.randint(0, MAX_SET_SIZE)
            S = set(range(random_set_length))
            random_subset_length = random.randint(0, random_set_length)

            number_subsets = len(bit_array_map(S, random_subset_length))
            self.assertEqual(number_subsets, 
                  mathextra.n_choose_r(random_set_length, random_subset_length))

    def test_recursive_default(self):
        recursive_default = self.cls.recursive_default
        filter_set = self.filter_set

        for i in range(len(self.sets)):
            for j in range(i + 1):
                self.assertEqual(recursive_default(self.sets[i], j),
                                 filter_set(self.subsets_list[i], j))

    def test_recursive_default_rand(self):
        recursive_default = self.cls.recursive_default

        NUM_TESTS_RUN = 10
        MAX_SET_SIZE = 15
        for _ in range(NUM_TESTS_RUN):
            random_set_length = random.randint(0, MAX_SET_SIZE)
            S = set(range(random_set_length))
            random_subset_length = random.randint(0, random_set_length)

            number_subsets = len(recursive_default(S, random_subset_length))
            self.assertEqual(number_subsets, 
                  mathextra.n_choose_r(random_set_length, random_subset_length))

    def test_recursive_choice(self):
        recursive_choice = self.cls.recursive_choice
        filter_set = self.filter_set

        for i in range(len(self.sets)):
            for j in range(i + 1):
                self.assertEqual(recursive_choice(self.sets[i], j),
                                 filter_set(self.subsets_list[i], j))

    def test_recursive_choice_rand(self):
        recursive_choice = self.cls.recursive_choice

        NUM_TESTS_RUN = 10
        MAX_SET_SIZE = 15
        for _ in range(NUM_TESTS_RUN):
            random_set_length = random.randint(0, MAX_SET_SIZE)
            S = set(range(random_set_length))
            random_subset_length = random.randint(0, random_set_length)

            number_subsets = len(recursive_choice(S, random_subset_length))
            self.assertEqual(number_subsets, 
                  mathextra.n_choose_r(random_set_length, random_subset_length))

def main():
    unittest.main()

if __name__ == '__main__':
    main()