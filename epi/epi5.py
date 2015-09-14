from epi.util import bitmanip, mathextra
import itertools

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
    def quick_swap(x, i, j):
        """
        Swap by toggling bits i and j of x if different.
        """

        if (bitmanip.get_bit(x, i) != bitmanip.get_bit(x, j)):
            x = bitmanip.toggle_bit(bitmanip.toggle_bit(x, i), j)
        return x

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
        for offset in range(0, number_bits // 2):
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

        This grabs each set of bits of cls._cache_bit_size and maps them
        to the reverses.
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
                x = bitmanip.swap_bits_index(x, i, i + 1)
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
        """

        if not isinstance(S, set):
            S = set(S)

        L = list(S)
        subsets = set()

        def helper_add(start_i=0, subset=set()):
            """
            Populate subsets with the subsets of the elements L[start_i:] of
            size k. Start with an empty subset and keep adding.

            Each element defaults to not in the current subset. This is why
            subsets are added at each call to helper_add() if the
            size == k - elements not added are defaulted.

            :param start_i: the index of L to start generating the subets.
            :param subset: The current subset of S.
            """

            if (len(subset) == k):
                subsets.add(frozenset(subset))
                if (output):
                    print(subset)
                return

            for i in range(start_i, len(L)):
                subset.add(L[i])
                helper_add(i + 1, subset)
                subset.remove(L[i])

        def helper_remove(start_i=0, subset=set(S)):
            """
            Populate subsets with the subsets of the elements L[start_i:] of
            size k. Start with an empty subset and keep removing.

            Each element defaults to in the current subset. This is why
            subsets are added at each call to helper_remove() if the
            size == k- elements not removed are defaulted.

            :param start_i: the index of L to start generating the subets.
            :param subset: The current subset of S.
            """

            if (len(subset) == k):
                subsets.add(frozenset(subset))
                if (output):
                    print(subset)
                return

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
        subsets = set()

        def helper_add(start_i=0, subset=set()):
            """
            Populate subsets with the subsets of the elements L[start_i:] of
            size k.

            At each call of helper(), two choices are made to include and not
            include the current element of the set into the subset. This
            is why subset is only added to subset at the end of the
            call stack when the size == k, since a choice is made for
            all elements. The  ones that haven't been added explicitly default
            to not in the set.

            This is a pruned version of the P5_Powerset version. The if case
            limits len(subset) to be <= k for this function. In the elif case,
            this function only makes more calls if there are more items. This
            is needed because the if case allows subsets of length < k to
            sneak by.

            :param start_i: the index of L to start generating the subsets.
            :param subset: The current subset of S.
            """

            if (len(subset) == k):
                subsets.add(frozenset(subset))
                if (output):
                    print(subset)
            elif (start_i < len(L)):
                subset.add(L[start_i])
                helper_add(start_i + 1, subset)
                subset.remove(L[start_i])
                helper_add(start_i + 1, subset)

        def helper_remove(start_i=0, subset=set(S)):
            """
            Populate subsets with the subsets of the elements L[start_i:] of
            size k.

            At each call of helper(), two choices are made to not include and
            include the current element of the set into the subset. This
            is why subset is only added to subset at the end of the
            call stack when the size == k, since a choice is made for all
            elements. The ones that haven't been removed explicitly default
            to in the set.

            This is a pruned version of the P5_Powerset version. The if case
            limits len(subset) to be >= k for this function. In the elif case,
            this function only makes more calls if there are more items. This
            is needed because the if case allows subsets of length > k to
            sneak by.

            :param start_i: the index of L to start generating the subsets.
            :param subset: The current subset of S.
            """

            if (len(subset) == k):
                subsets.add(frozenset(subset))
                if (output):
                    print(subset)
            elif (start_i < len(L)):
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
