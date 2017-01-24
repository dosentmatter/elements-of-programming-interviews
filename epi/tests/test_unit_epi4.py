import unittest
from epi.epi4 import *
import random
from epi.utils import randomextra

class P1_MaxDiff_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P1_MaxDiff

    def test_random(self):
        brute_force = self.cls.brute_force
        divide_and_conquer = self.cls.divide_and_conquer
        previous_min = self.cls.previous_min

        NUM_TESTS_RUN = 1000
        MIN_MAX_DIFF_LIST_LENGTH = 2
        MAX_LIST_LENGTH = 100
        MAX_LIST_NUMBER = 100
        for _ in range(NUM_TESTS_RUN):
            random_list_length = random.randint(MIN_MAX_DIFF_LIST_LENGTH,
                                                MAX_LIST_LENGTH)
            random_list = \
                randomextra.randlist_duplicates(MAX_LIST_NUMBER,
                                                random_list_length)

            a = brute_force(random_list)
            b = divide_and_conquer(random_list)
            c = previous_min(random_list)

            self.assertEqual(a, b)
            self.assertEqual(b, c)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
