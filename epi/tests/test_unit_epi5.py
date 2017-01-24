import unittest
from epi.epi5 import *
from epi.utils import bitmanip, mathextra
import random, math

class P1_Parity_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P1_Parity

    def test_direct(self):
        direct = self.cls.direct
        self.assertEqual(direct(5), 0)
        self.assertEqual(direct(3), 0)
        self.assertEqual(direct(12), 0)
        self.assertEqual(direct(13), 1)
        self.assertEqual(direct(1), 1)
        self.assertEqual(direct(2), 1)
        self.assertEqual(direct(bitmanip.ones(64)), 0)
        self.assertEqual(direct(bitmanip.ones(70)), 0)

    def test_drop(self):
        drop = self.cls.drop
        self.assertEqual(drop(5), 0)
        self.assertEqual(drop(3), 0)
        self.assertEqual(drop(12), 0)
        self.assertEqual(drop(13), 1)
        self.assertEqual(drop(1), 1)
        self.assertEqual(drop(2), 1)
        self.assertEqual(drop(bitmanip.ones(64)), 0)
        self.assertEqual(drop(bitmanip.ones(70)), 0)

    def test_precompute(self):
        self.cls.fill_cache()

        precompute = self.cls.precompute
        self.assertEqual(precompute(5), 0)
        self.assertEqual(precompute(3), 0)
        self.assertEqual(precompute(12), 0)
        self.assertEqual(precompute(13), 1)
        self.assertEqual(precompute(1), 1)
        self.assertEqual(precompute(2), 1)
        self.assertEqual(precompute(bitmanip.ones(64)), 0)
        self.assertEqual(precompute(bitmanip.ones(70)), 0)

    def test_precompute_rand(self):
        drop = self.cls.drop
        precompute = self.cls.precompute

        NUM_TESTS_RUN = 10
        MAX_BIT_SIZE = 256
        MAX_CACHE_BIT_SIZE = 18
        for _ in range(NUM_TESTS_RUN):
            self.cls.fill_cache(random.randint(1, MAX_CACHE_BIT_SIZE))

            random_number = random.randint(0, 2**MAX_BIT_SIZE)
            self.assertEqual(drop(random_number), precompute(random_number))

class P2_SwapBits_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P2_SwapBits

    def test_swap_bits_index(self):
        swap_bits_index = self.cls.swap_bits_index
        self.assertEqual(swap_bits_index(1, 0, 1), 2)
        self.assertEqual(swap_bits_index(2, 1, 0), 1)
        self.assertEqual(swap_bits_index(1, 63, 0), 1 << 63)

class P3_Reverse_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P3_Reverse

    def test_swap_reverse(self):
        swap_reverse = self.cls.swap_reverse
        self.assertEqual(swap_reverse(0xAAAAAAAAAAAAAAAA, 4, 60),
                                           0xA55555555555555A)
        self.assertEqual(swap_reverse(0x5555555555555555, 4, 60),
                                           0x5AAAAAAAAAAAAAA5)
        self.assertEqual(swap_reverse(1, 0, 59), 1 << 58)
        self.assertEqual(swap_reverse(3, 1, 4), 9)
        self.assertEqual(swap_reverse(0b00110011, 2, 6), 0b00001111)

    def test_swap_reverse_size(self):
        swap_reverse_size = self.cls.swap_reverse_size
        self.assertEqual(swap_reverse_size(0xAAAAAAAAAAAAAAAA),
                                           0x5555555555555555)
        self.assertEqual(swap_reverse_size(0x5555555555555555),
                                           0xAAAAAAAAAAAAAAAA)
        self.assertEqual(swap_reverse_size(1), 1 << 63)
        self.assertEqual(swap_reverse_size(3), 3 << 62)

    def test_precompute(self):
        precompute = self.cls.precompute

        self.cls.fill_cache(5)

        self.assertEqual(precompute(0xAAAAAAAAAAAAAAAA, 4, 60),
                                           0xA55555555555555A)
        self.assertEqual(precompute(0x5555555555555555, 4, 60),
                                           0x5AAAAAAAAAAAAAA5)
        self.assertEqual(precompute(1, 0, 59), 1 << 58)
        self.assertEqual(precompute(3, 1, 4), 9)
        self.assertEqual(precompute(0b00110011, 2, 6), 0b00001111)

    def test_precompute_size(self):
        precompute_size = self.cls.precompute_size

        self.cls.fill_cache()

        self.assertEqual(precompute_size(0xAAAAAAAAAAAAAAAA), 0x5555555555555555)
        self.assertEqual(precompute_size(0x5555555555555555), 0xAAAAAAAAAAAAAAAA)
        self.assertEqual(precompute_size(1), 1 << 63)
        self.assertEqual(precompute_size(3), 3 << 62)

    def test_precompute_rand(self):
        swap_reverse = self.cls.swap_reverse
        precompute = self.cls.precompute

        NUM_TESTS_RUN = 10
        MAX_BIT_SIZE = 256
        MAX_CACHE_BIT_SIZE = 18
        for _ in range(NUM_TESTS_RUN):
            self.cls.fill_cache(random.randint(1, MAX_CACHE_BIT_SIZE))

            random_number = random.randint(0, 2**MAX_BIT_SIZE)
            bit_length = random_number.bit_length()
            random_start = random.randint(0, bit_length)
            random_end = random.randint(random_start, bit_length)
            self.assertEqual(
                    swap_reverse(random_number, random_start, random_end),
                    precompute(random_number, random_start, random_end))

class P4_ClosestSameBits_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P4_ClosestSameBits

    def test_first_consecutive_diff_iterate(self):
        first_consecutive_diff_iterate = self.cls.first_consecutive_diff_iterate
        self.assertEqual(first_consecutive_diff_iterate(5), 6)
        self.assertEqual(first_consecutive_diff_iterate(9), 10)
        self.assertEqual(first_consecutive_diff_iterate(12), 10)

    def test_first_consecutive_diff_bitmanip(self):
        first_consecutive_diff_bitmanip = self.cls.first_consecutive_diff_bitmanip
        self.assertEqual(first_consecutive_diff_bitmanip(5), 6)
        self.assertEqual(first_consecutive_diff_bitmanip(9), 10)
        self.assertEqual(first_consecutive_diff_bitmanip(12), 10)

class P5_Powerset_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P5_Powerset

        f = frozenset

        self.SETS = []
        self.POWERSETS = []

        self.SETS.append({})
        self.POWERSETS.append({ f({}) })

        self.SETS.append({0})
        self.POWERSETS.append({ f({}), f({0}) })

        self.SETS.append({0, 1})
        self.POWERSETS.append({ f({}), f({0}), f({1}), f({0, 1}) })

        self.SETS.append({0, 1, 2})
        self.POWERSETS.append({ f({}), f({0}), f({1}), f({0, 1}),
                         f({2}), f({0, 2}), f({1, 2}), f({0, 1, 2}) })

    def test_bit_array_map(self):
        bit_array_map = self.cls.bit_array_map

        for i in range(len(self.SETS)):
            self.assertEqual(bit_array_map(self.SETS[i]), self.POWERSETS[i])

    def test_bit_array_map_rand(self):
        bit_array_map = self.cls.bit_array_map

        NUM_TESTS_RUN = 10
        MAX_SET_SIZE = 15
        for _ in range(NUM_TESTS_RUN):
            random_set_length = random.randint(0, MAX_SET_SIZE)
            S = set(range(random_set_length))
            powerset_length = len(bit_array_map(S))
            self.assertEqual(powerset_length, 2 ** random_set_length)

    def test_recursive_default(self):
        recursive_default = self.cls.recursive_default

        for i in range(len(self.SETS)):
            self.assertEqual(recursive_default(self.SETS[i]), self.POWERSETS[i])

    def test_recursive_default_rand(self):
        recursive_default = self.cls.recursive_default

        NUM_TESTS_RUN = 10
        MAX_SET_SIZE = 15
        for _ in range(NUM_TESTS_RUN):
            random_set_length = random.randint(0, MAX_SET_SIZE)
            S = set(range(random_set_length))
            powerset_length = len(recursive_default(S))
            self.assertEqual(powerset_length, 2 ** random_set_length)

    def test_recursive_choice(self):
        recursive_choice = self.cls.recursive_choice

        for i in range(len(self.SETS)):
            self.assertEqual(recursive_choice(self.SETS[i]), self.POWERSETS[i])

    def test_recursive_choice_rand(self):
        recursive_choice = self.cls.recursive_choice

        NUM_TESTS_RUN = 10
        MAX_SET_SIZE = 15
        for _ in range(NUM_TESTS_RUN):
            random_set_length = random.randint(0, MAX_SET_SIZE)
            S = set(range(random_set_length))
            powerset_length = len(recursive_choice(S))
            self.assertEqual(powerset_length, 2 ** random_set_length)

class P5_1_Subsets_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P5_1_Subsets

        f = frozenset

        self.SETS = []
        self.SUBSETS_LIST = []

        self.SETS.append({})
        self.SUBSETS_LIST.append({ f({}) })

        self.SETS.append({0})
        self.SUBSETS_LIST.append({ f({}), f({0}) })

        self.SETS.append({0, 1})
        self.SUBSETS_LIST.append({ f({}), f({0}), f({1}), f({0, 1}) })

        self.SETS.append({0, 1, 2})
        self.SUBSETS_LIST.append({ f({}), f({0}), f({1}), f({0, 1}),
                         f({2}), f({0, 2}), f({1, 2}), f({0, 1, 2}) })

    def filter_set(self, S, k):
        """
        Return a set with items in S that are of length k.
        """

        return {s for s in S if len(s) == k}

    def test_bit_array_map(self):
        bit_array_map = self.cls.bit_array_map
        filter_set = self.filter_set

        for i in range(len(self.SETS)):
            for j in range(i + 1):
                self.assertEqual(bit_array_map(self.SETS[i], j),
                                 filter_set(self.SUBSETS_LIST[i], j))

    def test_bit_array_map_rand(self):
        bit_array_map = self.cls.bit_array_map

        NUM_TESTS_RUN = 10
        MAX_SET_SIZE = 15
        for _ in range(NUM_TESTS_RUN):
            random_set_length = random.randint(0, MAX_SET_SIZE)
            S = set(range(random_set_length))
            random_subset_length = random.randint(0, random_set_length)

            number_subsets = len(bit_array_map(S, random_subset_length))
            self.assertEqual(number_subsets,
                  mathextra.n_choose_r(random_set_length, random_subset_length))

    def test_recursive_default(self):
        recursive_default = self.cls.recursive_default
        filter_set = self.filter_set

        for i in range(len(self.SETS)):
            for j in range(i + 1):
                self.assertEqual(recursive_default(self.SETS[i], j),
                                 filter_set(self.SUBSETS_LIST[i], j))

    def test_recursive_default_rand(self):
        recursive_default = self.cls.recursive_default

        NUM_TESTS_RUN = 10
        MAX_SET_SIZE = 15
        for _ in range(NUM_TESTS_RUN):
            random_set_length = random.randint(0, MAX_SET_SIZE)
            S = set(range(random_set_length))
            random_subset_length = random.randint(0, random_set_length)

            number_subsets = len(recursive_default(S, random_subset_length))
            self.assertEqual(number_subsets,
                  mathextra.n_choose_r(random_set_length, random_subset_length))

    def test_recursive_choice(self):
        recursive_choice = self.cls.recursive_choice
        filter_set = self.filter_set

        for i in range(len(self.SETS)):
            for j in range(i + 1):
                self.assertEqual(recursive_choice(self.SETS[i], j),
                                 filter_set(self.SUBSETS_LIST[i], j))

    def test_recursive_choice_rand(self):
        recursive_choice = self.cls.recursive_choice

        NUM_TESTS_RUN = 10
        MAX_SET_SIZE = 15
        for _ in range(NUM_TESTS_RUN):
            random_set_length = random.randint(0, MAX_SET_SIZE)
            S = set(range(random_set_length))
            random_subset_length = random.randint(0, random_set_length)

            number_subsets = len(recursive_choice(S, random_subset_length))
            self.assertEqual(number_subsets,
                  mathextra.n_choose_r(random_set_length, random_subset_length))

class P6_StringIntegerConversion_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P6_StringIntegerConversion

    def test_int_to_string_concatenate(self):
        int_to_string_concatenate = self.cls.int_to_string_concatenate
        self.assertEqual(int_to_string_concatenate(0), "0")
        self.assertEqual(int_to_string_concatenate(79312), "79312")
        self.assertEqual(int_to_string_concatenate(-813289), "-813289")
        self.assertEqual(int_to_string_concatenate(9382901), "9382901")

    def test_int_to_string_list(self):
        int_to_string_list = self.cls.int_to_string_list
        self.assertEqual(int_to_string_list(0), "0")
        self.assertEqual(int_to_string_list(79312), "79312")
        self.assertEqual(int_to_string_list(-813289), "-813289")
        self.assertEqual(int_to_string_list(9382901), "9382901")

    def test_int_to_string_generator(self):
        int_to_string_generator = self.cls.int_to_string_generator
        self.assertEqual(int_to_string_generator(0), "0")
        self.assertEqual(int_to_string_generator(79312), "79312")
        self.assertEqual(int_to_string_generator(-813289), "-813289")
        self.assertEqual(int_to_string_generator(9382901), "9382901")

    def test_int_to_string_deque(self):
        int_to_string_deque = self.cls.int_to_string_deque
        self.assertEqual(int_to_string_deque(0), "0")
        self.assertEqual(int_to_string_deque(79312), "79312")
        self.assertEqual(int_to_string_deque(-813289), "-813289")
        self.assertEqual(int_to_string_deque(9382901), "9382901")

    def test_string_to_int(self):
        string_to_int = self.cls.string_to_int
        self.assertEqual(0, string_to_int("0"))
        self.assertEqual(79312, string_to_int("79312"))
        self.assertEqual(-813289, string_to_int("-813289"))
        self.assertEqual(9382901, string_to_int("9382901"))

class P7_BaseConversion_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P7_BaseConversion

    def test_int_to_string_concatenate(self):
        convert_base = self.cls.convert_base

        self.assertEqual(convert_base("0", 10, 16), "0")
        self.assertEqual(convert_base("79312", 10, 16), "135d0")
        self.assertEqual(convert_base("-813289", 10, 16), "-c68e9")
        self.assertEqual(convert_base("9382901", 10, 16), "8f2bf5")

        self.assertEqual(convert_base("90812", 10, 8), "261274")
        self.assertEqual(convert_base("983", 10, 2), "1111010111")
        self.assertEqual(convert_base("324", 5, 10), "89")

class P8_SpreadsheetColumnEncoding_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P8_SpreadsheetColumnEncoding

    def test_column_id_encode(self):
        column_id_encode = self.cls.column_id_encode

        self.assertEqual(column_id_encode(1), "a")
        self.assertEqual(column_id_encode(27), "aa")
        self.assertEqual(column_id_encode(26), "z")
        self.assertEqual(column_id_encode(55), "bc")
        self.assertEqual(column_id_encode(702), "zz")
        self.assertEqual(column_id_encode(703), "aaa")

    def test_column_id_decode(self):
        column_id_decode = self.cls.column_id_decode

        self.assertEqual(column_id_decode("a"), 1)
        self.assertEqual(column_id_decode("aa"), 27)
        self.assertEqual(column_id_decode("z"), 26)
        self.assertEqual(column_id_decode("bc"), 55)
        self.assertEqual(column_id_decode("zz"), 702)
        self.assertEqual(column_id_decode("aaa"), 703)

class P9_EliasGammaCoding_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P9_EliasGammaCoding

        self.LISTS = []
        self.CODESTRINGS = []

        self.LISTS.append([])
        self.CODESTRINGS.append("")

        self.LISTS.append([13])
        self.CODESTRINGS.append("0001101")

        self.LISTS.append([13, 14])
        self.CODESTRINGS.append("00011010001110")

        self.LISTS.append([1, 78, 30])
        self.CODESTRINGS.append("10000001001110000011110")

    def test_elias_gamma_list_encode(self):
        elias_gamma_list_encode = self.cls.elias_gamma_list_encode

        for i in range(len(self.LISTS)):
            self.assertEqual(
                    elias_gamma_list_encode(self.LISTS[i]), self.CODESTRINGS[i])

    def test_elias_gamma_list_decode(self):
        elias_gamma_list_decode = self.cls.elias_gamma_list_decode

        for i in range(len(self.LISTS)):
            self.assertEqual(
                    elias_gamma_list_decode(self.CODESTRINGS[i]), self.LISTS[i])

class P10_GreatestCommonDivisor_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P10_GreatestCommonDivisor

    def test_greatest_common_divisor(self):
        greatest_common_divisor = self.cls.greatest_common_divisor

        self.assertEqual(greatest_common_divisor(64, 6), 2)
        self.assertEqual(greatest_common_divisor(2310, 210), 210)
        self.assertEqual(greatest_common_divisor(810, 472), 2)
        self.assertEqual(greatest_common_divisor(871, 2132), 13)
        self.assertEqual(greatest_common_divisor(8912, 184), 8)
        self.assertEqual(greatest_common_divisor(813289, 937402), 1)

class P11_GeneratePrimes_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P11_GeneratePrimes

        self.MAX_NUMBERS = []
        self.PRIMES_LIST = []

        self.MAX_NUMBERS.append(100)
        self.PRIMES_LIST.append([2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                                  31, 37, 41, 43, 47, 53, 59, 61, 67,
                                  71, 73, 79, 83, 89, 97])

        self.MAX_NUMBERS.append(200)
        self.PRIMES_LIST.append([2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                                  31, 37, 41, 43, 47, 53, 59, 61, 67,
                                  71, 73, 79, 83, 89, 97, 101, 103, 107,
                                  109, 113, 127, 131, 137, 139, 149, 151,
                                  157, 163, 167, 173, 179, 181, 191, 193,
                                  197, 199])

        self.MAX_NUMBERS.append(300)
        self.PRIMES_LIST.append([2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                                 31, 37, 41, 43, 47, 53, 59, 61, 67,
                                 71, 73, 79, 83, 89, 97, 101, 103, 107,
                                 109, 113, 127, 131, 137, 139, 149, 151,
                                 157, 163, 167, 173, 179, 181, 191, 193,
                                 197, 199, 211, 223, 227, 229, 233, 239,
                                 241, 251, 257, 263, 269, 271, 277, 281,
                                 283, 293])

    def test_generate_primes_list(self):
        generate_primes_list = self.cls.generate_primes_list

        for i in range(len(self.MAX_NUMBERS)):
            self.assertEqual(
                generate_primes_list(self.MAX_NUMBERS[i]), self.PRIMES_LIST[i])

class P12_XyRectanglesIntersect_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P12_XyRectanglesIntersect

        Rectangle = mathextra.Rectangle
        FrozenPoint = mathextra.FrozenPoint

        point = FrozenPoint(0, 0)
        rectangle = Rectangle.create_from_lower_left(point, 5, 5)
        self.BASE_RECTANGLE = rectangle

        self.INTERSECT_RECTANGLES = []

        point = self.BASE_RECTANGLE.lower_right_point + FrozenPoint(-1, 1)
        rectangle = Rectangle.create_from_upper_left(point, 3, 3)
        self.INTERSECT_RECTANGLES.append(rectangle)
        rectangle = Rectangle.create_from_lower_left(point, 3, 3)
        self.INTERSECT_RECTANGLES.append(rectangle)

        point = self.BASE_RECTANGLE.upper_right_point + FrozenPoint(-1, -1)
        rectangle = Rectangle.create_from_lower_left(point, 3, 3)
        self.INTERSECT_RECTANGLES.append(rectangle)
        rectangle = Rectangle.create_from_lower_right(point, 3, 3)
        self.INTERSECT_RECTANGLES.append(rectangle)

        point = self.BASE_RECTANGLE.upper_left_point + FrozenPoint(1, -1)
        rectangle = Rectangle.create_from_lower_right(point, 3, 3)
        self.INTERSECT_RECTANGLES.append(rectangle)
        rectangle = Rectangle.create_from_upper_right(point, 3, 3)
        self.INTERSECT_RECTANGLES.append(rectangle)

        point = self.BASE_RECTANGLE.lower_left_point + FrozenPoint(1, 1)
        rectangle = Rectangle.create_from_upper_right(point, 3, 3)
        self.INTERSECT_RECTANGLES.append(rectangle)
        rectangle = Rectangle.create_from_upper_left(point, 3, 3)
        self.INTERSECT_RECTANGLES.append(rectangle)

        point = self.BASE_RECTANGLE.lower_right_point
        rectangle = Rectangle.create_from_upper_left(point, 3, 3)
        self.INTERSECT_RECTANGLES.append(rectangle)

        point = self.BASE_RECTANGLE.upper_right_point
        rectangle = Rectangle.create_from_lower_left(point, 3, 3)
        self.INTERSECT_RECTANGLES.append(rectangle)

        point = self.BASE_RECTANGLE.upper_left_point
        rectangle = Rectangle.create_from_lower_right(point, 3, 3)
        self.INTERSECT_RECTANGLES.append(rectangle)

        point = self.BASE_RECTANGLE.lower_left_point
        rectangle = Rectangle.create_from_upper_right(point, 3, 3)
        self.INTERSECT_RECTANGLES.append(rectangle)


        self.NON_INTERSECT_RECTANGLES = []

        point = self.BASE_RECTANGLE.lower_right_point + FrozenPoint(1, -1)
        rectangle = Rectangle.create_from_upper_left(point, 3, 3)
        self.NON_INTERSECT_RECTANGLES.append(rectangle)

        point = self.BASE_RECTANGLE.upper_right_point + FrozenPoint(1, 1)
        rectangle = Rectangle.create_from_lower_left(point, 3, 3)
        self.NON_INTERSECT_RECTANGLES.append(rectangle)

        point = self.BASE_RECTANGLE.upper_left_point + FrozenPoint(-1, 1)
        rectangle = Rectangle.create_from_lower_right(point, 3, 3)
        self.NON_INTERSECT_RECTANGLES.append(rectangle)

        point = self.BASE_RECTANGLE.lower_left_point + FrozenPoint(-1, -1)
        rectangle = Rectangle.create_from_upper_right(point, 3, 3)
        self.NON_INTERSECT_RECTANGLES.append(rectangle)

    def test_intersects(self):
        intersects = self.cls.intersects

        all_intersect = all(intersects(self.BASE_RECTANGLE, rectangle)
                            for rectangle in self.INTERSECT_RECTANGLES)
        self.assertTrue(all_intersect)

        none_intersect = all(not intersects(self.BASE_RECTANGLE, rectangle)
                             for rectangle in self.NON_INTERSECT_RECTANGLES)
        self.assertTrue(none_intersect)

    def test_intersection(self):
        intersection = self.cls.intersection

        Rectangle = mathextra.Rectangle
        FrozenPoint = mathextra.FrozenPoint

        point = self.BASE_RECTANGLE.lower_right_point + FrozenPoint(-1, 1)
        rectangle = Rectangle.create_from_upper_left(point, 1, 1)
        intersection_rectangle = intersection(self.BASE_RECTANGLE,
                                              self.INTERSECT_RECTANGLES[0])
        self.assertEqual(rectangle, intersection_rectangle)
        rectangle = Rectangle.create_from_lower_left(point, 1, 3)
        intersection_rectangle = intersection(self.BASE_RECTANGLE,
                                              self.INTERSECT_RECTANGLES[1])
        self.assertEqual(rectangle, intersection_rectangle)

        point = self.BASE_RECTANGLE.upper_right_point + FrozenPoint(-1, -1)
        rectangle = Rectangle.create_from_lower_left(point, 1, 1)
        intersection_rectangle = intersection(self.BASE_RECTANGLE,
                                              self.INTERSECT_RECTANGLES[2])
        self.assertEqual(rectangle, intersection_rectangle)
        rectangle = Rectangle.create_from_lower_right(point, 3, 1)
        intersection_rectangle = intersection(self.BASE_RECTANGLE,
                                              self.INTERSECT_RECTANGLES[3])
        self.assertEqual(rectangle, intersection_rectangle)

        point = self.BASE_RECTANGLE.upper_left_point + FrozenPoint(1, -1)
        rectangle = Rectangle.create_from_lower_right(point, 1, 1)
        intersection_rectangle = intersection(self.BASE_RECTANGLE,
                                              self.INTERSECT_RECTANGLES[4])
        self.assertEqual(rectangle, intersection_rectangle)
        rectangle = Rectangle.create_from_upper_right(point, 1, 3)
        intersection_rectangle = intersection(self.BASE_RECTANGLE,
                                              self.INTERSECT_RECTANGLES[5])
        self.assertEqual(rectangle, intersection_rectangle)

        point = self.BASE_RECTANGLE.lower_left_point + FrozenPoint(1, 1)
        rectangle = Rectangle.create_from_upper_right(point, 1, 1)
        intersection_rectangle = intersection(self.BASE_RECTANGLE,
                                              self.INTERSECT_RECTANGLES[6])
        self.assertEqual(rectangle, intersection_rectangle)
        rectangle = Rectangle.create_from_upper_left(point, 3, 1)
        intersection_rectangle = intersection(self.BASE_RECTANGLE,
                                              self.INTERSECT_RECTANGLES[7])
        self.assertEqual(rectangle, intersection_rectangle)

        point = self.BASE_RECTANGLE.lower_right_point
        rectangle = Rectangle.create_from_upper_left(point, 0, 0)
        intersection_rectangle = intersection(self.BASE_RECTANGLE,
                                              self.INTERSECT_RECTANGLES[8])
        self.assertEqual(rectangle, intersection_rectangle)

        point = self.BASE_RECTANGLE.upper_right_point
        rectangle = Rectangle.create_from_lower_left(point, 0, 0)
        intersection_rectangle = intersection(self.BASE_RECTANGLE,
                                              self.INTERSECT_RECTANGLES[9])
        self.assertEqual(rectangle, intersection_rectangle)

        point = self.BASE_RECTANGLE.upper_left_point
        rectangle = Rectangle.create_from_lower_right(point, 0, 0)
        intersection_rectangle = intersection(self.BASE_RECTANGLE,
                                              self.INTERSECT_RECTANGLES[10])
        self.assertEqual(rectangle, intersection_rectangle)

        point = self.BASE_RECTANGLE.lower_left_point
        rectangle = Rectangle.create_from_upper_right(point, 0, 0)
        intersection_rectangle = intersection(self.BASE_RECTANGLE,
                                              self.INTERSECT_RECTANGLES[11])
        self.assertEqual(rectangle, intersection_rectangle)


        none_intersect = all(intersection(self.BASE_RECTANGLE,
                                          rectangle) is None
                             for rectangle in self.NON_INTERSECT_RECTANGLES)
        self.assertTrue(none_intersect)

class P12_1_IsRectangle_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P12_1_IsRectangle

        self.RECTANGLES = []

        Rectangle = mathextra.Rectangle
        FrozenPoint = mathextra.FrozenPoint

        point = FrozenPoint(0, 0)
        rectangle = Rectangle.create_from_lower_left(point, 3, 3)
        self.RECTANGLES.append(rectangle.points)

        point = FrozenPoint(0, 0)
        rectangle = Rectangle.create_from_lower_left(point, 0, 0)
        self.RECTANGLES.append(rectangle.points)

        point = FrozenPoint(1, 0)
        rectangle = Rectangle.create_from_lower_left(point, 3, 3)
        self.RECTANGLES.append(rectangle.points)

        point = FrozenPoint(1, 1)
        rectangle = Rectangle.create_from_upper_left(point, 3, 3)
        self.RECTANGLES.append(rectangle.points)

        point = FrozenPoint(-1, 1)
        rectangle = Rectangle.create_from_upper_right(point, 3, 3)
        self.RECTANGLES.append(rectangle.points)

        point = FrozenPoint(-1.2, 1.5)
        rectangle = Rectangle.create_from_upper_right(point, 6.7, 8.1)
        self.RECTANGLES.append(rectangle.points)


        p = mathextra.FrozenPoint

        self.RECTANGLES.append((p(0, 0), p(1, 1), p(-1, 1), p(0, 2)))

        angle = 25 * math.pi / 180

        self.RECTANGLES.append((p(0, 0),
                                p(math.cos(angle), math.sin(angle)),
                                p(-math.sin(angle), math.cos(angle)),
                                p(math.cos(angle) - math.sin(angle),
                                  math.sin(angle) + math.cos(angle))))

        self.NON_RECTANGLES = []

        self.NON_RECTANGLES.append((p(0, 0), p(1, 2), p(3, 2), p(8, 9)))
        self.NON_RECTANGLES.append((p(0, 0), p(0, 0), p(0, 0), p(1, 0)))
        self.NON_RECTANGLES.append((p(1, 0), p(0, 0), p(0, 0), p(0, 0)))
        self.NON_RECTANGLES.append((p(0, 0), p(0, 1), p(1, 0), p(1, 0)))
        self.NON_RECTANGLES.append((p(1, 0), p(0, 1), p(0, 0), p(2, 2)))
        self.NON_RECTANGLES.append((p(1, 0), p(0, 1), p(0, 0), p(1.01, 1.01)))

    def test_is_rectangle(self):
        is_rectangle = self.cls.is_rectangle

        all_are_rectangles = all(is_rectangle(*points)
                                 for points in self.RECTANGLES)
        self.assertTrue(all_are_rectangles)

        none_are_rectangles = all(not is_rectangle(*points)
                                  for points in self.NON_RECTANGLES)
        self.assertTrue(none_are_rectangles)

class P13_MultiplicationBitwise_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P13_MultiplicationBitwise

    def test_is_rectangle_rand(self):
        multiply_bitwise = self.cls.multiply_bitwise

        NUM_TESTS_RUN = 100
        MAX_NUMBER = 1000000
        for _ in range(NUM_TESTS_RUN):
            random_x = random.randint(0, MAX_NUMBER)
            random_y = random.randint(0, MAX_NUMBER)

            product = random_x * random_y

            self.assertEqual(multiply_bitwise(random_x, random_y), product)

class P14_FloorDivision_Test(unittest.TestCase):

    def setUp(self):
        self.cls = P14_FloorDivision

    def test_floordiv_bitwise_rand(self):
        floordiv_bitwise = self.cls.floordiv_bitwise

        NUM_TESTS_RUN = 100
        MAX_NUMBER = 1000000

        for _ in range(NUM_TESTS_RUN):
            random_x = random.randint(0, MAX_NUMBER)
            random_y = random.randint(1, MAX_NUMBER)

            quotient = random_x // random_y

            self.assertEqual(floordiv_bitwise(random_x, random_y), quotient)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
