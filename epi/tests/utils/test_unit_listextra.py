import unittest
from epi.utils.listextra import *
from epi.utils import randomextra, general
import random, collections

class counting_sort_Test(unittest.TestCase):

    def test_counting_sort(self):
        self.assertEqual(counting_sort([]), [])

    def test_counting_sort_random(self):
        NUM_TESTS_RUN = 100
        MAX_KEY_VALUE = 10
        MAX_LIST_LENGTH = 100
        for _ in range(NUM_TESTS_RUN):
            random_list_length = random.randint(1, MAX_LIST_LENGTH)
            random_list = randomextra.randlist_duplicates(MAX_KEY_VALUE, \
                                                          random_list_length)
            random_list = list(map(general.key, random_list))

            before_counter = collections.Counter(random_list)
            sorted_list = counting_sort(random_list)
            after_counter = collections.Counter(sorted_list)

            self.assertEqual(before_counter, after_counter)

            previous_value = -float("inf")
            for key in sorted_list:
                value = key.value

                self.assertLessEqual(previous_value, value)
                previous_value = value
