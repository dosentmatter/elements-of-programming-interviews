import unittest
from epi.util.bitmanip import *

class log2_Test(unittest.TestCase):

    def setUp(self):
        self.log2_cached = log2_cached_creator()

    def test_log2(self):
        self.assertEqual(log2(0), -float("inf"))
        self.assertEqual(log2(1 << 63), 63)
        self.assertEqual(log2(1 << 7), 7)
        self.assertEqual(log2(1 << 8), 8)
        self.assertEqual(log2(1 << 90), 90)
        self.assertEqual(log2(1 << 4), 4)
        self.assertEqual(log2(1 << 21), 21)

    def test_log2_cached(self):
        log2_cached = self.log2_cached
        self.assertEqual(log2_cached(0), -float("inf"))
        self.assertEqual(log2_cached(1 << 63), 63)
        self.assertEqual(log2_cached(1 << 7), 7)
        self.assertEqual(log2_cached(1 << 8), 8)
        self.assertEqual(log2_cached(1 << 90), 90)
        self.assertEqual(log2_cached(1 << 4), 4)
        self.assertEqual(log2_cached(1 << 21), 21)
        self.assertEqual(log2_cached(1 << 99), 99)