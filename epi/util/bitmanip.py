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

def drop_lsb(x):
    """
    Return x with the LSB (least significant bit) set to 0.
    """

    return x & (x - 1)

def extract_lsb(x):
    """
    Return the LSB (least significant bit) of x.
    """

    return x & ~(x - 1)

def swap_bits(x, i, j):
    """
    Swap bits by toggling bits i and j of x if different.
    """

    if (get_bit(x, i) != get_bit(x, j)):
        x = toggle_bit(toggle_bit(x, i), j)
    return x

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
        i = log2(extract_lsb(bit_array))
        bit_array = drop_lsb(bit_array)
        S.add(L[i])
    return frozenset(S)
