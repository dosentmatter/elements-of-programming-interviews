def ones(n, offset=0):
    """
    Return a number that is a stream of n 1's with an offset.
    """

    return ((1 << n) - 1) << offset

def get_bit(x, k):
    """
    Return the k-th bit of x.
    """

    return (x >> k) & 1

def toggle_bit(x, k):
    """
    Return x with the k-th bit toggled.
    """

    return (1 << k) ^ x

def drop_lowest_set_bit(x):
    """
    Return x with the lowest set bit set to 0.
    """

    return x & (x - 1)

def get_lowest_set_bit(x):
    """
    Return the lowest set bit of x.
    """

    return x & ~(x - 1)

def get_least_significant_bits(x, n):
    """
    Return the n least significant bits of x.
    """

    return x & ones(n)

def get_bits(x, k, size, offset=0):
    """
    Return the k-th set of size bits starting from offset.
    """

    answer = x >> offset
    answer >>= k * size
    return get_least_significant_bits(answer, size)

def swap_bits(x, i, j):
    """
    Return x with bits swapped by toggling bits i and j of x if different.
    """

    if (get_bit(x, i) != get_bit(x, j)):
        x = toggle_bit(toggle_bit(x, i), j)
    return x

def shift_bits(x, k):
    """
    Return x logically right shifted by k. k can be negative, which would
    mean a logical left shift.
    """
    if (k >= 0):
        return x << k
    else:
        return x >> -k

def log2(x):
    """
    Return the log base 2 of x.

    Finds the highest amount x can be rightshifted by a multiple of 2.
    Then goes downwards looking for any amounts x can still be rightshifted.
    
    Example:
    x == 1 << 59
    59 == 0b11 1011    # binary

    The highest amount x can be rightshifted by a multiple of 2 is 32.
    x >> = 32
    x == 1 << 27
    27 == 0b01 1011

    Now, the highest x can be rightshifted by is 16 == 32 >> 1.
    x >> 16
    x == 1 << 11
    11 == 0b00 1011

    Keep going, and x can still be shifted by 8, 2, and 1. At this point,
    x == 1 << 0 == 1.

    The answer will be the sum of the shifts: 32 + 16 + 8 + 2 + 1 == 59.
    """

    if (x == 0):
        return -float("inf")
    elif (x == 1):
        return 0

    highest_shift_amount = 1
    while (True):
        if (x >> highest_shift_amount):
            highest_shift_amount <<= 1
        else:
            highest_shift_amount >>= 1    # backtrack
            break

    shift_amount = highest_shift_amount

    answer = 0
    while (x != 1):
        if (x >> shift_amount):
            x >>= shift_amount
            answer += shift_amount
        shift_amount >>= 1
    return answer

def log2_cached_creator():
    """
    Return a closure that caches log2 answers.
    """

    log2_dict = {}
    log2_dict[0] = -float("inf")
    max_shift_amount = 0

    def closure(x):
        """
        Given an x, This will find and cache all solutions of numbers less
        than x if they haven't already been cached.
        """

        nonlocal max_shift_amount

        if (x in log2_dict):
            return log2_dict[x]

        while (True):
            max_num = 1 << max_shift_amount
            log2_dict[max_num] = max_shift_amount
            max_shift_amount += 1
            if (x == max_num):
                return log2_dict[x]
    return closure

def bit_array_select(L, bit_array, log2):
    """
    Return a frozenset that contains L[k] iff get_bit(bit_array, k) == 1.
    """

    S = set()
    while (bit_array):
        i = log2(get_lowest_set_bit(bit_array))
        bit_array = drop_lowest_set_bit(bit_array)
        S.add(L[i])
    return frozenset(S)
