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

def drop_LSB(x):
    """
    Return x with the LSB (least significant bit) set to 0.
    """

    return x & (x - 1)

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
    """

    if (x == 0):
        return float(-"inf")
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

#def bit_array_select(L, bit_array):
#    """
#    Return a frozenset that contains L[k] iff get_bit(bit_array, k) == 1.
#    """

#    S = set()
#    while (bit_array):
