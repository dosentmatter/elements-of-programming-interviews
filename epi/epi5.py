from epi.util import bitmanip

class P1_Parity:
    """
    Compute the parity of a 64-bit whole number x.
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

        Iterates through high bits by using drop_lsb() and xors them.
        """

        result = 0
        while (x):
            result ^= 1
            x = bitmanip.drop_lsb(x)
        return result

    P = []
    @classmethod
    def initialize(cls):
        """
        Precompute 16-bit number parities.
        """

        for i in range(2**16):
            cls.P.append(cls.drop(i))

    @classmethod
    def precompute(cls, x):
        """
        Return parity by using the precomputed parities.
        """

        return cls.P[(x >> 48) & 0xFFFF] \
              ^ cls.P[(x >> 32) & 0xFFFF] \
              ^ cls.P[(x >> 16) & 0xFFFF] \
              ^ cls.P[x & 0xFFFF]

P1_Parity.initialize()

class P2_SwapBits:
    """
    Swap bits at indices i and j of a 64-bit integer x.
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
    Reverse the bits of a 64-bit integer x.
    """

    @staticmethod
    def swap_reverse(x, n=64):
        """
        Return reverse by swapping opposite-sided pairs.
        """

        for i in range(n // 2):
            i_opposite = (n - 1) - i
            x = bitmanip.swap_bits(x, i, i_opposite)
        return x

    P = []
    @classmethod
    def initialize(cls):
        """
        Precompute 16-bit number reverses.
        """

        for i in range(2**16):
            cls.P.append(cls.swap_reverse(i, 16))

    @classmethod
    def precompute(cls, x):
        """
        Return reverse by using the precomputed reverses.
        """

        return cls.P[(x >> 48) & 0xFFFF] \
              | cls.P[(x >> 32) & 0xFFFF] << 16 \
              | cls.P[(x >> 16) & 0xFFFF] << 32 \
              | cls.P[x & 0xFFFF] << 48

P3_Reverse.initialize()

class P4_ClosestSameBits:
    """
    x is a 64-bit number with k bits set high, k != 0, 64.
	Find a number y that also has k bits set high and is
	closest to x (either greater or less than x).
    """

    @staticmethod
    def first_consecutive_diff(x):
        """
        Return y by swapping the first two consecutive bits that differ.

        Iterate through the bits of x starting from the LSB
        and swapping the first two consecutive bits that differ. This works,
        intuitively, because it changes the least significant bits possible.
        """

        for i in range(63):
            if (bitmanip.get_bit(x, i) != bitmanip.get_bit(x, i + 1)):
                x = bitmanip.swap_bits(x, i, i + 1)
                return x

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

#class P5_1_Subsets:
#    """
#    Print all subsets of size k o {1, 2, 3, ..., n}.
#    """
#
#    @staticmethod
#    def bit_array_map(S, output=False):
#        """
#        Return the powerset of S. Print the subsets if output == True.
#
#        Iterates through all len(S)-bit numbers and maps each number to
#        a subset to create the powerset.
#
#        This is the slowest powerset method. For a set of size 22, timeit
#        said it took ~40.76s.
#        """
#
#
#        if not isinstance(S, set):
#            S = set(S)
#
#        L = list(S)
#        log2_cached = bitmanip.log2_cached_creator()
#        powerset = set()
#        for i in range(2 ** len(L)):
#            subset = bitmanip.bit_array_select(L, i, log2_cached)
#            powerset.add(subset)
#            if (output):
#                print(subset)
#        return powerset
#
#    @staticmethod
#    def recursive_default(S, output=False):
#        """
#        Return the powerset of S. Print the subsets if output == True.
#
#        For a call on a set of size N, there will be 2**N calls additions
#        to powerset and 2**N calls to helper().
#
#        This is the second fastest powerset method. For a set of size 22,
#        timeit said it took ~6.53s.
#        """
#
#        if not isinstance(S, set):
#            S = set(S)
#
#        L = list(S)
#        powerset = set()
#        def helper(start_i=0, subset=set()):
#            """
#            Populate powerset with the powerset of the elements L[start_i:]
#
#            Each element defaults to not in the current subset. This is why
#            subsets are added at each call to helper() - elements not added
#            are defaulted.
#
#            :param start_i: the index of L to start generating the powerset.
#            :param subset: The current subset of S.
#            """
#
#            powerset.add(frozenset(subset))
#            if (output):
#                print(subset)
#
#            for i in range(start_i, len(L)):
#                subset.add(L[i])
#                helper(i + 1, subset)
#                subset.remove(L[i])
#        helper()
#        return powerset
#
#    @staticmethod
#    def recursive_choice(S, output=False):
#        """
#        Return the powerset of S. Print the subsets if output == True.
#
#        For a call on a set of size N, there will be 2**N calls additions
#        to powerset and 2**(N+1) - 1 calls to helper().
#
#        This is the second fastest powerset method. For a set of size 22,
#        timeit said it took ~6.34s.
#
#        Although it has more calls to helper than recursive_default(), I
#        think it is faster because recursive_default() has to assign
#        i during the for loop. They both have the same number of set additions,
#        removes, and branches (if and for).
#        """
#
#        if not isinstance(S, set):
#            S = set(S)
#
#        L = list(S)
#        powerset = set()
#        def helper(start_i=0, subset=set()):
#            """
#            Populate powerset with the powerset of the elements L[start_i:]
#
#            At each call of helper(), two choices are made to include and not
#            include the current element of the set into the subset. This
#            is why subset is only added to subset at the end of the
#            call stack, when a choice is made for all elements.
#
#            :param start_i: the index of L to start generating the powerset.
#            :param subset: The current subset of S.
#            """
#
#            if (start_i == len(L)):
#                powerset.add(frozenset(subset))
#                if (output):
#                    print(subset)
#            else:
#                subset.add(L[start_i])
#                helper(start_i + 1, subset)
#                subset.remove(L[start_i])
#                helper(start_i + 1, subset)
#        helper()
#        return powerset
