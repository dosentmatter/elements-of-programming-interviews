from collections import deque

from epi.utils import bitmanip, itertoolsextra, mathextra, python, stringextra

class P1_Parity:
    """
    Compute the parity of a 64-bit (or more) whole number x.
    """

    @staticmethod
    def direct(x):
        """
        Return the parity of x with direct calculation.

        Iterates through all bits and xors them.
        """

        result = 0
        while (x):
            result ^= (x & 1)
            x >>= 1
        return result

    @staticmethod
    def drop(x):
        """
        Return parity by only looking at high bits.

        Iterates through high bits by using drop_lowest_set_bit()
        and xors them.
        """

        result = 0
        while (x):
            result ^= 1
            x = bitmanip.drop_lowest_set_bit(x)
        return result

    _cache = []
    _cache_bit_size = 0
    _cache_filled = False

    @classmethod
    def fill_cache(cls, cache_bit_size=16):
        """
        Precompute _cache_bit_size-bit number parities and add to _cache.
        """

        cls.empty_cache()

        cls._cache_bit_size = cache_bit_size
        for i in range(2**cls._cache_bit_size):
            cls._cache.append(cls.drop(i))

        cls._cache_filled = True

    @classmethod
    def empty_cache(cls):
        """
        Empty _cache.
        """

        del cls._cache[:]
        _cache_bit_size = 0
        _cache_filled = False

    @classmethod
    def precompute(cls, x):
        """
        Return parity by using the precomputed parities.

        This grabs each set of bits of cls._cache_bit_size and maps them
        to the parities.
        In effect, it does this:
        return cls._cache[(x >> 48) & 0xFFFF] \
              ^ cls._cache[(x >> 32) & 0xFFFF] \
              ^ cls._cache[(x >> 16) & 0xFFFF] \
              ^ cls._cache[x & 0xFFFF]

        It also finishes up if x.bit_length() isn't divisible by
        cls._cache_bit_size.
        """

        if (not cls._cache_filled):
            cls.fill_cache()

        number_bits = x.bit_length()
        answer = 0
        divisible_split = number_bits // cls._cache_bit_size
        for i in range(divisible_split):
            answer ^= cls._cache[bitmanip.get_bits(x, i, cls._cache_bit_size)]

        if (number_bits % cls._cache_bit_size):
            answer ^= cls._cache[bitmanip.get_bits(x,
                                              divisible_split,
                                              cls._cache_bit_size)]

        return answer

class P2_SwapBits:
    """
    Swap bits at indices i and j of a 64-bit (or more) integer x.
    """

    @staticmethod
    def swap_bits_index(x, i, j=python.Parameter.OTHER_ARGUMENT):
        """
        Return x with bits swapped by toggling bits i and j of x if different.
        j defaults to i + 1.
        """

        return bitmanip.swap_bits_index(x, i, j)

class P3_Reverse:
    """
    Reverse the bits of a 64-bit (or more) integer x.
    """

    @staticmethod
    def swap_reverse(x, start=0, end=None):
        """
        Return x with bits from start (inclusive) to end (exclusive) reversed.
        """

        if (end == None):
            end = x.bit_length()

        number_bits = end - start
        for offset in range(number_bits // 2):
            i = start + offset
            i_opposite = (end - 1) - offset
            x = bitmanip.swap_bits_index(x, i, i_opposite)
        return x

    @classmethod
    def swap_reverse_size(cls, x, size=64):
        """
        Returns swap_reverse with size bits starting from 0.
        """

        return cls.swap_reverse(x, 0, size)

    _cache = []
    _cache_bit_size = 16
    _cache_filled = False

    @classmethod
    def fill_cache(cls, cache_bit_size=16):
        """
        Precompute _cache_bit_size-bit number reverses and add to _cache.
        Deletes pre-existing _cache.
        """

        cls.empty_cache()

        cls._cache_bit_size = cache_bit_size
        for i in range(2**cls._cache_bit_size):
            cls._cache.append(cls.swap_reverse_size(i, cls._cache_bit_size))

        cls._cache_filled = True

    @classmethod
    def empty_cache(cls):
        """
        Empty _cache.
        """

        del cls._cache[:]
        _cache_bit_size = 0
        _cache_filled = False

    @classmethod
    def precompute(cls, x, start=0, end=None):
        """
        Return x with bits from start (inclusive) to end (exclusive) reversed
        by using the precomputed reverses.

        This grabs each set of bits of cls._cache_bit_size, maps them
        to the reverses., and shifts them to their correct position.
        In effect, it does this:
        return cls._cache[(x >> 48) & 0xFFFF] \
              | cls._cache[(x >> 32) & 0xFFFF] << 16 \
              | cls._cache[(x >> 16) & 0xFFFF] << 32 \
              | cls._cache[x & 0xFFFF] << 48

        It also finishes up if number_bits isn't divisible by
        cls._cache_bit_size.

        The mask at the end makes the answer keep the non-rotated part.
        """

        if (not cls._cache_filled):
            cls.fill_cache()

        if (end == None):
            end = x.bit_length()

        number_bits = end - start
        answer = 0
        divisible_split = number_bits // cls._cache_bit_size
        for i in range(divisible_split):
            part_answer = cls._cache[bitmanip.get_bits(x,
                                                  i,
                                                  cls._cache_bit_size,
                                                  start)]
            shift_amount = end - ((i + 1) * cls._cache_bit_size)
            part_answer = bitmanip.shift_bits(part_answer, shift_amount)

            answer |= part_answer

        if (number_bits % cls._cache_bit_size):
            part_answer = cls._cache[bitmanip.get_bits(x,
                                                  divisible_split,
                                                  cls._cache_bit_size,
                                                  start)]
            shift_amount = end - ((divisible_split + 1) * cls._cache_bit_size)
            part_answer = bitmanip.shift_bits(part_answer, shift_amount)

            answer |= part_answer

        mask = bitmanip.ones(number_bits, start)
        answer &= mask
        answer |= x & ~mask
        return answer

    @classmethod
    def precompute_size(cls, x, size=64):
        """
        Returns precompute with size bits starting from 0.
        """

        return cls.precompute(x, 0, size)

class P4_ClosestSameBits:
    """
    x is a 64-bit (or more) number with k bits set high, k != 0, 64 (or more).
    Find a number y that also has k bits set high and is
    closest to x (either greater or less than x).
    """

    @staticmethod
    def first_consecutive_diff_iterate(x):
        """
        Return y by swapping the first two consecutive bits that differ.

        Iterate through the bits of x starting from the LSB
        and swapping the first two consecutive bits that differ. This works,
        intuitively, because it changes the least significant bits possible.
        """

        for i in range(x.bit_length()):
            if (bitmanip.get_bit(x, i) != bitmanip.get_bit(x, i + 1)):
                x = bitmanip.swap_bits_index(x, i)
                return x

    @staticmethod
    def first_consecutive_diff_bitmanip(x):
        """
        Return y by swapping the first two consecutive bits that differ.
        This works using bit manipulation.
        """

        bit_array = bitmanip.get_first(x, bitmanip.get_consecutive_diff)

        return bitmanip.swap_bits_bit_array(x, bit_array)

class P5_Powerset:
    """
    S is a set of distinct elements. Print the subsets one per line,
    with elements separated by commas.
    """

    @staticmethod
    def bit_array_map(S, output=False):
        """
        Return the powerset of S. Print the subsets if output == True.

        Iterates through all len(S)-bit numbers and maps each number to
        a subset to create the powerset.

        This is the slowest powerset method. For a set of size 22, timeit
        said it took ~40.76s.
        """


        if not isinstance(S, set):
            S = set(S)

        L = list(S)
        log2_cached = bitmanip.log2_cached_creator()
        powerset = set()
        for i in range(2 ** len(L)):
            subset = bitmanip.bit_array_select(L, i, log2_cached)
            powerset.add(subset)
            if (output):
                print(subset)
        return powerset

    @staticmethod
    def recursive_default(S, output=False):
        """
        Return the powerset of S. Print the subsets if output == True.

        For a call on a set of size N, there will be 2**N calls additions
        to powerset and 2**N calls to helper().

        This is the second fastest powerset method. For a set of size 22,
        timeit said it took ~6.53s.
        """

        if not isinstance(S, set):
            S = set(S)

        L = list(S)
        powerset = set()
        def helper(start_i=0, subset=set()):
            """
            Populate powerset with the powerset of the elements L[start_i:]

            Each element defaults to not in the current subset. This is why
            subsets are added at each call to helper() - elements not added
            are defaulted.

            :param start_i: the index of L to start generating the powerset.
            :param subset: The current subset of S.
            """

            powerset.add(frozenset(subset))
            if (output):
                print(subset)

            for i in range(start_i, len(L)):
                subset.add(L[i])
                helper(i + 1, subset)
                subset.remove(L[i])
        helper()
        return powerset

    @staticmethod
    def recursive_choice(S, output=False):
        """
        Return the powerset of S. Print the subsets if output == True.

        For a call on a set of size N, there will be 2**N calls additions
        to powerset and 2**(N+1) - 1 calls to helper().

        This is the second fastest powerset method. For a set of size 22,
        timeit said it took ~6.34s.

        Although it has more calls to helper than recursive_default(), I
        think it is faster because recursive_default() has to assign
        i during the for loop. They both have the same number of set additions,
        removes, and branches (if and for).
        """

        if not isinstance(S, set):
            S = set(S)

        L = list(S)
        powerset = set()
        def helper(start_i=0, subset=set()):
            """
            Populate powerset with the powerset of the elements L[start_i:]

            At each call of helper(), two choices are made to include and not
            include the current element of the set into the subset. This
            is why subset is only added to subset at the end of the
            call stack, when a choice is made for all elements.

            :param start_i: the index of L to start generating the powerset.
            :param subset: The current subset of S.
            """

            if (start_i == len(L)):
                powerset.add(frozenset(subset))
                if (output):
                    print(subset)
            else:
                subset.add(L[start_i])
                helper(start_i + 1, subset)
                subset.remove(L[start_i])
                helper(start_i + 1, subset)
        helper()
        return powerset

class P5_1_Subsets:
    """
    Print all subsets of S of size k {0, 1, 2, 3, ..., n}.
    """

    @staticmethod
    def bit_array_map(S, k, output=False):
        """
        Return the subsets of S of size k. Print the subsets if output == True.

        Iterates through all len(S)-bit numbers that have k high bits and maps
        each number to a subset to create the powerset.

        The code uses a while loop to check when its done but you can also use
        combinations (nCr) because you can calculate the number of subsets.

        This is the slowest.
        """

        if (k == 0):
            return { frozenset({}) }

        if not isinstance(S, set):
            S = set(S)

        L = list(S)
        log2_cached = bitmanip.log2_cached_creator()
        subsets = set()
        i = bitmanip.ones(k)
        upper_bound_i = 2 ** len(L)
        while (i < upper_bound_i):
            subset = bitmanip.bit_array_select(L, i, log2_cached)
            subsets.add(subset)
            if (output):
                print(subset)
            i = bitmanip.same_bits_up(i)
        return subsets

    @staticmethod
    def recursive_default(S, k, output=False):
        """
        Return the subsets of S of size k. Print the subsets if output == True.

        Since this uses recursion, if k != 0, len(S), there is a buildup before
        the subsets length start to == k. This is why there are two helpers,
        one that starts with 0 length subsets and adds (helper_add()), and one
        that starts with len(S) length subsets and removes (helper_remove()).

        number_possible_k_values == len(S) + 1 because for S of length n,
        there are (0, 1, 2, 3, ..., n) == n + 1 possible values for k.

        This divides the use of the helpers by
        (number_possible_k_values + 1) // 2 because it favors helper_add()
        for odd length number_possible_k_values. This is done because
        helper_add() is a little faster because it starts with an empty
        subset so it doesn't have to copy S to start.

        Example:
        For S == {0, 1, 2, 3}, len(S) = 4
        number_possible_k_values == 5 because k can be from [0:4]
        use helper_add() for k == 0, 1, 2
        use helper_remove() for k == 3, 4

        This is the fastest because it doesn't waste time
        """

        if not isinstance(S, set):
            S = set(S)

        L = list(S)
        L_length = len(L)
        subsets = set()

        def helper_add(start_i=0, subset=set()):
            """
            Populate subsets with the subsets of the elements L[start_i:] of
            size k. Start with an empty subset and keep adding.

            Each element defaults to not in the current subset. This is why
            subsets are added when subset_length == k, since the elements
            that are not added to the subset are defaulted to not being in the
            subset.

            This is a pruned version of the P5_Powerset version. The first if
            case limits subset_length to be <= k for this function. In the
            second if case, it only considers adding if there are enough
            elements to remove to reach a subset of size k.

            :param start_i: the index of L to start generating the subets.
            :param subset: The current subset of S.
            """

            subset_length = len(subset)

            if (subset_length == k):
                subsets.add(frozenset(subset))
                if (output):
                    print(subset)
                return

            elements_required_to_add = k - subset_length
            elements_remaining_to_add = L_length - start_i
            if (elements_required_to_add <= elements_remaining_to_add):
                for i in range(start_i, L_length):
                    subset.add(L[i])
                    helper_add(i + 1, subset)
                    subset.remove(L[i])

        def helper_remove(start_i=0, subset=set(S)):
            """
            Populate subsets with the subsets of the elements L[start_i:] of
            size k. Start with an empty subset and keep removing.

            Each element defaults to in the current subset. This is why
            subsets are added when subset_length == k, since the elements
            that are not removed from the subset are defaulted to being in the
            subset.

            This is a pruned version of the P5_Powerset version. The first if
            case limits subset_length to be >= k for this function. In the
            second if case, it considers removing if there are enough
            elements to remove to reach a subset of size k.

            :param start_i: the index of L to start generating the subets.
            :param subset: The current subset of S.
            """

            subset_length = len(subset)

            if (subset_length == k):
                subsets.add(frozenset(subset))
                if (output):
                    print(subset)
                return

            elements_required_to_remove = subset_length - k
            elements_remaining_to_remove = L_length - start_i
            if (elements_required_to_remove <= elements_remaining_to_remove):
                for i in range(start_i, len(L)):
                    subset.remove(L[i])
                    helper_remove(i + 1, subset)
                    subset.add(L[i])

        number_possible_k_values = len(S) + 1
        if (k < (number_possible_k_values + 1) // 2):
            helper_add()
        else:
            helper_remove()
        return subsets

    @staticmethod
    def recursive_choice(S, k, output=False):
        """
        Return the subsets of S of size k. Print the subsets if output == True.

        Since this uses recursion, if k != 0, len(S), there is a buildup before
        the subsets length start to == k. This is why there are two helpers,
        one that starts with 0 length subsets and adds first (helper_add()),
        and one that starts with len(S) length subsets and removes first
        (helper_remove()).

        number_possible_k_values == len(S) + 1 because for S of length n,
        there are (0, 1, 2, 3, ..., n) == n + 1 possible values for k.

        This divides the use of the helpers by
        (number_possible_k_values + 1) // 2 because it favors helper_add()
        for odd length number_possible_k_values. This is done because
        helper_add() is a little faster because it starts with an empty
        subset so it doesn't have to copy S to start.

        Example:
        For S == {0, 1, 2, 3}, len(S) = 4
        number_possible_k_values == 5 because k can be from [0:4]
        use helper_add() for k == 0, 1, 2
        use helper_remove() for k == 3, 4
        """

        if not isinstance(S, set):
            S = set(S)

        L = list(S)
        L_length = len(L)
        subsets = set()

        def helper_add(start_i=0, subset=set()):
            """
            Populate subsets with the subsets of the elements L[start_i:] of
            size k.

            At each call of helper_add(), two choices are made to include and
            not include the current element of the set into the subset. This
            is why subset is only added to subsets at the end of the
            call stack when the subset_length == k, since a choice is made for
            all elements. The ones that haven't been added explicitly default
            to not in the set.

            This is a pruned version of the P5_Powerset version. The first if
            case limits len(subset) to be <= k for this function. In the second
            if case, it only makes more calls if there are enough elements
            to possibly reach a subset of size k by removing from subset.

            :param start_i: the index of L to start generating the subsets.
            :param subset: The current subset of S.
            """

            subset_length = len(subset)

            if (subset_length == k):
                subsets.add(frozenset(subset))
                if (output):
                    print(subset)
                return

            elements_required_to_add = k - subset_length
            elements_remaining_to_add = L_length - start_i
            if (elements_required_to_add <= elements_remaining_to_add):
                subset.add(L[start_i])
                helper_add(start_i + 1, subset)
                subset.remove(L[start_i])
                helper_add(start_i + 1, subset)

        def helper_remove(start_i=0, subset=set(S)):
            """
            Populate subsets with the subsets of the elements L[start_i:] of
            size k.

            At each call of helper_remove(), two choices are made to not include
            and include the current element of the set into the subset. This
            is why subset is only added to subsets at the end of the
            call stack when the subset_length == k, since a choice is made for
            all elements. The ones that haven't been removed explicitly default
            to in the set.

            This is a pruned version of the P5_Powerset version. The first if
            case limits len(subset) to be >= k for this function. In the second
            if case, it only makes more calls if there are enough elements
            to possibly reach a subset of size k by removeing from subset.

            :param start_i: the index of L to start generating the subsets.
            :param subset: The current subset of S.
            """

            subset_length = len(subset)

            if (len(subset) == k):
                subsets.add(frozenset(subset))
                if (output):
                    print(subset)
                return

            elements_required_to_remove = subset_length - k
            elements_remaining_to_remove = L_length - start_i
            if (elements_required_to_remove <= elements_remaining_to_remove):
                subset.remove(L[start_i])
                helper_remove(start_i + 1, subset)
                subset.add(L[start_i])
                helper_remove(start_i + 1, subset)

        number_possible_k_values = len(S) + 1
        if (k < (number_possible_k_values + 1) // 2):
            helper_add()
        else:
            helper_remove()
        return subsets

class P6_StringIntegerConversion:
    """
    Implement string/integer inter-conversion functions.

    The int_to_string methods run at about the same speed.

    Joining an iterator is supposed to be slower because Python goes
    through the data twice - one pass to add up the lengths of
    the string fragments so it knows how much memory to allocate
    for the final result, and a second pass to copy the string
    fragments into the new buffer to create a single new string.
    It creates a temporary list of the generator in the first
    pass to use for the second pass. However, I don't notice
    the difference in performance between the iterators and
    string/collections below.
    """

    @staticmethod
    def int_to_string_concatenate(x, base=10):
        """
        Returns the string version of the integer x. Uses string
        concatenation. The string is represented in base base.
        Alphabetical digits are lowercase. Accepts bases in the range
        [2, 36].

        Inserting when doing concatenation ie.
        answer = char + answer (so no need to reverse at end)
        turns out to be slower.
        """

        if (not x):
            return "0"

        is_negative = False
        if (x < 0):
            x = -x
            is_negative = True

        answer = ""
        while (x):
            answer += stringextra.int_to_digit(x % base)
            x //= base

        if (is_negative):
            answer += '-'

        return answer[::-1]

    @staticmethod
    def int_to_string_list(x, base=10):
        """
        Returns the string version of the integer x. Uses list
        joining. The string is represented in base base.
        Alphabetical digits are lowercase. Accepts bases in the range
        [2, 36].
        """

        if (not x):
            return "0"

        is_negative = False
        if (x < 0):
            x = -x
            is_negative = True

        answer = []
        while (x):
            answer.append(stringextra.int_to_digit(x % base))
            x //= base

        if (is_negative):
            answer.append('-')

        return ''.join(reversed(answer))

    @staticmethod
    def int_to_string_generator(x, base=10):
        """
        Returns the string version of the integer x. Uses generator
        joining. The string is represented in base base.
        Alphabetical digits are lowercase. Accepts bases in the range
        [2, 36].
        """

        if (not x):
            return "0"

        is_negative = False
        if (x < 0):
            x = -x
            is_negative = True

        def helper_generator(y):
            """
            Yields each digit and sign of y as a string (character).
            """

            while(y):
                yield stringextra.int_to_digit(y % base)
                y //= base
            if (is_negative):
                yield '-'

        return ''.join(helper_generator(x))[::-1]

    @staticmethod
    def int_to_string_deque(x, base=10):
        """
        Returns the string version of the integer x. Uses deque
        joining. The string is represented in base base.
        Alphabetical digits are lowercase. Accepts bases in the range
        [2, 36].
        """

        if (not x):
            return "0"

        is_negative = False
        if (x < 0):
            x = -x
            is_negative = True

        answer = deque()
        while (x):
            answer.appendleft(stringextra.int_to_digit(x % base))
            x //= base

        if (is_negative):
            answer.appendleft('-')

        return ''.join(answer)

    @staticmethod
    def string_to_int(s, base=10):
        """
        Returns the integer version of the string x. base is the base
        s is represented in.
        Alphabetical digits are lowercase or uppercase. Accepts bases
        in the range [2, 36].
        """

        is_negative = False
        if (s[0] == '-'):
            s = iter(s)
            # skip first element
            next(s)
            is_negative = True

        answer = 0
        for c in s:
            answer = answer * base + stringextra.digit_to_int(c)

        if (is_negative):
            answer = -answer
        return answer

class P7_BaseConversion:
    """
    Convert a string s from base base1 to a string in base2.
    """

    @staticmethod
    def convert_base(s, base1, base2):
        """
        s is a base1 string that represents a number. Return a string
        that is the representation of s in base2.
        Alphabetical digits are lowercase. Accepts bases in the range
        [2, 36].
        """
        answer = stringextra.string_to_int(s, base1)
        answer = stringextra.int_to_string(answer, base2)
        return answer

class P8_SpreadsheetColumnEncoding:
    """
    Convert Excel column ids to and from the corresponding integer,
    with 'a' corresponding to 1.
    """

    _ALPHABET_SIZE = 26

    @classmethod
    def column_id_encode(cls, x):
        """
        Returns the encoded (string) version of the integer x.

        The code can't just use % and // directly because when the
        lowest digit is z, x is divisible by cls._ALPHABET_SIZE.
        """

        answer = deque()
        while (x):
            remainder = ((x - 1) % cls._ALPHABET_SIZE) + 1
            answer.appendleft(stringextra.column_id_digit_encode(remainder))
            x = (x - 1) // cls._ALPHABET_SIZE

        return ''.join(answer)

    @classmethod
    def column_id_decode(cls, s):
        """
        Returns the decoded (integer) version of the column id s.
        """

        answer = 0
        for c in s:
            answer = answer * cls._ALPHABET_SIZE + \
                     stringextra.column_id_digit_decode(c)
        return answer

class P9_EliasGammaCoding:
    """
    L is a list of n integers. Write an encode function that returns
    a string representing the concatenation of the Elias gamma codes
    for L, and a decode function that takes a string s, generated
    by the encode function, and returns the array that was passed to
    the encode function.
    """

    @staticmethod
    def elias_gamma_list_encode(L):
        """
        Returns the encoded (string) version of the list L.
        """

        answer = ""
        for x in L:
            answer += stringextra.elias_gamma_encode(x)
        return answer

    @staticmethod
    def elias_gamma_list_decode(s):
        """
        Returns the decoded (list) version of the string s.
        """

        answer = []
        i = 0
        length_s = len(s)
        while (i < length_s):
            decoding, i = stringextra.elias_gamma_decode(s, i, True)
            answer.append(decoding)
        return answer

class P10_GreatestCommonDivisor:
    """
    Compute the GCD of two numbers without using multiplication, division,
    or the modulus operators.
    """

    @staticmethod
    def greatest_common_divisor(x, y):
        """
        Returns the greatest common divisor of x and y iteratively.

        This works by using Euclid's algorithm as shown in the else case
        and in the if case when (y == 0). The code keeps x > y.
        There are some optimizations to Euclid's algorithm by checking
        when x and y are even.
        If both x and y are even, you can divide
        them both by 2 (right shift 1) and multiply the final answer
        by 2 (left shift 1).
        If only one is even, you can divide that one by 2 because
        2 is not a factor of the GCD since the other number isn't
        divisible by 2. When x is the even one (and y is odd),
        x gets divided by 2 so you have to check if x is still > y,
        otherwise you swap them.
        If they are both odd, follow with the Euclid's alogirthm,
        which is "The GCD of two numbers does not change if the larger
        number is replaced by its difference with the smaller number".
        You have to check if x and y need to be swapped in this case
        as well, to keep x > y.
        """

        if (x < y):
            x, y = y, x

        shift_multiplier = 0
        while (True):
            if (y == 0):
                return x << shift_multiplier

            x_is_even = mathextra.is_even(x)
            x_is_odd = not x_is_even
            y_is_even = mathextra.is_even(y)
            y_is_odd = not y_is_even

            if (x_is_even and y_is_even):
                x >>= 1
                y >>= 1
                shift_multiplier += 1
            elif (x_is_odd and y_is_even):
                y >>= 1
            elif (x_is_even and y_is_odd):
                x >>= 1
                if (x < y):
                    x, y = y, x
            else:
                x -= y
                if (x < y):
                    x, y = y, x

class P11_GeneratePrimes:
    """
    Given a single positive integer argument, n >= 2, return all the primes
    less than or equal to n.
    """

    @staticmethod
    def generate_primes(n):
        """
        Return a generator of prime numbers from [1, n].
        """

        return mathextra.generate_primes(n)

    @classmethod
    def generate_primes_list(cls, n):
        """
        Return a list of prime numbers from [1, n].
        """

        return list(cls.generate_primes(n))

class P12_XyRectanglesIntersect:
    """
    Let R and S be xy-aligned rectangles in the Cartesian plane. Write a
    function which tests if R and S have nonempty intersection. If the
    intersection is nonempty, return the rectangle formed by their
    intersection.
    """

    @staticmethod
    def intersects(R, S):
        """
        Return True if R intersects with S. This also considers
        the rectangles intersecting if they touch by a line or a point
        (0 area).
        """

        return R.intersects(S)

    @staticmethod
    def intersection(R, S):
        """
        Return the Rectangle formed from the intersection of R and
        S. If there is no intersection, return None.
        """

        return R.intersection(S)

class P12_1_IsRectangle:
    """
    Given four points in the plane, check if they are vertices of a
    rectangle (includes xy-aligned).
    """

    @staticmethod
    def is_rectangle(point0, point1, point2, point3):
        """
        Return True if points[0-3] are vertices of a rectangle.
        """

        return mathextra.Rectangle.is_rectangle(point0,
                                                point1,
                                                point2,
                                                point3)

class P12_2_RectanglesIntersect:
    """
    Check if two rectangles, not necessarily xy-aligned intersect.
    """

    @staticmethod
    def intersects(R, S):
        """
        Can use a method to check if two polygons intersect. There
        exists many algorithms. Maybe check if there exists points
        of one polygon that is contained by the other polygon.
        """

        return

class P13_MultiplicationBitwise:
    """
    Multiply two unsigned integers using only assignment, bitwise
    operators, loops, and conditionals.
    """

    @staticmethod
    def multiply_bitwise(x, y):
        """
        Return the product of x and y using only assignment, bitwise operators,
        loops, and conditionals.
        """

        return bitmanip.multiply_bitwise(x, y)

class P14_FloorDivision:
    """
    Given two positive integers, compute x // y if the only operators you
    can use are addition, subtraction, and multiplication.
    """

    @staticmethod
    def floordiv_bitwise(x, y):
        """
        Return x // y (both positive integers) using only
        addition, subtraction, multiplication, and bitwise operations.

        This works by finding the highest 2**k * y (where k is a whole
        number) to subtract from x multiple times until
        x < y (the remainder). In effect, this is building a binary number
        (0babcde) * y == x + remainder bit by bit. The answer would be
        (0babcde) in decimal.
        In the first loop, highest_power is found where
        2**highest_power * y == y << highest_power can be subtracted
        from x to keep x >= 0. This fails then backtracks.
        In the second loop, all powers <= highest_power are checked to
        see if y << power can be subtracted. If it can, 1 << power is
        added to answer. In effect, this is creating answer by
        (0ba0000) + (0b0b000) + (0b00c00) + (0b000d0) + (0b0000e)
        But the terms are only added if they != 0.

        I could've used a multiplier instead of power
        multiplier * y
        multiplier <<= 1
        But the power avoids multiplication and makes this problem more
        similar to bitmanip.log2
        I could've also done (1 << power) * y or (2 ** power) * y
        instead of y << power but this avoids multiplication.

        highest_power starts at 1 because if it exits the loop
        with a starting value of 0, the value would be -1 after exiting
        the loop. This case just means that !(y << 0 <= x) => (y > x) which
        is handled in the beginning if case.

        Optmizations:

        Add elif (x < (y << 1)): return 1 in the beginning if case to avoid
        going through the loops for a simple case. This just means that
        (2y > x >= y) since 2y == y << 1 and x < y is false since it is
        checked in the first if clause. This allows highest_power to start at 2.


        We know y << highest_power will be subtractable so we can skip the
        second while loop's first iteration.
        <<<<<<<
        power = highest_power

        answer = 0
        =======
        power = highest_power - 1

        answer = 1 << highest_power
        x -= y << highest_power
        >>>>>>>
        """

        if (y == 0):
            raise ZeroDivisionError("integer division by 0")

        if (x < y):
            return 0

        highest_power = 1
        while (True):
            if ((y << highest_power) <= x):
                highest_power += 1
            else:
                highest_power -= 1    # backtrack
                break

        power = highest_power

        answer = 0
        while (x >= y):
            subtract_amount = y << power
            if (x >= subtract_amount):
                x -= subtract_amount
                answer += 1 << power
            power -= 1
        return answer
