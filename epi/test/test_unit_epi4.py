import unittest
from epi.epi4 import *
import random
from epi.util import randomextra

class Max_Diff_Test(unittest.TestCase):

    def setUp(self):
        self.cls = Max_Diff

    def test_random(self):
        brute_force = self.cls.brute_force
        divide_and_conquer = self.cls.divide_and_conquer
        previous_min = self.cls.previous_min

        NUM_TESTS_RUN = 1000
        MAX_LIST_LENGTH = 100
        MAX_LIST_NUMBER = 100
        for _ in range(NUM_TESTS_RUN):
            random_list_length = random.randint(0, MAX_LIST_LENGTH)
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
