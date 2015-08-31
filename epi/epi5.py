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
            opposite_i = (n - 1) - i
            x = bitmanip.swap_bits(x, i, opposite_i)
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

    @classmethod
    def recursive(cls, S):
        powerset = set()

