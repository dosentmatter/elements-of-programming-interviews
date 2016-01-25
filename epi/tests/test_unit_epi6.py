import collections
import operator
import random
import unittest

from epi.epi6 import *
from epi.utils import general, mathextra, randomextra

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

class P1_3_TwoKeyPartitioning_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P1_3_TwoKeyPartitioning

        self.NUMBER_KEY_VALUES = 2

    def test_two_key_partition(self):
        two_key_partition = self.cls.two_key_partition

        self.assertEqual(two_key_partition([]), [])

    def test_two_key_partition_random(self):
        two_key_partition = self.cls.two_key_partition

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
            two_key_partition(random_list)
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

    def test_two_key_partition_random_boolean(self):
        two_key_partition = self.cls.two_key_partition

        NUM_TESTS_RUN = 100
        MAX_LIST_LENGTH = 100
        for _ in range(NUM_TESTS_RUN):
            random_list_length = random.randint(1, MAX_LIST_LENGTH)
            random_list = randomextra.randlist_boolean(random_list_length)
            random_list = list(map(general.key, random_list))

            before_counter = collections.Counter(random_list)
            two_key_partition(random_list)
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

class P2_UninitializedArray_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P2_UninitializedArray

    def test_UninitializedArray(self):
        UninitializedArray = self.cls.UninitializedArray

        array = UninitializedArray(100)

        for element in array:
            self.assertIs(element, False)

        write_indices = {9, 39, 69, 99}

        for i in write_indices:
            array[i] = True
            self.assertIs(array[i], True)

        for i, element in enumerate(array):
            if (i not in write_indices):
                self.assertIs(element, False)

    def test_UninitializedArray_random(self):
        UninitializedArray = self.cls.UninitializedArray

        NUM_TESTS_RUN = 100
        MAX_ARRAY_LENGTH = 100
        for _ in range(NUM_TESTS_RUN):
            random_array_length = random.randint(0, MAX_ARRAY_LENGTH)
            random_array = UninitializedArray(random_array_length)

            for element in random_array:
                self.assertIs(element, False)

            random_write_amount = random.randint(0, random_array_length)
            random_write_indices = \
                randomextra.randlist_no_duplicates(random_array_length - 1,
                                                   random_write_amount)
            random_write_indices = set(random_write_indices)

            for i in random_write_indices:
                random_array[i] = True
                self.assertIs(random_array[i], True)

            for i, element in enumerate(random_array):
                if (i not in random_write_indices):
                    self.assertIs(element, False)

class P3_RobotMaxDiff_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P3_RobotMaxDiff

    def test_robot_max_diff(self):
        robot_max_diff = self.cls.robot_max_diff

        z_iterable = [0, 1, 2, 3, 4, 5]
        z_iterable = map(self.__class__.add_random_x_y_coordinates, z_iterable)
        self.assertEquals(robot_max_diff(z_iterable), 5)

        z_iterable = [0, 1, 99, 3, 4, 5]
        z_iterable = map(self.__class__.add_random_x_y_coordinates, z_iterable)
        self.assertEquals(robot_max_diff(z_iterable), 99)

        z_iterable = [12, 21, 5, 54, 6, 2, 6]
        z_iterable = map(self.__class__.add_random_x_y_coordinates, z_iterable)
        self.assertEquals(robot_max_diff(z_iterable), 49)

    @staticmethod
    def add_random_x_y_coordinates(z):
        ARBITRARY_MAX_X_Y = 1000000
        x = random.randint(0, ARBITRARY_MAX_X_Y)
        y = random.randint(0, ARBITRARY_MAX_X_Y)

        return mathextra.ThreeDimensionalPoint(x, y, z)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
