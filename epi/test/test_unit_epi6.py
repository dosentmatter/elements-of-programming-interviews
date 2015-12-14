import unittest
from epi.epi6 import *
from epi.util import randomextra
import random, operator, collections

class P1_ThreeWayPartitioning_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P1_ThreeWayPartitioning

    def test_three_way_partition_random(self):
        three_way_partition = self.cls.three_way_partition

        NUM_TESTS_RUN = 100
        MAX_LIST_NUMBER = 10
        MAX_LIST_LENGTH = 10
        OPERATORS = [operator.__lt__, operator.__eq__, operator.__gt__]
        for _ in range(NUM_TESTS_RUN):
            random_list_length = random.randint(1, MAX_LIST_LENGTH)
            random_list = randomextra.randlist_duplicates(MAX_LIST_NUMBER, \
                                                          random_list_length)
            random_i = random.randint(0, random_list_length - 1)

            pivot = random_list[random_i]

            before_counter = collections.Counter(random_list)
            three_way_partition(random_list, random_i)
            after_counter = collections.Counter(random_list)

            self.assertEqual(before_counter, after_counter)

            operator_i = 0
            for element in random_list:
                while (True):
                    if (OPERATORS[operator_i](element, pivot)):
                        break
                    operator_i += 1
                    self.assertTrue(operator_i < len(OPERATORS))
