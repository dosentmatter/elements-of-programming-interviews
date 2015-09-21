import unittest
from epi.epi5 import *
import timeit
from epi.util import timeitextra

class P5_Powerset_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P5_Powerset

        self.TEST_SET_LENGTH = 22

        self.test_set = set(range(self.TEST_SET_LENGTH))

    def test_bit_array_map(self):
        bit_array_map = self.cls.bit_array_map
        wrapped = timeitextra.wrapper(bit_array_map,
                                      self.test_set)
        print("\n{}".format(timeit.timeit(wrapped, number=1)))

    def test_recursive_default(self):
        recursive_default = self.cls.recursive_default
        wrapped = timeitextra.wrapper(recursive_default,
                                      self.test_set)
        print("\n{}".format(timeit.timeit(wrapped, number=1)))

    def test_recursive_choice(self):
        recursive_choice = self.cls.recursive_choice
        wrapped = timeitextra.wrapper(recursive_choice,
                                      self.test_set)
        print("\n{}".format(timeit.timeit(wrapped, number=1)))

    def tearDown(self):
        print()

class P5_1_Subsets_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P5_1_Subsets

        self.TEST_SET_LENGTH = 22

        self.test_set = set(range(self.TEST_SET_LENGTH))

    def test_bit_array_map(self):
        bit_array_map = self.cls.bit_array_map
        wrapped = timeitextra.wrapper(bit_array_map,
                                      self.test_set,
                                      self.TEST_SET_LENGTH // 2)
        print("\n{}".format(timeit.timeit(wrapped, number=1)))

    def test_recursive_default(self):
        recursive_default = self.cls.recursive_default
        wrapped = timeitextra.wrapper(recursive_default,
                                      self.test_set,
                                      self.TEST_SET_LENGTH // 2)
        print("\n{}".format(timeit.timeit(wrapped, number=1)))

    def test_recursive_choice(self):
        recursive_choice = self.cls.recursive_choice
        wrapped = timeitextra.wrapper(recursive_choice,
                                      self.test_set,
                                      self.TEST_SET_LENGTH // 2)
        print("\n{}".format(timeit.timeit(wrapped, number=1)))

    def tearDown(self):
        print()

def main():
    unittest.main()

if __name__ == '__main__':
    main()
