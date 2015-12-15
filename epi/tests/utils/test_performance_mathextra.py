import unittest
from epi.utils.mathextra import *
import timeit
from epi.utils import timeitextra

class is_prime_Test(unittest.TestCase):

    def setUp(self):
        self.PRIME = 29996224275833

    def test_is_prime(self):
        wrapped = timeitextra.wrapper(is_prime,
                                      self.PRIME)
        print("\n{}".format(timeit.timeit(wrapped, number=1)))
        print(is_prime(self.PRIME))

    def test_is_prime_sieve(self):
        wrapped = timeitextra.wrapper(is_prime_sieve,
                                      self.PRIME)
        print("\n{}".format(timeit.timeit(wrapped, number=1)))
        print(is_prime_sieve(self.PRIME))

    def tearDown(self):
        print()

def main():
    unittest.main()

if __name__ == '__main__':
    main()
