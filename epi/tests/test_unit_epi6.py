import unittest
from epi.epi6 import *
from epi.utils import randomextra, general
import random, operator, collections

class P1_ThreeWayPartitioning_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P1_ThreeWayPartitioning

    def test_three_way_partition(self):
        three_way_partition = self.cls.three_way_partition

        self.assertEqual(three_way_partition([], -1), [])

    def test_three_way_partition_random(self):
        three_way_partition = self.cls.three_way_partition

        NUM_TESTS_RUN = 100
        MAX_LIST_NUMBER = 1000
        MAX_LIST_LENGTH = 100
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

class P1_1_ThreeKeyPartitioning_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P1_1_ThreeKeyPartitioning

        self.NUMBER_KEY_VALUES = 3

    def test_three_key_partition(self):
        three_key_partition = self.cls.three_key_partition

        self.assertEqual(three_key_partition([]), [])

    def test_three_key_partition_random(self):
        three_key_partition = self.cls.three_key_partition

        NUM_TESTS_RUN = 100
        MAX_KEY_VALUE = 1000
        MAX_LIST_LENGTH = 100
        for _ in range(NUM_TESTS_RUN):
            random_list_length = random.randint(1, MAX_LIST_LENGTH)
            random_list = randomextra.randlist_subset(MAX_KEY_VALUE, \
                                                      random_list_length, \
                                                      self.NUMBER_KEY_VALUES)
            random_list = list(map(general.key, random_list))

            before_counter = collections.Counter(random_list)
            three_key_partition(random_list)
            after_counter = collections.Counter(random_list)

            self.assertEqual(before_counter, after_counter)

            done_values = set()
            random_iter = iter(random_list)
            previous_value = next(random_iter).value
            for key in random_iter:
                value = key.value

                if (value != previous_value):
                    self.assertNotIn(previous_value, done_values)
                    done_values.add(previous_value)

                    previous_value = value

class P1_2_FourKeyPartitioning_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P1_2_FourKeyPartitioning

        self.NUMBER_KEY_VALUES = 4

    def test_four_key_partition(self):
        four_key_partition = self.cls.four_key_partition

        self.assertEqual(four_key_partition([]), [])

    def test_four_key_partition_random(self):
        four_key_partition = self.cls.four_key_partition

        NUM_TESTS_RUN = 100
        MAX_KEY_VALUE = 1000
        MAX_LIST_LENGTH = 100
        for _ in range(NUM_TESTS_RUN):
            random_list_length = random.randint(1, MAX_LIST_LENGTH)
            random_list = randomextra.randlist_subset(MAX_KEY_VALUE, \
                                                      random_list_length, \
                                                      self.NUMBER_KEY_VALUES)
            random_list = list(map(general.key, random_list))

            before_counter = collections.Counter(random_list)
            four_key_partition(random_list)
            after_counter = collections.Counter(random_list)

            self.assertEqual(before_counter, after_counter)

            done_values = set()
            random_iter = iter(random_list)
            previous_value = next(random_iter).value
            for key in random_iter:
                value = key.value

                if (value != previous_value):
                    self.assertNotIn(previous_value, done_values)
                    done_values.add(previous_value)

                    previous_value = value

def main():
    unittest.main()

if __name__ == '__main__':
    main()
