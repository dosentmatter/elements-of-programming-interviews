import unittest
from epi.epi5 import *
import timeit
from epi.util import timeitextra
from math import factorial

class P5_Powerset_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P5_Powerset

        self.TEST_SET_LENGTH = 22

        self.TEST_SET = set(range(self.TEST_SET_LENGTH))

    def test_bit_array_map(self):
        bit_array_map = self.cls.bit_array_map
        wrapped = timeitextra.wrapper(bit_array_map,
                                      self.TEST_SET)
        print("\n{}".format(timeit.timeit(wrapped, number=1)))

    def test_recursive_default(self):
        recursive_default = self.cls.recursive_default
        wrapped = timeitextra.wrapper(recursive_default,
                                      self.TEST_SET)
        print("\n{}".format(timeit.timeit(wrapped, number=1)))

    def test_recursive_choice(self):
        recursive_choice = self.cls.recursive_choice
        wrapped = timeitextra.wrapper(recursive_choice,
                                      self.TEST_SET)
        print("\n{}".format(timeit.timeit(wrapped, number=1)))

    def tearDown(self):
        print()

class P5_1_Subsets_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P5_1_Subsets

        self.TEST_SET_LENGTH = 22

        self.TEST_SET = set(range(self.TEST_SET_LENGTH))

    def test_bit_array_map(self):
        bit_array_map = self.cls.bit_array_map
        wrapped = timeitextra.wrapper(bit_array_map,
                                      self.TEST_SET,
                                      self.TEST_SET_LENGTH // 2)
        print("\n{}".format(timeit.timeit(wrapped, number=1)))

    def test_recursive_default(self):
        recursive_default = self.cls.recursive_default
        wrapped = timeitextra.wrapper(recursive_default,
                                      self.TEST_SET,
                                      self.TEST_SET_LENGTH // 2)
        print("\n{}".format(timeit.timeit(wrapped, number=1)))

    def test_recursive_choice(self):
        recursive_choice = self.cls.recursive_choice
        wrapped = timeitextra.wrapper(recursive_choice,
                                      self.TEST_SET,
                                      self.TEST_SET_LENGTH // 2)
        print("\n{}".format(timeit.timeit(wrapped, number=1)))

    def tearDown(self):
        print()

class P6_StringIntegerConversion_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P6_StringIntegerConversion

        self.INTEGER = factorial(15000)

    def test_int_to_string_concatenate(self):
        int_to_string_concatenate = self.cls.int_to_string_concatenate
        wrapped = timeitextra.wrapper(int_to_string_concatenate,
                                      self.INTEGER)
        print("\n{}".format(timeit.timeit(wrapped, number=1)))

    def test_int_to_string_list(self):
        int_to_string_list = self.cls.int_to_string_list
        wrapped = timeitextra.wrapper(int_to_string_list,
                                      self.INTEGER)
        print("\n{}".format(timeit.timeit(wrapped, number=1)))

    def test_int_to_string_generator(self):
        int_to_string_generator = self.cls.int_to_string_generator
        wrapped = timeitextra.wrapper(int_to_string_generator,
                                      self.INTEGER)
        print("\n{}".format(timeit.timeit(wrapped, number=1)))

    def test_int_to_string_deque(self):
        int_to_string_deque = self.cls.int_to_string_deque
        wrapped = timeitextra.wrapper(int_to_string_deque,
                                      self.INTEGER)
        print("\n{}".format(timeit.timeit(wrapped, number=1)))

    def tearDown(self):
        print()

def main():
    unittest.main()

if __name__ == '__main__':
    main()
