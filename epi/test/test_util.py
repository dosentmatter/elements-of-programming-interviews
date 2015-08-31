import unittest
from epi.util.bitmanip import *

class log2_Test(unittest.TestCase):

    def test_log2(self):
        self.assertEqual(log2(1 << 63), 63)
        self.assertEqual(log2(1 << 7), 7)
        self.assertEqual(log2(1 << 8), 8)
        self.assertEqual(log2(1 << 90), 90)
        self.assertEqual(log2(1 << 4), 4)
        self.assertEqual(log2(1 << 21), 21)